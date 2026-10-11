from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.exceptions import (
    DbProjectAlreadyExistsError,
    DbProjectNotFoundError,
    TaskProjectWorkspaceMismatchError,
    UserAlreadyExistsError,
    UserNotFoundError,
    WorkspaceAlreadyExistsError,
    WorkspaceNotFoundError,
)
from app.m3_schemas import (
    DbProjectCreateRequest,
    DbProjectResponse,
    SortOrder,
    TaskCreateRequest,
    TaskListItemResponse,
    TaskListResponse,
    TaskResponse,
    TaskSortBy,
    UserCreateRequest,
    UserResponse,
    WorkspaceCreateRequest,
    WorkspaceResponse,
)
from app.services import (
    ProjectDbService,
    TaskDbService,
    UserDbService,
    WorkspaceDbService,
)


router = APIRouter()

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    body: UserCreateRequest,
    session: Session = Depends(get_session),
) -> UserResponse:
    service = UserDbService(session)

    try:
        user = service.create_user(
            username=body.username,
            email=body.email,
        )
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
    )

@router.post(
    "/workspaces",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workspace(
    body: WorkspaceCreateRequest,
    session: Session = Depends(get_session),
) -> WorkspaceResponse:
    service = WorkspaceDbService(session)

    try:
        workspace = service.create_workspace(
            owner_user_id=body.owner_user_id,
            name=body.name,
        )
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except WorkspaceAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return WorkspaceResponse(
        id=workspace.id,
        owner_user_id=workspace.owner_user_id,
        name=workspace.name,
    )

@router.post(
    "/workspaces/{workspace_id}/projects",
    response_model=DbProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    workspace_id: int,
    body: DbProjectCreateRequest,
    session: Session = Depends(get_session),
) -> DbProjectResponse:
    service = ProjectDbService(session)

    try:
        project = service.create_project(
            workspace_id=workspace_id,
            name=body.name,
            description=body.description,
        )
    except WorkspaceNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except DbProjectAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return DbProjectResponse(
        id=project.id,
        workspace_id=project.workspace_id,
        name=project.name,
        description=project.description,
    )

@router.post(
    "/workspaces/{workspace_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    workspace_id: int,
    body: TaskCreateRequest,
    session: Session = Depends(get_session),
) -> TaskResponse:
    service = TaskDbService(session)

    try:
        task = service.create_task(
            workspace_id=workspace_id,
            project_id=body.project_id,
            title=body.title,
            description=body.description,
            status=body.status,
        )
    except (
        WorkspaceNotFoundError,
        DbProjectNotFoundError,
    ) as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except TaskProjectWorkspaceMismatchError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return TaskResponse(
        id=task.id,
        workspace_id=task.workspace_id,
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        status=task.status,
    )

@router.get(
    "/workspaces/{workspace_id}/tasks",
    response_model=TaskListResponse,
)
def list_tasks(
    workspace_id: int,
    session: Session = Depends(get_session),
    task_status: Annotated[
        str | None,
        Query(alias="status"),
    ] = None,
    project_id: int | None = None,
    limit: Annotated[
        int,
        Query(ge=1, le=100),
    ] = 20,
    offset: Annotated[
        int,
        Query(ge=0),
    ] = 0,
    sort_by: TaskSortBy = "created_at",
    order: SortOrder = "desc",
    title_contains: Annotated[
        str | None,
        Query(min_length=1, max_length=200),
    ] = None,
    
) -> TaskListResponse:
    service = TaskDbService(session)

    try:
        items, total = service.list_tasks(
            workspace_id=workspace_id,
            status=task_status,
            project_id=project_id,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
            title_contains=title_contains,
        )
    except WorkspaceNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return TaskListResponse(
        items=[
            TaskListItemResponse(
                id=item.id,
                workspace_id=item.workspace_id,
                project_id=item.project_id,
                project_name=item.project_name,
                title=item.title,
                description=item.description,
                status=item.status,
                created_at=item.created_at,
            )
            for item in items
        ],
        total=total,
        limit=limit,
        offset=offset,
    )