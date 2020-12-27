from emailSender import mailTo
from spider_plan import exam_plan, formatTable


if __name__ == "__main__":
    res = exam_plan("2020-2021-1")
    with open("examPlan.txt", "r", encoding="utf-8") as f:
        t = "".join(f.readlines())
    with open("examPlan.txt", "w", encoding="utf-8") as f:
        f.write(res)
    if formatTable(t) == formatTable(res):
        print("两次的相等")
    else:
        to = mailTo(["861759757@qq.com", ], "考试安排提醒", res, format="html")
        print(to)
