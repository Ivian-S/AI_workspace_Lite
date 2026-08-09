# a = [1,2]
# b = a
# c=[1,2]

# print(b is a)
# print(c is a)

# # 内容相同
# # ≠
# # 同一个对象

# #不可变对象
# name = "Workspace"
# name = name + " Lite"

# # 后端开发真正危险的是“嵌套可变对象”
# project = {
#     "name": "AI Workspace Lite",
#     "tags": ["python"],
#     "settings": {"visibility": "private"},
# }
# # dict 是可变的
# # list 也是可变的

# # 浅拷贝：只复制第一层，不复制嵌套对象
# temp_project = project.copy()

# print( temp_project is project)
# print( temp_project["tags"] is project["tags"])

# # 两个 dict 不一样。
# # 但是里面的 tags 仍然是同一个 list。
# temp_project["tags"].append("javascript")
# print(project["tags"])

# #深拷贝
# from copy import deepcopy
# temp2_project = deepcopy(project)

# print( temp2_project is project)
# print( temp2_project["tags"] is project["tags"])

# 但是不要形成一个坏习惯：# “不知道引用关系怎么办？全部 deepcopy()。”
# 不允许这么学。

# 大型对象的深拷贝可能：
# 浪费内存；
# 增加运行时间；
# 复制本来应该共享的对象；
# 掩盖数据结构设计问题。

project = {
    "name": "AI Workspace Lite",
    "tags": ["python"],
    "settings": {"visibility": "private"},
}

# 函数参数也遵循同样的规则
# 增加标签
def add_tag(project, tag):
    project["tags"].append(tag)

add_tag(project, "javascript")

#**调用函数时，参数名称会绑定到传入的那个对象。**
print(project["tags"])
print(project["name"])

