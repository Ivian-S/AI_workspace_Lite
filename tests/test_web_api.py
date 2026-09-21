from collections.abc import Iterator

import pytest

from fastapi.testclient import TestClient

import app.main as main_module

from app.services import ProjectService
from app.storage import InMemoryProjectStorage

@pytest.fixture
def client(
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[TestClient]:
    test_service = ProjectService(
        InMemoryProjectStorage()
    )

    monkeypatch.setattr(
        main_module,
        "web_project_service",
        test_service,
    )

    with TestClient(
        main_module.app
    ) as test_client:
        yield test_client

def test_projects_start_empty(
    client: TestClient,
) -> None:
    response = client.get(
        "/projects"
    )

    assert response.status_code == 200
    assert response.json() == []

def test_create_project(
    client: TestClient,
) -> None:
    response = client.post(
        "/projects",
        json={
            "name": "alpha",
            "description": "demo",
            "tags": ["fastapi"],
            "members": ["ivian"],
        },
    )

    assert response.status_code == 201

    assert response.json() == {
        "name": "alpha",
        "description": "demo",
        "tags": ["fastapi"],
        "members": ["ivian"],
    }

def test_list_projects(
    client: TestClient,
) -> None:
    client.post(
        "/projects",
        json={
            "name": "alpha",
        },
    )

    client.post(
        "/projects",
        json={
            "name": "beta",
        },
    )

    response = client.get(
        "/projects"
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "name": "alpha",
            "description": None,
            "tags": [],
            "members": [],
        },
        {
            "name": "beta",
            "description": None,
            "tags": [],
            "members": [],
        },
    ]


def test_get_project(
    client: TestClient,
) -> None:
    client.post(
        "/projects",
        json={
            "name": "alpha",
            "description": "demo",
        },
    )

    response = client.get(
        "/projects/alpha"
    )

    assert response.status_code == 200

    assert response.json() == {
        "name": "alpha",
        "description": "demo",
        "tags": [],
        "members": [],
    }


def test_patch_project_preserves_unsent_fields(
    client: TestClient,
) -> None:
    client.post(
        "/projects",
        json={
            "name": "alpha",
            "description": "before",
            "tags": ["python"],
            "members": ["alice"],
        },
    )

    response = client.patch(
        "/projects/alpha",
        json={
            "description": "after",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "name": "alpha",
        "description": "after",
        "tags": ["python"],
        "members": ["alice"],
    }

def test_delete_project(
    client: TestClient,
) -> None:
    client.post(
        "/projects",
        json={
            "name": "alpha",
        },
    )

    delete_response = client.delete(
        "/projects/alpha"
    )

    assert (
        delete_response.status_code
        == 204
    )

    assert delete_response.content == b""

    get_response = client.get(
        "/projects/alpha"
    )

    assert get_response.status_code == 404

def test_missing_project_returns_404(
    client: TestClient,
) -> None:
    response = client.get(
        "/projects/missing"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": (
            "Project not found: missing"
        )
    }

def test_duplicate_project_returns_409(
    client: TestClient,
) -> None:
    client.post(
        "/projects",
        json={
            "name": "alpha",
        },
    )

    response = client.post(
        "/projects",
        json={
            "name": "alpha",
        },
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": (
            "Project already exists: alpha"
        )
    }

def test_patch_rename_conflict_returns_409(
    client: TestClient,
) -> None:
    client.post(
        "/projects",
        json={
            "name": "alpha",
        },
    )

    client.post(
        "/projects",
        json={
            "name": "beta",
        },
    )

    response = client.patch(
        "/projects/alpha",
        json={
            "name": "beta",
        },
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": (
            "Project already exists: beta"
        )
    }

def test_invalid_project_body_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        "/projects",
        json={
            "name": "",
        },
    )

    assert response.status_code == 422

    detail = response.json()[
        "detail"
    ]

    assert detail[0]["loc"] == [
        "body",
        "name",
    ]

    assert (
        detail[0]["type"]
        == "string_too_short"
    )