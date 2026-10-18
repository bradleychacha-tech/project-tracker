from uuid import uuid4


class Project:
    def __init__(self, title, user_id, description=""):
        self.id = str(uuid4())[:8]
        self.title = title
        self.user_id = user_id
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "description": self.description
        }