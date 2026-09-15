from fastapi import FastAPI

from app.main import app

def test_fastapi_app_exists() -> None:
    assert isinstance(app, FastAPI)

def test_root_route_is_in_openapi_schema() -> None:
    openapi_schema = app.openapi()

    assert "/" in openapi_schema["paths"]
    assert "get" in openapi_schema["paths"]["/"]

# 新增：确认FastAPI 正确识别 Path / Query 参数及其类型
def test_parameter_demo_is_in_openapi_schema() -> None:
    openapi_schema = app.openapi()

    operation = openapi_schema["paths"][
        "/parameter-demo/{project_name}"
    ]["get"]

    parameters = {
        parameter["name"]: parameter for parameter in operation["parameters"]
    }

    assert parameters["project_name"]["in"] == "path"
    assert parameters["project_name"]["schema"]["type"] == "string"

    assert parameters["limit"]["in"] == "query"
    assert parameters["limit"]["schema"]["type"] == "integer"
    assert parameters["limit"]["schema"]["default"] == 10

    assert parameters["include_archived"]["in"] == "query"
    assert parameters["include_archived"]["schema"]["type"] == "boolean"
    assert parameters["include_archived"]["schema"]["default"] is False

    assert parameters["offset"]["in"] == "query"
    assert parameters["offset"]["schema"]["type"] == "integer"
    assert parameters["offset"]["schema"]["default"] == 0

# 新增：确认 FastAPI 正确识别 Pydantic Request Body
def test_request_body_demo_is_in_openapi_schema() -> None:
    openapi_schema = app.openapi()

    operation = openapi_schema["paths"][
        "/request-body-demo"
    ]["post"]

    request_body = operation["requestBody"]

    assert request_body["required"] is True

    body_ref = request_body[
        "content"
    ]["application/json"]["schema"]["$ref"]

    schema_name = body_ref.rsplit("/", 1)[-1]

    body_schema = openapi_schema[
        "components"
    ]["schemas"][schema_name]

    assert "name" in body_schema["required"]

    assert (
        body_schema["properties"]["name"]["type"]
        == "string"
    )

    assert (
        body_schema["properties"]["name"]["minLength"]
        == 1
    )

    assert (
        body_schema["properties"]["tags"]["type"]
        == "array"
    )

    assert (
        body_schema["properties"]["members"]["type"]
        == "array"
    )
