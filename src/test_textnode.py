import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()
