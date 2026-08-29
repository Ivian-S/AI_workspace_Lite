# 新增：tests/test_json_storage.py
from pathlib import Path

import pytest

from app.exceptions import ProjectStorageDataError
from app.models import Project
from app.storage import JsonProjectStorage

def test_missing_json_file_returns_empty_list(
    tmp_path: Path,
) -> None:
    storage = JsonProjectStorage(
        tmp_path / "projects.json"
    )

    assert storage.list_all() == []

def test_project_survives_new_storage_instance(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "projects.json"

    storage = JsonProjectStorage(file_path)
    storage.save(Project(name="demo"))

    reload_storage = JsonProjectStorage(file_path)
    
    project = reload_storage.get_by_name("demo")

    assert project is not None
    assert project.name == "demo"

def test_empty_json_file_returns_empty_list(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "projects.json"
    file_path.write_text("", encoding="utf-8")
    
    storage = JsonProjectStorage(file_path)

    assert storage.list_all() == []

def test_invalid_json_raises_storage_data_error(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "projects.json"
    file_path.write_text(
        "{invalid json",
        encoding="utf-8",
    )
    storage = JsonProjectStorage(file_path)
    
    with pytest.raises(ProjectStorageDataError):
        storage.list_all()

# update后重新实例化仍能读到新值
def test_update_project_survives_new_storage_instance(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "projects.json"

    storage = JsonProjectStorage(file_path)
    storage.save(Project(name="demo"))

    updated_project = Project(name="updated_demo")
    storage.update_by_name("demo", updated_project)

    reload_storage = JsonProjectStorage(file_path)
    project = reload_storage.get_by_name("updated_demo")

    assert project is not None
    assert project.name == "updated_demo"

def test_delete_project_removes_from_storage(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "projects.json"

    storage = JsonProjectStorage(file_path)
    storage.save(Project(name="demo"))

    storage.delete_by_name("demo")

    reload_storage = JsonProjectStorage(file_path)
    project = reload_storage.get_by_name("demo")

    assert project is None

def test_project_all_fields_survive_reload(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "projects.json"

    storage = JsonProjectStorage(file_path)
    storage.save(
        Project(
            name="demo",
            description="backend project",
            tags=["python", "json"],
            members=["alice"],
        )
    )

    reloaded_storage = JsonProjectStorage(file_path)
    project = reloaded_storage.get_by_name("demo")

    assert project is not None
    assert project.description == "backend project"
    assert project.tags == ["python", "json"]
    assert project.members == ["alice"]
