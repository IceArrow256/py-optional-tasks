import unittest
import src.optional_tasks.optional_tasks as optional_tasks


class TestOptionalTasks(unittest.TestCase):
    def test_function(self):
        self.assertEqual(optional_tasks.function(), 42)
