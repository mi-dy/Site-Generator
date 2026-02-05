import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_valid(self):
        node = HTMLNode("<d>", "onetwothree", [HTMLNode("one"), HTMLNode("two")], {"href": "https://www.google.com", "target": "_blank"})

        self.assertEqual(node.tag, "<d>")
        self.assertEqual(node.value, "onetwothree")
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.props["href"], "https://www.google.com")


    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com", "target": "_blank"})

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    

    def test_props_to_html_none(self):
        node = HTMLNode()

        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "www.googgy.com"})

        self.assertEqual(node.to_html(), '<a href="www.googgy.com">Hello, world!</a>')


    def test_leaf_to_html_ntag(self):
        node = LeafNode(None, "Hello, world!")

        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)

    def test_to_html_no_tag(self):
        child_node = LeafNode("p", "child")
        parent_node = ParentNode(None, [child_node])

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_child(self):
        child_node = LeafNode(None, None)
        parent_node = ParentNode("p", [child_node])

        with self.assertRaises(ValueError):
            parent_node.to_html()
