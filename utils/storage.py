import json
from pathlib import Path

DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"
DATA_FOLDER.mkdir(exist_ok=True)


def load(file_name):
    file_path = DATA_FOLDER / f"{file_name}.json"
    if not file_path.exists():
        file_path.write_text("[]")
    return json.loads(file_path.read_text())


def save(file_name, items):
    file_path = DATA_FOLDER / f"{file_name}.json"
    file_path.write_text(json.dumps(items, indent=4))