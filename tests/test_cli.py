# 新增: 测试 CLI 命令

from pathlib import Path

from app.main import main
from app.storage import JsonProjectStorage

def test_cli_create_project(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "projects.json"

    exit_code = main(
        [
            "create",
            "demo",
            "--description",
            "backend project",
            "--tag",
            "python",
            "--member",
            "alice",
        ],
        storage_path=file_path,
    )

    storage = JsonProjectStorage(file_path)
    project = storage.get_by_name("demo")

    assert exit_code == 0
    assert project is not None
    assert project.description == "backend project"
    assert project.tags == ["python"]
    assert project.members == ["alice"]

def test_cli_list_projects(
    tmp_path: Path,
    capsys,
) -> None:
    file_path = tmp_path / "projects.json"

    main(
        ["create","demo"],
        storage_path=file_path,
    )

    exit_code = main(
        ["list"],
        storage_path=file_path,
    )

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "demo" in output


def test_cli_get_missing_project_returns_error(
    tmp_path: Path,
    capsys,
) -> None:
    exit_code = main(
        ["get", "missing"],
        storage_path=tmp_path / "projects.json",
    )

    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Project not found: missing" in output


def test_cli_update_project(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "projects.json"

    main(
        ["create", "demo"],
        storage_path=file_path,
    )

    exit_code = main(
        [
            "update",
            "demo",
            "--name",
            "demo-v2",
            "--description",
            "updated",
            "--tag",
            "json",
            "--member",
            "alice",
        ],
        storage_path=file_path,
    )

    storage = JsonProjectStorage(file_path)

    assert exit_code == 0
    assert storage.get_by_name("demo") is None

    project = storage.get_by_name("demo-v2")

    assert project is not None
    assert project.description == "updated"
    assert project.tags == ["json"]
    assert project.members == ["alice"]

def test_cli_delete_project(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "projects.json"

    main(
        ["create", "demo"],
        storage_path=file_path,
    )

    exit_code = main(
        ["delete", "demo"],
        storage_path=file_path,
    )

    storage = JsonProjectStorage(file_path)

    assert exit_code == 0
    assert storage.get_by_name("demo") is None


def test_cli_create_duplicate_project_returns_error(
    tmp_path: Path,
    capsys,
) -> None:
    file_path = tmp_path / "projects.json"

    first_exit_code = main(
        ["create", "demo"],
        storage_path=file_path,
    )

    second_exit_code = main(
        ["create", "demo"],
        storage_path=file_path,
    )

    output = capsys.readouterr().out

    assert first_exit_code == 0
    assert second_exit_code == 1
    assert "Project already exists: demo" in output


def test_cli_list_invalid_json_returns_storage_error(
    tmp_path: Path,
    capsys,
) -> None:
    file_path = tmp_path / "projects.json"
    file_path.write_text(
        "{invalid json",
        encoding="utf-8",
    )

    exit_code = main(
        ["list"],
        storage_path=file_path,
    )

    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Invalid project storage data" in output