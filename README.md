# Project Tracker CLI

A simple command-line app for managing users, projects, and tasks. It saves the data in JSON files.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Usage

Run commands from the project folder:

```bash
python main.py <command> [options]
```

Commands:

- `add-user --name NAME`
- `list-users`
- `add-project --user USER --title TITLE`
- `list-projects`
- `search-projects --user USER`
- `add-task --project PROJECT --title TITLE`
- `list-tasks`
- `complete-task --task TASK`

Optional: `--email` for `add-user`, `--description` for `add-project`, `--user` for `list-projects`, and `--contributors` for `add-task`.

Use `python main.py --help` to see the help for all commands.

### Examples

```bash
python main.py add-user --name Brad --email brad@example.com
python main.py add-project --user Brad --title Website
python main.py add-task --project Website --title "Build homepage" --contributors Brad
python main.py complete-task --task "Build homepage"
```

## Running Tests

```bash
python -m unittest
```
