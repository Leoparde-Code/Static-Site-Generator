import unittest
from gen_content import extract_title

class TestGenContent(unittest.TestCase):

    def test_normal(self):
        markdown = "# This is a heading\nThis is not a heading"

        self.assertEqual(extract_title(markdown), "This is a heading")

    def test_heading_2(self):
        markdown = "## This is a heading 2\nThis is not a heading"

        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_heading_2_before_1(self):
        markdown = "## This is a heading 2 \n# This is a heading 1"

        self.assertEqual(extract_title(markdown), "This is a heading 1")

    def test_more_whitespace(self):
        markdown = "#    This is a heading    \nThis is not a heading"

        self.assertEqual(extract_title(markdown), "This is a heading")
