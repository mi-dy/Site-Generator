import unittest

from htmlnode import HTMLNode, LeafNode

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
