from app.models import Project

#新版的create_project函数
# list() 会新建独立列表，而不是复用传入的原列表。
def create_project(
    name: str,
    description: str | None = None,
    # tags 可选，只能是「字符串列表 / None」，默认None
    tags: list[str] | None = None,

    members: list[str] | None = None,
) -> Project: #返回值类型为Project
    safe_tags = [] if tags is None else list[str](tags)
    safe_members = [] if members is None else list[str](members)

    return Project(
        name=name,
        description=description,
        tags=safe_tags,
        members=safe_members,
    )


# 增加标签
def add_tag_in_place(
    project: Project,
    tag: str,
) -> None:
    project.tags.append(tag)



# 增加标签
def with_tag(
    project: Project,
    tag: str,
) -> Project:
    return Project(
        name=project.name,
        description=project.description,
        tags=[*project.tags, tag],
        members=list[str](project.members),
    )



# *list表示展开列表，将列表中的元素作为独立的参数传递给函数。 
# **dict表示展开字典，将字典中的键值对作为独立的参数传递给函数。

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

def clone_project(
    project: Project,
) -> Project:
    return Project(
        name=project.name,
        description=project.description,
        tags=list[str](project.tags),
        members=list[str](project.members),
    )


# 测试,否则此文件被引用时，会执行代码
if __name__ == "__main__":


    p1 = create_project_test2("AI Workspace Lite")
    p1["tags"].append("python")
    print("p1:", p1)

    #p2被污染了，因为p1的tags list被修改了
    p2 = create_project_test2("AI Workspace Lite2") 
    print("p2:", p2)

