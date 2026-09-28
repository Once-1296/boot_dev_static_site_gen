import unittest
from blocks import markdown_to_blocks, block_to_blocktype, BlockType, markdown_to_html_node

class TestRegex(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    
    
    
    
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def checkBlockType(self):
        block = "# heading normal"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
        block = "## heading normal"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
        block = "### heading normal"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
        block = "#### heading normal"  
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING) 
        block = "##### heading normal"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
        block = "###### heading normal"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
        
        block = '```\ncode block\n```'
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)

        block = "> This is a quote\n> with multiple lines"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_blocktype(block), BlockType.UNORDERED_LIST)
        
        block = "1. item 1\n2. item 2\n3. item 3"
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)
        
        # false cases
        
        block = "####### heading normal"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
        block = "###"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
        block = "```\ncode block"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
        block = "This is not a quote\n> with multiple lines"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
        block ="-ncdn\n-dndfkak\n-3. dndk"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
        block="2. item 1\n3. item 2\n4. item 3"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
    
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()