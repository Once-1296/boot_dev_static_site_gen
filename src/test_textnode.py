import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("HELLEOEOOEOEO", TextType.ITALIC)
        node4 = TextNode("WOOWOOWOWOW", TextType.TEXT, 'http://localhost:8080')
        self.assertNotEqual(node3,node4)
        node5 = TextNode("W", TextType.CODE, 'http://localhost:8080')
        node6 = TextNode("W", TextType.CODE, 'http://localhost:8080')
        self.assertEqual(node6,node5)
        node7 = TextNode("abc.com", TextType.LINK)
        node8 = TextNode("abc.com", TextType.LINK, 'http://localhost:8080')
        self.assertNotEqual(node7,node8)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_splitter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert new_nodes == [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]


if __name__ == "__main__":
    unittest.main()