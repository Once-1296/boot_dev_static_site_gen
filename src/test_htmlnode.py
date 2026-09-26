import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode('h1','Hello')
        assert 'Hello' in node1.__repr__()
        node2 = HTMLNode('img', 'cat',[], {"alt":"cat"})
        assert '\'alt\': \'cat\'' in node2.__repr__()
        node3 = HTMLNode('link', 'notrickroll',[], {"href": "https://youtu.be/dQw4w9WgXcQ?si=XDdNTGk6gd-g8i3F","target":"_blank"})
        # print(node3.props_to_html())
        assert node3.props_to_html() == " href=\"https://youtu.be/dQw4w9WgXcQ?si=XDdNTGk6gd-g8i3F\" target=\"_blank\""
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        node = LeafNode("img", "cat.jpg", {"src":"assets/cat.jpg"})
        self.assertEqual(node.to_html(), "<img src=\"assets/cat.jpg\">cat.jpg</img>")
        node = LeafNode("i", "birb")
        self.assertEqual(node.to_html(), "<i>birb</i>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
            

if __name__ == "__main__":
    unittest.main()