import unittest
import src.python_app.python_app as python_app


class TestPythonApp(unittest.TestCase):
    def test_function(self):
        self.assertEqual(python_app.function(), 42)
