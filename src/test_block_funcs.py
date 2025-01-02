import unittest
from block_funcs import markdown_to_block

class TestMarkdownToBlock(unittest.TestCase):
    def test_header_paragraph_list(self):
        md = """
# This is a header for a website

This is some paragraph with *italic text*

Another paragraph with some `code`

* This is a list
* with 2 items
"""

        self.assertEqual(
            [
                "# This is a header for a website",
                "This is some paragraph with *italic text*",
                "Another paragraph with some `code`",
                "* This is a list\n* with 2 items"
            ],
            markdown_to_block(md)
        )

    def test_excessive_whitespace(self):
        md = """
# This is another header






With excessive **white space!**


* How
* scary :(
"""
        self.assertEqual(
            [
                "# This is another header",
                "With excessive **white space!**",
                "* How\n* scary :("
            ],
            markdown_to_block(md)
        )

if __name__ == "__main__":
    unittest.main()