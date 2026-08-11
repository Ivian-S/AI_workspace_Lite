from unicodedata import name

from app import project_state
from app.models import Project
from app.project_state import (
    add_tag_in_place,
    create_project,
    with_tag,
    clone_project,
)

def test_assignment_share_same_project():
    project_a = create_project("AI Workspace Lite")
    project_b = project_a
    project_b.name += "Changed"
    assert project_a is project_b

def test_in_place_operation_changes_original_project():
    project = create_project("Workspace")

    add_tag_in_place(project, "python")
    print(project)

    #内容一致，但是用is判断是否是同一个对象，结果是False
    assert project.tags == ["python"]

def test_with_tag_does_not_change_original_project():
    original = create_project("Workspace")

    updated = with_tag(original, "python")

    assert original.tags == []
    assert updated.tags == ["python"]

    assert original is not updated
    assert original.tags is not updated.tags


def test_create_project():
    project_a = create_project("A")
    project_b = create_project("B")

    assert project_a.members is not project_b.members

def test_shallow_copy_shares_nested_members() -> None:
    original = {
        "members": [],    
    }
    copied = original.copy()
    copied["members"].append("member")

    assert original["members"] == copied["members"]


def test_clone_project():
    original = create_project("original")
    cloned = clone_project(original)

    assert original is not cloned
    assert cloned.tags is not original.tags
    assert cloned.members is not original.members
    assert cloned.name == original.name
    assert cloned.tags == original.tags
    assert cloned.members == original.members

#M1-T03相关测试
def test_create_project_returns_project() -> None:
    project = create_project("demo")

    #isinstance(obj, 类型)：Python 内置函数，判断 obj 是否是该类 / 子类的实例；
    assert isinstance(project, Project)
    assert project.name == "demo"

def test_projects_do_not_share_lists() -> None:
    first = Project(name="first")
    second = Project(name="second")
    first.tags.append("python")

    assert first.tags == ["python"]
    assert second.tags == []

def test_create_project__copies_input_tags() -> None:
    tags = ["python"]
    project = create_project("demo", tags=tags)
    tags.append("docker")

    assert tags == ["python", "docker"]
    assert project.tags == ["python"]


def test_create_project_description() -> None:
    project = create_project("demo", "test_description")
    project2 = create_project("demo")
    
    
    assert project.description == "test_description"
    assert project2.description is None

