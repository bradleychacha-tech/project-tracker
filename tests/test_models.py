import unittest
from models.user import User
from models.project import Project
from models.task import Task


class TestModels(unittest.TestCase):
    def test_user(self):
        user = User("Brad", "brad@example.com")
        self.assertEqual(user.name, "Brad")
        self.assertTrue(user.to_dict()["id"])

    def test_project(self):
        project = Project("My Project", "user123")
        self.assertEqual(project.title, "My Project")

    def test_task(self):
        task = Task("Write code", "project123")
        task.complete()
        self.assertTrue(task.completed)


if __name__ == "__main__":
    unittest.main()