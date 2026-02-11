import unittest

from main import markdown_to_blocks

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(blocks,
                        [
                            "# This is a heading",
                            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                            """- This is the first list item in a list block
- This is a list item
- This is another list item""",
])

    def test_markdown_to_blocks(self):
        markdown = """
    This is a block with extra white spaces
and only one new line.    

And this is a normal block"""
        
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(blocks,
                         [f"This is a block with extra white spaces\nand only one new line.""",
                          "And this is a normal block"])

if __name__ == "__main__":
    unittest.main()
