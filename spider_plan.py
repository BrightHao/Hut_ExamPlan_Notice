import requests
import redis
from lxml import etree
from html.parser import HTMLParser

# 请求头
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
}


# 获取存储的cookies
def get_cookies(username):
    r = redis.Redis(host="127.0.0.1", port=6379)
    keys = r.hgetall(username)
    cookies = {k.decode('utf-8'): v.decode('utf-8') for k, v in keys.items()}
    return cookies


def login(username, encode):
    login_url = 'http://218.75.197.123:83/jsxsd/xk/LoginToXk'
    data = {
        "userAccount": username,
        "userPassword": '',
        "encoded": encode
    }
    s = requests.session()
    try:
        s.post(login_url, data=data, timeout=3)
    except Exception:
        return False
    cookies = s.cookies.get_dict()
    r = redis.Redis(host="127.0.0.1", port=6379)
    for cookie in cookies:
        r.hset(username, cookie, cookies[cookie])
    return cookies


def exam_plan(semester):
    from lxml import html
    url = 'http://218.75.197.123:83/jsxsd/xsks/xsksap_list'
    data = {
        "xnxqid": semester,
        "xqlbmc": "期末",
        "xqlb": 3
    }
    try:
        res = requests.post(url, data=data, cookies=get_cookies("17401200108"), headers=headers, timeout=3)
    except Exception:
        return False
    html_text = etree.HTML(res.text)
    trs = html_text.xpath('//table[@id="dataList"]/tr')
    if len(trs) == 0:  # 没登录
        cookies = login(username="17401200108", encode="MTc0MDEyMDAxMDg=%%%MDgyMFRITHphaTF6aG9uZw==")
        if not cookies:
            return False
        try:
            res = requests.post(url, data=data, cookies=cookies, headers=headers, timeout=3)
        except:
            return False
        html = etree.HTML(res.text)
        trs = html.xpath('//table[@id="dataList"]/tr')
        if not trs:
            return False
        tr = html_text.xpath('//table[@id="dataList"]')[0]
        t = html.tostring(tr)
        res = HTMLParser().unescape(t.decode())
        return t
    tr = html_text.xpath('//table[@id="dataList"]')[0]
    t = html.tostring(tr)
    res = HTMLParser().unescape(t.decode())
    return res


def formatTable(text):
    html = etree.HTML(text)
    trs = html.xpath('//table[@id="dataList"]/tr')
    data = []
    for tr in trs[1:]:
        tds = tr.xpath('./td')
        course = tds[4].xpath('./text()')[0]
        datetime = tds[6].xpath('./text()')[0]
        date, time = datetime.split(' ')
        classroom = tds[7].xpath('./text()')[0]
        data.append(
            {"course": course, "date": date, "time": time, "classroom": classroom})
    return data


if __name__ == "__main__":
    res = exam_plan("2020-2021-1")
    print(res)
