import pytest
from app.services import ProjectService 
from app.storage import InMemoryProjectStorage
from app.exceptions import ProjectNotFoundError

def test_service_creates_and_stores_project() -> None:
    storage = InMemoryProjectStorage()
    service = ProjectService(storage)

    project = service.create_project(
        "AI Workspace Lite",
        description="backend learning project",
    )

    projects = service.list_projects()

    assert project.name == "AI Workspace Lite"
    assert project.description == "backend learning project"
    assert projects == [project]

def test_service_keeps_multiple_projects() -> None:
    storage = InMemoryProjectStorage()
    service = ProjectService(storage)

    first = service.create_project("first")
    second = service.create_project("second")

    assert service.list_projects() == [first, second]

def test_different_storages_have_independent_state() -> None:
    storage_a = InMemoryProjectStorage()
    storage_b = InMemoryProjectStorage()

    service_a = ProjectService(storage_a)
    service_b = ProjectService(storage_b)

    service_a.create_project("only-a")

    assert len(service_a.list_projects()) == 1
    assert service_b.list_projects() == []

def test_list_projects_does_not_expose_storage_list() -> None:
    storage = InMemoryProjectStorage()
    service = ProjectService(storage)

    service.create_project("demo")

    projects = service.list_projects()
    projects.clear()

    assert len(service.list_projects()) == 1

def test_get_project_by_name_success() -> None:
    storage = InMemoryProjectStorage()
    service = ProjectService(storage)

    project = service.create_project("demo")

    assert service.get_project("demo") == project

def test_get_project_raises_when_project_not_found() -> None:
    storage = InMemoryProjectStorage()
    service = ProjectService(storage)

    with pytest.raises(
        ProjectNotFoundError,
        match="Project not found: missing",
    ):
        service.get_project("missing")
    

