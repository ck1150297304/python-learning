# 练习1
# count = 1
# while count <= 5:
#     print(count)
#     count += 1

# 练习2
# for i in range(1, 6):
#     print(i)

# 练习3
# scores = [88, 72, 95, 60, 100]
# for score in scores:
#     print(score)

# 练习4
# for i in range(1, 6):
#     if i == 3:
#         continue
#     print(i)

# 练习5
# for i in range(1,101):
#     if i > 3:
#         break
#     print(i)

# 工程练习
scores = [88, 72, 95, 60, 100]
for score in scores:
    if score >= 60:
        print("通过：" + str(score))
    else:
        print("未通过：" + str(score))
