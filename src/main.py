from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    node = TextNode("some text", TextType.LINK, "www.wowza.com")
    print(node)


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        result = LeafNode(tag=None, value=text_node.text)
        return result

    if text_node.text_type == TextType.BOLD:
        result = LeafNode(tag="b", value=text_node.text)
        return result

    if text_node.text_type == TextType.ITALIC:
        result = LeafNode(tag="i", value=text_node.text)
        return result

    if text_node.text_type == TextType.CODE:
        result = LeafNode(tag="code", value=text_node.text)
        return result

    if text_node.text_type == TextType.LINK:
        result = LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        return result

    if text_node.text_type == TextType.IMAGE:
        result = LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        return result
    raise Exception("TextType not found")

if __name__ == "__main__":
    main()
