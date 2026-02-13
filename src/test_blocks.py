
import unittest
from blocks import BlockType, markdown_to_blocks, block_to_block_type

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

        def test_markdown_to_blocks_with_whitespace(self):
                markdown = """
    This is a block with extra white spaces
and only one new line.    

And this is a normal block"""
                blocks = markdown_to_blocks(markdown)
                self.assertEqual(blocks,
                                ["This is a block with extra white spaces\nand only one new line.",
                                 "And this is a normal block"])

        def test_block_to_block_type(self):
                b1 = "## heading text"
                b2 = """```
code
block ```"""
                b3 = """>Text1
> text2"""
                b4 = """- first item
- second item
- third item"""
                b5 = """1. first item
2. second item
3. third item"""
                b6 = """### heading text
>quoted text"""

                self.assertEqual(block_to_block_type(b1), BlockType.HEADING)
                self.assertEqual(block_to_block_type(b2), BlockType.CODE)
                self.assertEqual(block_to_block_type(b3), BlockType.QUOTE)
                self.assertEqual(block_to_block_type(b4), BlockType.UNORDERED_LIST)
                self.assertEqual(block_to_block_type(b5), BlockType.ORDERED_LIST)
                self.assertEqual(block_to_block_type(b6), BlockType.PARAGRAPH)

        def test_block_to_block_type_edge(self):
                b1 = "abc## wrong heading"
                b2 = "```wrongcloser``"
                b3 = """-no space
-on new lines"""
                b4 = """1. wrong
3. enumeration
2. example"""

                self.assertEqual(block_to_block_type(b1), BlockType.PARAGRAPH)
                self.assertEqual(block_to_block_type(b2), BlockType.PARAGRAPH)
                self.assertEqual(block_to_block_type(b3), BlockType.PARAGRAPH)
                self.assertEqual(block_to_block_type(b4), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()

