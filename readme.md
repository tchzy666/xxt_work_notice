# 学习通作业提醒

#### 目的

很简单，就是一个查询并提醒 `未完成作业`的脚本

#### 开源许可

本人不对任何后果负责，不放心请不要使用此项目    
此项目禁止商业使用

### 使用方法
> 支持多用户  

打开 `data.json`，填入学习通的手机号和密码

在 `classinfo`填入你需要被提醒的课程

`courseid`和 `clazzid`可以在函数`get_course()`中抓取

将脚本及数据放到 服务器/云函数 定时执行即可

#### Q&A

Q: API从哪获取的 ?    
A: 在学习通的的微信公众号服务Tab栏中取得。

Q: 能不能使用qmsg/server酱 ?  
A: 可以，自己实现一下即可，详见脚本最后注释的部分。

Q: 其他问题 ?  
A: 如果有其他问题，直接在github上提issue
