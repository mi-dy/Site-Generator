import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import BlockType, markdown_to_blocks, block_to_block_type 

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


def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]

    delimiters = [("**", TextType.BOLD), ("_", TextType.ITALIC), ("`", TextType.CODE)]

    for d, tt in delimiters:
        node = split_nodes_delimiter(node, d, tt)

    node = split_nodes_link(split_nodes_image(node))
    
    return node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    result = []

    for block in blocks:
        b_type = block_to_block_type(block)

        if b_type == BlockType.PARAGRAPH:
            text = block.replace("\n", " ")

            children = text_to_children(text)
            result.append(ParentNode("p", children))

        if b_type == BlockType.HEADING:
            hashes = re.match(r"(#{1,6}) ", block)
            level = len(hashes.group(1))
            tag = f"h{level}"
            text = block[level+1:]

            children = text_to_children(text)
            result.append(ParentNode(tag, children))

        if b_type == BlockType.CODE:
            text = block[4:-3]
            t_node = TextNode(text, TextType.TEXT)
            child_node = text_node_to_html_node(t_node)
            code_node = ParentNode("code", [child_node])
            pre_node = ParentNode("pre", [code_node])
            result.append(pre_node)
        
        if b_type == BlockType.QUOTE:
            lines = block.split("\n")
            n_block = ""
            for line in lines:
                line = line.strip(">").strip(" ")
                if n_block == "":
                    n_block = line
                else:
                    n_block = n_block + " " + line

            children = text_to_children(n_block)
            result.append(ParentNode("blockquote", children))

        if b_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            p_nodes = []
            for line in lines:

                line = line[2:]
                children = text_to_children(line)
                p_nodes.append(ParentNode("li", children))

            result.append(ParentNode("ul", p_nodes))

        if b_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            p_nodes = []

            for line in lines:
                parts = line.split(".", 1)
                if len(parts) > 1:
                    l_text = parts[1].strip(" ")

                children = text_to_children(l_text)
                p_nodes.append(ParentNode("li", children))

            result.append(ParentNode("ol", p_nodes))

    return ParentNode("div", result)



def text_to_children(text):
    t_nodes = text_to_textnodes(text)
    children = []

    for node in t_nodes:
        children.append(text_node_to_html_node(node))

    return children


if __name__ == "__main__":
    main()
