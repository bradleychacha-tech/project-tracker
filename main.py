import argparse
from rich.console import Console
from rich.table import Table

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import load, save

console = Console()


def find_item(items, text, name_field):
    for item in items:
        if item["id"] == text or item[name_field].lower() == text.lower():
            return item
    return None


def find_user(name):
    return find_item(load("users"), name, "name")


def add_user(args):
    user = User(args.name, args.email)
    users = load("users")
    users.append(user.to_dict())
    save("users", users)
    console.print(f"[green]User added: {user.name} ({user.id})[/green]")


def list_users():
    table = Table(title="Users")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Email")
    for user in load("users"):
        table.add_row(user["id"], user["name"], user["email"])
    console.print(table)


def add_project(args):
    user = find_user(args.user)
    if not user:
        raise ValueError("User not found")
    project = Project(args.title, user["id"], args.description)
    projects = load("projects")
    projects.append(project.to_dict())
    save("projects", projects)
    console.print("[green]Project added.[/green]")


def list_projects(args):
    projects = load("projects")
    if args.user:
        user = find_user(args.user)
        if not user:
            raise ValueError("User not found")
        user_projects = []
        for project in projects:
            if project["user_id"] == user["id"]:
                user_projects.append(project)
        projects = user_projects

    table = Table(title="Projects")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Owner ID")
    table.add_column("Description")
    for project in projects:
        table.add_row(
            project["id"], project["title"],
            project["user_id"], project["description"]
        )
    console.print(table)


def add_task(args):
    project = find_item(load("projects"), args.project, "title")
    if not project:
        raise ValueError("Project not found")

    contributor_ids = []
    for name in args.contributors:
        user = find_user(name)
        if not user:
            raise ValueError(f"User not found: {name}")
        contributor_ids.append(user["id"])

    task = Task(args.title, project["id"], contributor_ids)
    tasks = load("tasks")
    tasks.append(task.to_dict())
    save("tasks", tasks)
    console.print("[green]Task added.[/green]")


def list_tasks():
    table = Table(title="Tasks")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Project ID")
    table.add_column("Status")
    for task in load("tasks"):
        status = "Complete" if task["completed"] else "Pending"
        table.add_row(task["id"], task["title"], task["project_id"], status)
    console.print(table)


def complete_task(args):
    tasks = load("tasks")
    task = find_item(tasks, args.task, "title")
    if not task:
        raise ValueError("Task not found")
    task["completed"] = True
    save("tasks", tasks)
    console.print("[green]Task completed.[/green]")


def create_parser():
    parser = argparse.ArgumentParser(description="Project Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("--name", required=True, help="Name of the user")
    add_user_parser.add_argument("--email", default="", help="Email of the user")

    subparsers.add_parser("list-users", help="Show all users")

    add_project_parser = subparsers.add_parser(
        "add-project", help="Add a project for a user"
    )
    add_project_parser.add_argument(
        "--user", required=True, help="Name or ID of the project owner"
    )
    add_project_parser.add_argument(
        "--title", required=True, help="Title of the project"
    )
    add_project_parser.add_argument(
        "--description", default="", help="Description of the project"
    )

    list_projects_parser = subparsers.add_parser(
        "list-projects", help="Show all projects, or only one user's projects"
    )
    list_projects_parser.add_argument(
        "--user", help="Name or ID of the user to filter by"
    )

    search_projects_parser = subparsers.add_parser(
        "search-projects", help="Show the projects of one user"
    )
    search_projects_parser.add_argument(
        "--user", required=True, help="Name or ID of the user"
    )

    add_task_parser = subparsers.add_parser(
        "add-task", help="Add a task to a project"
    )
    add_task_parser.add_argument(
        "--project", required=True, help="Title or ID of the project"
    )
    add_task_parser.add_argument(
        "--title", required=True, help="Title of the task"
    )
    add_task_parser.add_argument(
        "--contributors", nargs="*", default=[],
        help="Names or IDs of users who work on the task"
    )

    subparsers.add_parser("list-tasks", help="Show all tasks and their status")

    complete_task_parser = subparsers.add_parser(
        "complete-task", help="Mark a task as complete"
    )
    complete_task_parser.add_argument(
        "--task", required=True, help="Title or ID of the task"
    )

    return parser


def run():
    args = create_parser().parse_args()

    try:
        if args.command == "add-user":
            add_user(args)
        elif args.command == "list-users":
            list_users()
        elif args.command == "add-project":
            add_project(args)
        elif args.command in ("list-projects", "search-projects"):
            list_projects(args)
        elif args.command == "add-task":
            add_task(args)
        elif args.command == "list-tasks":
            list_tasks()
        elif args.command == "complete-task":
            complete_task(args)
    except (ValueError, KeyError) as error:
        console.print(f"[red]Error: {error}[/red]")


if __name__ == "__main__":
    run()