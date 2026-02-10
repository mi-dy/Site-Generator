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


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
            continue

        for image_alt, image_link in images:
            sections = node.text.split(f"![{image_alt}]({image_link})", 1)
            
            if len(sections) > 1:
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))

                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                node.text = sections[1]

        if node.text != "":
            new_nodes.append(TextNode(node.text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
            continue

        for link_alt, link in links:
            sections = node.text.split(f"[{link_alt}]({link})", 1)
            
            if len(sections) > 1:
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))

                new_nodes.append(TextNode(link_alt, TextType.LINK, link))
                node.text = sections[1]

        if node.text != "":
            new_nodes.append(TextNode(node.text, TextType.TEXT))

    return new_nodes


if __name__ == "__main__":
    main()
