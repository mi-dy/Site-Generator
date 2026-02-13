import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node, split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes


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

    def test_node_split(self):
        n1 = TextNode("text text **bold** text text", TextType.TEXT)
        n2 = TextNode("**bold** text text", TextType.TEXT)
        n3 = TextNode("text text **bold**", TextType.TEXT)
        n4 = TextNode("bold text", TextType.BOLD)

        new_nodes = split_nodes_delimiter([n1,n2,n3,n4], "**", TextType.BOLD)
        expected = [
                TextNode("text text ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text text", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text text", TextType.TEXT),
                TextNode("text text ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("bold text", TextType.BOLD)]

        self.assertEqual(new_nodes, expected)

    def test_node_split_invalid(self):
        node = TextNode("text ** text", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_extract_markdwon_images(self):
        matches = extract_markdown_images("this is an image ![image](link.com) and this ![image2](link2.com) but not this [link text](link3.com)")

        self.assertEqual(matches, [("image", "link.com"), ("image2", "link2.com")])

    def test_extract_markdwon_links(self):
        matches = extract_markdown_links("this is a link [link1](link.com) and this [link2](link2.com) but not this ![image](link3.com)")

        self.assertEqual(matches, [("link1", "link.com"), ("link2", "link2.com")])

    def test_extract_markdown_false(self):
        match1 = extract_markdown_links("this is just text")
        match2 = extract_markdown_images("this is just text")

        self.assertEqual(match1, [])
        self.assertEqual(match2, [])

    def test_split_nodes_image(self):
        n1 = TextNode("marky text ![image text](www.imglink.com) more text [link text](www.linklink.com)", TextType.TEXT)
        n2 = TextNode("![image text 2](www.imglink2.com)", TextType.TEXT)
        n3 = TextNode("Just plain text", TextType.TEXT)

        result = [
                TextNode("marky text ", TextType.TEXT),
                TextNode("image text", TextType.IMAGE, "www.imglink.com"),
                TextNode(" more text [link text](www.linklink.com)", TextType.TEXT),
                TextNode("image text 2", TextType.IMAGE, "www.imglink2.com"),
                TextNode("Just plain text", TextType.TEXT)]

        self.assertEqual(split_nodes_image([n1,n2,n3]), result)

    def test_split_nodes_link(self):
        n1 = TextNode("marky text [link text](www.linklink.com) more text ![image text](www.imglink.com)", TextType.TEXT)
        n2 = TextNode("[link text 2](www.linklink2.com)", TextType.TEXT)
        n3 = TextNode("Just plain text", TextType.TEXT)

        result = [
                TextNode("marky text ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "www.linklink.com"),
                TextNode(" more text ![image text](www.imglink.com)", TextType.TEXT),
                TextNode("link text 2", TextType.LINK, "www.linklink2.com"),
                TextNode("Just plain text", TextType.TEXT)]

        self.assertEqual(split_nodes_link([n1,n2,n3]), result)


    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(text_to_textnodes(text), result)



if __name__ == "__main__":
    unittest.main()
