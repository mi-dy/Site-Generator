import re
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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        d_count = node.text.count(delimiter)
        if d_count % 2 != 0:
            raise Exception("Invalid Markdown syntax")
        if d_count == 0:
            new_nodes.append(node)
            continue

        text_split = node.text.split(delimiter)
            
        for i, text in enumerate(text_split):
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]+)\]\(([^\(\)]+)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)", text)
    return matches


if __name__ == "__main__":
    main()
