import unittest
from main import extract_title
class TestRegex(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello  "
        title = extract_title(md)
        self.assertEqual(title, "Hello")
        md = "# Actual \n# Fake"
        title = extract_title(md)
        self.assertEqual(title, "Actual")

if __name__ == "__main__":
    unittest.main()