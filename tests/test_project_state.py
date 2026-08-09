from unicodedata import name

from app import project_state
from app.project_state import (
    add_tag_in_place,
    create_project,
    with_tag,
    clone_project,
)

def test_assignment_share_same_project():
    project_a = create_project("AI Workspace Lite")
    project_b = project_a
    project_b["name"] += "Changed"

    assert project_a["name"] != "Changed"
    assert project_a is project_b

def test_in_place_operation_changes_original_project():
    project = create_project("Workspace")

    add_tag_in_place(project, "python")
    print(project)

    #内容一致，但是用is判断是否是同一个对象，结果是False
    assert project["tags"] == ["python"]

def test_with_tag_does_not_change_original_project():
    original = create_project("Workspace")

    updated = with_tag(original, "python")

    assert original["tags"] == []
    assert updated["tags"] == ["python"]

    assert original is not updated
    assert original["tags"] is not updated["tags"]


def test_create_project():
    project_a = create_project("A")
    project_b = create_project("B")

    assert project_a["members"] is not project_b["members"]

def test_shallow_copy_shares_nested_members():
    original = create_project("original")
    copied = original.copy()
    copied["members"].append("member")

    assert original["members"] == copied["members"]

def test_clone_project():
    original = create_project("original")
    cloned = clone_project(original)

    assert original is not cloned
    assert cloned["tags"] is not original["tags"]
    assert cloned["members"] is not original["members"]
    assert cloned["name"] == original["name"]
    assert cloned["tags"] == original["tags"]
    assert cloned["members"] == original["members"]

# 1. 为什么 b = a 不是复制？
#    因为 b = a 只是将 a 的引用赋值给 b，而不是创建一个新的对象。



# 2. == 和 is 的区别是什么？
#    == 是比较对象的内容是否相等，而 is 是比较对象的引用是否相同。

# 3. dict.copy() 为什么可能仍然污染原数据？
#    因为 dict.copy() 只是复制第一层，不复制嵌套对象。

#    例如，如果 dict 中�含 list 或 dict 等可变对象，那么复制后的对象的嵌套对象会指向原始对象的嵌套对象。
#    则会导致原始对象的嵌套对象被修改，从而污染原始数据。

# 4. 函数调用 add_tag(project, ...) 后，
#    为什么函数外的 project 会改变？
#    因为 add_tag_in_place() 是直接修改项目的标签列表，而不是返回一个新的项目结构体。
# 调用 add_tag
# 不是把整个字典复制一份传给函数；
# 只是把字典对象的内存引用地址赋值给形参 project
# append() 是列表原地修改（in‑place）方法，不产生新列表，直接修改内存里原来的列表。
# 因为内外共用同一个对象，函数外面的 project 自然看到变化。

# 5. deepcopy 能解决什么问题？
# deepcopy：递归遍历对象，把所有层级嵌套对象全部复制一份全新独立副本。
# 解决的核心问题：浅拷贝带来的「嵌套对象共享引用」
#    为什么又不应该无脑使用？
#    因为 deepcopy 会递归地复制所有嵌套对象，导致内存占用增加。
# deepcopy：递归遍历对象，把所有层级嵌套对象全部复制一份全新独立副本。
# 解决的核心问题：浅拷贝带来的「嵌套对象共享引用」
   



