from uuid import uuid4


class Person:
    def __init__(self, name):
        self._name = name.strip()
        if not self._name:
            raise ValueError("Name is required")

    @property
    def name(self):
        return self._name


class User(Person):
    def __init__(self, name, email=""):
        super().__init__(name)
        self.id = str(uuid4())[:8]
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }