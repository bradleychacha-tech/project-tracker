from uuid import uuid4


class Task:
    def __init__(self, title, project_id, contributors=None):
        self.id = str(uuid4())[:8]
        self.title = title
        self.project_id = project_id
        self.contributors = contributors or []
        self.completed = False

    def complete(self):
        self.completed = True

    def to_dict(self):
        return vars(self)