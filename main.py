import argparse
from rich.console import Console
from rich.table import Table

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import load, save

console = Console()


def find_user(name):
    return next(
        (u for u in load("users") if u["name"].lower() == name.lower()
         or u["id"] == name),
        None
    )


def run():
    parser = argparse.ArgumentParser(description="Project Tracker CLI")
    commands = parser.add_subparsers(dest="command", required=True)

    p = commands.add_parser("add-user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", default="")

    commands.add_parser("list-users")

    p = commands.add_parser("add-project")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")

    p = commands.add_parser("list-projects")
    p.add_argument("--user")

    p = commands.add_parser("search-projects")
    p.add_argument("--user", required=True)

    p = commands.add_parser("add-task")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--contributors", nargs="*", default=[])

    commands.add_parser("list-tasks")

    p = commands.add_parser("complete-task")
    p.add_argument("--task", required=True)

    args = parser.parse_args()

    try:
        if args.command == "add-user":
            user = User(args.name, args.email)
            users = load("users")
            users.append(user.to_dict())
            save("users", users)
            console.print(f"[green]User added: {user.name} ({user.id})[/green]")

        elif args.command == "list-users":
            table = Table(title="Users")
            table.add_column("ID")
            table.add_column("Name")
            table.add_column("Email")
            for u in load("users"):
                table.add_row(u["id"], u["name"], u["email"])
            console.print(table)

        elif args.command == "add-project":
            user = find_user(args.user)
            if not user:
                raise ValueError("User not found")
            project = Project(args.title, user["id"], args.description)
            projects = load("projects")
            projects.append(project.to_dict())
            save("projects", projects)
            console.print("[green]Project added.[/green]")

        elif args.command in ("list-projects", "search-projects"):
            projects = load("projects")
            if args.command == "search-projects" or args.user:
                name = args.user
                user = find_user(name)
                if not user:
                    raise ValueError("User not found")
                projects = [p for p in projects if p["user_id"] == user["id"]]

            table = Table(title="Projects")
            for column in ("ID", "Title", "Owner ID", "Description"):
                table.add_column(column)
            for p in projects:
                table.add_row(p["id"], p["title"], p["user_id"], p["description"])
            console.print(table)

        elif args.command == "add-task":
            project = next(
                (p for p in load("projects")
                 if p["title"].lower() == args.project.lower()
                 or p["id"] == args.project),
                None
            )
            if not project:
                raise ValueError("Project not found")

            contributors = []
            for name in args.contributors:
                user = find_user(name)
                if not user:
                    raise ValueError(f"User not found: {name}")
                contributors.append(user["id"])

            task = Task(args.title, project["id"], contributors)
            tasks = load("tasks")
            tasks.append(task.to_dict())
            save("tasks", tasks)
            console.print("[green]Task added.[/green]")

        elif args.command == "list-tasks":
            table = Table(title="Tasks")
            table.add_column("ID")
            table.add_column("Title")
            table.add_column("Project ID")
            table.add_column("Status")
            for t in load("tasks"):
                status = "Complete" if t["completed"] else "Pending"
                table.add_row(t["id"], t["title"], t["project_id"], status)
            console.print(table)

        elif args.command == "complete-task":
            tasks = load("tasks")
            task = next(
                (t for t in tasks
                 if t["id"] == args.task
                 or t["title"].lower() == args.task.lower()),
                None
            )
            if not task:
                raise ValueError("Task not found")
            task["completed"] = True
            save("tasks", tasks)
            console.print("[green]Task completed.[/green]")

    except (ValueError, KeyError) as error:
        console.print(f"[red]Error: {error}[/red]")


if __name__ == "__main__":
    run()