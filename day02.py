age = int(input("请输入年龄："))
if age >= 18:
    print("成年人")
else:
    print("未成年人")

fraction = int(input("请输入分数："))
if fraction >= 90:
    print("优秀")
elif fraction >= 80:
    print("良好")
elif fraction >= 60:
    print("及格")
else:
    print("不及格")

username = "admin"
password = "123456"
name = input("请输入用户名：")
num = int(input("请输入密码："))
if username == "admin" and password == num:
    print("登录成功")
else:
    print("用户名或网络错误")

number = int(input("请输入数字："))
if number > 0:
    print("正数")
elif number < 0:
    print("负数")
else:
    print(0)