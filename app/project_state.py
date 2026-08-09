# 创建项目结构体
def create_project(name):
    return {
        "name": name,
        "tags": [],
        "members": [],
    }

# p1 = create_project("AI Workspace Lite")
# print(p1)

# 增加标签
def add_tag_in_place(project, tag):
    # 直接修改项目的标签列表，而不是返回一个新的项目结构体
    project["tags"].append(tag)

# 增加标签
# 永远返回新对象，原始数据保持不变
# 执行顺序规则：
# 字典字面量，后面写的键，会覆盖前面同名的键。
def with_tag(project, tag):
    return {
        # 不可变性特征：返回一个新的项目结构体，而不是修改原始结构体
        **project,
        "tags": [*project["tags"], tag],
    }

# *list表示展开列表，将列表中的元素作为独立的参数传递给函数。 
# **dict表示展开字典，将字典中的键值对作为独立的参数传递给函数。

# p2 = with_tag(p1, "python")
# print( "p1 is p2?", p1 is p2)
# print( "p1 == p2?", p1 == p2)
# print( "p1['tags'] is p2['tags']?", p1["tags"] is p2["tags"] )

#这样的定义，会导致共享tags list，而不是创建一个新的list
def create_project_test1(name, tags=[]):
    return {
        "name": name,
        "tags": tags,
    }

#推荐的定义方式
def create_project_test2(name, tags=None):
    if tags is None:
        tags = []
    return {
        "name": name,
        "tags": tags,
    }

def clone_project(project):
    return {
        **project,
        "tags": [*project["tags"]],
        "members": [*project["members"]],
    }

# 测试,否则此文件被引用时，会执行代码
if __name__ == "__main__":


    p1 = create_project_test2("AI Workspace Lite")
    p1["tags"].append("python")
    print("p1:", p1)

    #p2被污染了，因为p1的tags list被修改了
    p2 = create_project_test2("AI Workspace Lite2") 
    print("p2:", p2)

