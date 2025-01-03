# %%
import time
import datetime
from pyquery import PyQuery as pq
import requests
import json
req = requests.Session()
req.headers = {
    "Accept-Encoding": "gzip",
    "Accept-Language": "zh-Hans-CN;q=1, zh-Hant-CN;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

def get_course():
    # 获取课程列表
    res2 = req.get("https://mooc1-2.chaoxing.com/course/phone/courselistdata?courseFolderId=0&isFiled=0&query=")
    doc = pq(res2.text)
    for i in doc('li').items():
        tmp={
            "courseid":i.attr("courseid"),
            "clazzid":i.attr("clazzid"),
            "classname":i("dt").text()
        }
        print(tmp)
    exit()

# 获取作业详情
def get_homework(user):
    alltaskinfo = ""
    num = 0
    print("开始查询")
    for classitem in user["classinfo"]:
        classname = classitem['classname']
        try:
            res3 = req.get(
                f"https://mooc1.chaoxing.com/work/task-list?courseId={classitem['courseid']}&classId={classitem['clazzid']}&vx=1")
            doc2 = pq(res3.text)
            for classinfo in doc2('li').items():
                status=classinfo("span").items()
                # 未交且作业未截至的作业有两个span，一个是未交，一个是截止时间
                # pyquery获取到的是个生成器，所以用了__next__()方法
                if  len(classinfo("span"))==2 and status.__next__().text() == "未交":
                    num += 1
                    alltaskinfo += f"\n{classname} {classinfo('a').text()}:{classinfo('p').text()}\n  - {status.__next__().text()}"
                    # print(classname, classinfo("p").text())
        except:
            alltaskinfo += f"{classname} 查询失败\n"
            print(classname, "查询失败")
        time.sleep(1)
    print("查询完成:", end="")
    if num == 0:
        print("暂无作业\n")
    else:
        print("未交作业数量：", num)
        print(alltaskinfo)
        # try:
        #     requests.get(
        #         "http://127.0.0.1:8082/send_private_msg?user_id="+user["qq"]+"&message=学习通作业别忘了哦"+alltaskinfo)
        #     print("发送通知成功")
        # except:
        #     print("发送通知失败")
        print()
                    
if __name__ == "__main__":
    try:
        userdata = json.load(open("./data.json", 'r', encoding='utf8'))
        for user in userdata:
            req.headers["Cookie"]=""
            account = user["account"]
            password = user["password"]
            url = f"https://passport2-api.chaoxing.com/v11/loginregister?code={password}&cx_xxt_passport=json&uname={account}&loginType=1&roleSelect=true"
            res = req.get(url)
            if res.json()['mes'] == "验证通过":
                # 获取Cookie
                cookie = requests.utils.dict_from_cookiejar(req.cookies)
                mycookie = ""
                for key, value in cookie.items():
                    mycookie += f"{key}={value};"
                req.headers["Cookie"] = mycookie
                print(account,"登录成功")
                # 获取课程信息
                # get_course()
                # 获取作业信息
                get_homework(user)
                
                
    except Exception as e:
        print("登陆失败", e)
