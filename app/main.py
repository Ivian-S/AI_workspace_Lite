# 修改：/project/app/main.py
import logging
import time

from collections.abc import Awaitable,Callable

import argparse
from pathlib import Path

from fastapi import FastAPI,Request,status,Response
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app import APP_NAME
from app.exceptions import(
    ProjectNotFoundError,
    ProjectAlreadyExistsError,
    ProjectStorageDataError,
)

from app.info import APP_VERSION
from app.models import Project
from app.services import ProjectService
from app.storage import JsonProjectStorage

DEFAULT_STORAGE_PATH = Path("data/projects.json")
logger = logging.getLogger("uvicorn.error")

#新增：Request Body Schema
class ProjectRequestBody(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    members: list[str] = Field(default_factory=list)


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
    )
    description: str | None = None
    tags: list[str] | None = None
    members: list[str] | None = None

class ProjectResponse(BaseModel):
    name: str
    description: str | None = None
    tags: list[str]
    members: list[str]

# 新增：FastAPI application instance
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)



@app.middleware("http")
async def log_http_request(
    request: Request,
    call_next: Callable[
        [Request],
        Awaitable[Response],
    ],
) -> Response:
    start_time = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception as exc:
        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.error(
            (
                "request_failed "
                "method=%s "
                "path=%s "
                "duration_ms=%.2f "
                "error_type=%s"
            ),
            request.method,
            request.url.path,
            duration_ms,
            type(exc).__name__,
        )

        raise

    duration_ms = (
        time.perf_counter() - start_time
    ) * 1000

    logger.info(
        (
            "request_complete "
            "method=%s "
            "path=%s "
            "status=%s "
            "duration_ms=%.2f"
        ),
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    return response

@app.exception_handler(ProjectNotFoundError)
async def project_not_found_exception_handler(
    request: Request,
    exc: ProjectNotFoundError,
) -> JSONResponse:
    logger.warning(
        (
            "business_error "
            "type=%s "
            "method=%s "
            "path=%s "
            "detail=%s"
        ),
        type(exc).__name__,
        request.method,
        request.url.path,
        str(exc),
    )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
        },
    )


@app.exception_handler(ProjectAlreadyExistsError)
async def project_already_exists_exception_handler(
    request: Request,
    exc: ProjectAlreadyExistsError,
) -> JSONResponse:
    logger.warning(
        (
            "business_error "
            "type=%s "
            "method=%s "
            "path=%s "
            "detail=%s"
        ),
        type(exc).__name__,
        request.method,
        request.url.path,
        str(exc),
    )

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
        },
    )

@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> Response:
    errors = [
        {
            "loc": ".".join(
                str(part)
                for part in error["loc"]
            ),
            "type": error["type"],
            "msg": error["msg"],
        }
        for error in exc.errors()
    ]

    logger.warning(
        (
            "validation_error "
            "method=%s "
            "path=%s "
            "errors=%s"
        ),
        request.method,
        request.url.path,
        errors,
    )

    return await (
        request_validation_exception_handler(
            request,
            exc,
        )
    )

web_project_service = ProjectService(
    storage=JsonProjectStorage(DEFAULT_STORAGE_PATH),
)

def project_to_response(project: Project) -> ProjectResponse:
    return ProjectResponse(
        name=project.name,
        description=project.description,
        tags=list(project.tags),
        members=list(project.members),
    )

@app.post(
        "/projects",
        response_model=ProjectResponse,
        status_code=status.HTTP_201_CREATED,
)
def create_project_api(
    body: ProjectRequestBody,
) -> ProjectResponse:
    project = web_project_service.create_project(
        name=body.name,
        description=body.description,
        tags=body.tags,
        members=body.members,
    )
    return project_to_response(project)

@app.get(
        "/projects",
        response_model=list[ProjectResponse],
)
def list_projects_api() -> list[ProjectResponse]:
    projects = web_project_service.list_projects()
    return [project_to_response(project) for project in projects]


@app.get(
        "/projects/{project_name}",
        response_model=ProjectResponse,
)
def get_project_api(
    project_name: str,
) -> ProjectResponse:
    project = web_project_service.get_project(project_name)
    return project_to_response(project)


@app.patch(
    "/projects/{project_name}",
    response_model=ProjectResponse,
)
def update_project_api(
    project_name: str,
    body: ProjectUpdateRequest,
) -> ProjectResponse:
    current_project = (
        web_project_service.get_project(
            project_name
        )
    )

    updates = body.model_dump(
        exclude_unset=True
    )

    new_name = (
        current_project.name
        if body.name is None
        else body.name
    )

    new_description = (
        current_project.description
        if "description" not in updates
        else body.description
    )

    new_tags = (
        current_project.tags
        if body.tags is None
        else body.tags
    )

    new_members = (
        current_project.members
        if body.members is None
        else body.members
    )

    updated_project = (
        web_project_service.update_project(
            project_name,
            name=new_name,
            description=new_description,
            tags=new_tags,
            members=new_members,
        )
    )

    return project_to_response(
        updated_project
    )

@app.delete(
    "/projects/{project_name}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_api(
    project_name: str,
) -> None:
    web_project_service.delete_project(
        project_name
    )


# 新增：M2-T02 只验证最小 HTTP 路由
@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "ok",
    }

# 新增：M2-T03 Path / Query 参数学习路由
@app.get("/parameter-demo/{project_name}")
def read_parameter_demo(
    project_name: str,
    limit: int = 10,
    include_archived: bool = False,
    offset: int = 0,
)-> dict[str, str | int | bool | int]:
    return {
        "project_name": project_name,
        "limit": limit,
        "include_archived": include_archived,
        "offset": offset,
    }

# 新增：M2-T04 Request Body 参数学习路由
@app.post("/request-body-demo")
def read_request_body_demo(
    project: ProjectRequestBody,
) -> dict[str, object]:
    return project.model_dump()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="AI-Workspace-Lite",
        description=APP_NAME,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"{APP_NAME} {APP_VERSION}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    #create
    create_parser = subparsers.add_parser(
        "create",
        help="Create a project",
    )

    create_parser.add_argument("name")
    create_parser.add_argument("--description")
    create_parser.add_argument(
        "--tag",
        action="append",
        default=[],
        dest="tags",
    )
    create_parser.add_argument(
        "--member",
        action="append",
        default=[],
        dest="members",
    )

    #list
    subparsers.add_parser(
        "list",
        help="List projects",
    )


    #get
    get_parser = subparsers.add_parser(
        "get",
        help="Get a project",
    )
    get_parser.add_argument("name")

    #update
    update_parser = subparsers.add_parser(
        "update",
        help="Replace a project",
    )
    update_parser.add_argument("current_name")
    update_parser.add_argument(
        "--name",
        required=True,
    )
    update_parser.add_argument("--description")
    update_parser.add_argument(
        "--tag",
        action="append",
        default=[],
        dest="tags",
    )
    update_parser.add_argument(
        "--member",
        action="append",
        default=[],
        dest="members",
    )

    #delete
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a project",
    )
    delete_parser.add_argument("name")

    return parser

def format_project(project: Project) -> str:
    description = (
        project.description
        if project.description is not None
        else "-"
    )

    tags = ", ".join(project.tags) or "-"
    members = ", ".join(project.members) or "-"

    return (
        f"Name: {project.name}\n"
        f"Description: {description}\n"
        f"Tags: {tags}\n"
        f"Members: {members}\n"
    )

def run_command(
    args: argparse.Namespace,
    service: ProjectService,
) -> None:
    if args.command == "create":
        project = service.create_project(
            name=args.name,
            description=args.description,
            tags=args.tags,
            members=args.members,
        )
        print("Project created.")
        print(format_project(project))
        return

    if args.command == "list":
        projects = service.list_projects()

        if not projects:
            print("No projects.")
            return

        for index, project in enumerate(
            projects,
            start=1,
        ):
            print(f"[{index}]")
            print(format_project(project))
        return

    if args.command == "get":
        project = service.get_project(args.name)
        print(format_project(project))
        return

    if args.command == "update":
        project = service.update_project(
            args.current_name,
            name=args.name,
            description=args.description,
            tags=args.tags,
            members=args.members,
        )
        print("Project updated.")
        print(format_project(project))
        return

    if args.command == "delete":
        service.delete_project(args.name)
        print(f"Project deleted: {args.name}")
        return

    raise ValueError(f"Unsupported command: {args.command}")

def main(
    argv: list[str] | None = None,
    *,
    storage_path: str |Path = DEFAULT_STORAGE_PATH,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    storage = JsonProjectStorage(storage_path)
    service = ProjectService(storage)
    try:
        run_command(args, service)
    except (
        ProjectNotFoundError,
        ProjectAlreadyExistsError,
        ProjectStorageDataError,
    ) as exc:
        print(f"Error: {exc}")
        return 1
    
    except OSError as exc:
        print(f"Storage error: {exc}")
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
