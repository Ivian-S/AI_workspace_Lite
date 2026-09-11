from fastapi import FastAPI

from app.main import app

def test_fastapi_app_exists() -> None:
    assert isinstance(app, FastAPI)

def test_root_route_is_in_openapi_schema() -> None:
    openapi_schema = app.openapi()

    assert "/" in openapi_schema["paths"]
    assert "get" in openapi_schema["paths"]["/"]