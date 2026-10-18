from uuid import uuid4


class Task:
    def __init__(self, title, project_id, contributors=None):
        self.id = str(uuid4())[:8]
        self.title = title
        self.project_id = project_id
        if contributors is None:
            contributors = []
        self.contributors = contributors
        self.completed = False

    def complete(self):
        self.completed = True

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "project_id": self.project_id,
            "contributors": self.contributors,
            "completed": self.completed
        }