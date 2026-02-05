import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_equal(self):
        node = TextNode("equal", TextType.BOLD)
        node2 = TextNode("equal", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("one", TextType.ITALIC)
        node2 = TextNode("two", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        url_none = TextNode("check", TextType.TEXT)
        url_y = TextNode("adress", TextType.LINK, "www.link.com")
        self.assertIsNone(url_none.url)
        self.assertTrue(url_y.url)
    
    def test_text_to_html_TEXT(self):
        node = TextNode("Test node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Test node")

    def test_text_to_html_BOLD(self):
        node = TextNode("BOLD node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "BOLD node")

    def test_text_to_html_ITALIC(self):
        node = TextNode("Italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic node")

    def test_text_to_html_CODE(self):
        node = TextNode("Code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code node")

    def test_text_to_html_LINK(self):
        node = TextNode("Link node", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})

    def test_text_to_html_IMAGE(self):
        node = TextNode("this is an image", TextType.IMAGE, "www.image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.image.com", "alt": "this is an image"})


if __name__ == "__main__":
    unittest.main()
