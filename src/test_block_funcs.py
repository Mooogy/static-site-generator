import unittest
from block_funcs import markdown_to_block, block_to_block_type, BLOCKTYPE

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

class TestBlockToBlockType(unittest.TestCase):
    def test__block_code(self):
        block = "```\nhi look at me epic python code!\npython code here\nreturn 0\n```"

        self.assertEqual(BLOCKTYPE.CODE, block_to_block_type(block))

    def test_block_quote(self):
        block = ">hi look at me epic quote!\n>quote here\n>quote"
        invalid = ">missing a\n>quote identifier\non the last line"

        self.assertEqual(BLOCKTYPE.QUOTE, block_to_block_type(block))
        self.assertEqual(BLOCKTYPE.PARAGRAPH, block_to_block_type(invalid))
    
    def test_block_ulist(self):
        block = "* hi look at me epic quote!\n* quote here\n* quote"
        invalid ="* hiii\nim missing something!"

        self.assertEqual(BLOCKTYPE.ULIST, block_to_block_type(block))
        self.assertEqual(BLOCKTYPE.PARAGRAPH, block_to_block_type(invalid))
    
    def test_block_olist(self):
        block = "1. hi look at me epic quote!\n2. quote here\n3. quote"
        invalid ="1. hiii\nim missing something!"

        self.assertEqual(BLOCKTYPE.OLIST, block_to_block_type(block))
        self.assertEqual(BLOCKTYPE.PARAGRAPH, block_to_block_type(invalid))
    
    def test_block_header(self):
        block1 = "## Look at this heading!"
        block2 = "#### Smaller heading!"

        self.assertEqual(BLOCKTYPE.HEADING, block_to_block_type(block1))
        self.assertEqual(BLOCKTYPE.HEADING, block_to_block_type(block2))
    
    def test_block_paragraph(self):
        block = "just a normal lil guy"

        self.assertEqual(BLOCKTYPE.PARAGRAPH, block_to_block_type(block))

if __name__ == "__main__":
    unittest.main()