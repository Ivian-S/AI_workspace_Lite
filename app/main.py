# 修改：/project/app/main.py

import argparse
from pathlib import Path

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
