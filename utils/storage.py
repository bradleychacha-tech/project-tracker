import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
DATA.mkdir(exist_ok=True)


def load(name):
    path = DATA / f"{name}.json"
    if not path.exists():
        path.write_text("[]")
    return json.loads(path.read_text())


def save(name, items):
    path = DATA / f"{name}.json"
    path.write_text(json.dumps(items, indent=4))