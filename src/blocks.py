import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "u_list"
    ORDERED_LIST = "o_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []

    for i in range(len(blocks)):
        if blocks[i] == "":
            continue

        result.append(blocks[i].strip())
   
    return result

def block_to_block_type(block):
    if re.fullmatch(r"#{1,6} .+", block):
        return BlockType.HEADING

    if re.fullmatch(r"```\n[\s\S]*```", block):
        return BlockType.CODE

    if re.fullmatch(r"(?:>.*(?:\n|$))+", block):
        return BlockType.QUOTE

    if re.fullmatch(r"(?:- .*(?:\n|$))+", block):
        return BlockType.UNORDERED_LIST

    if re.fullmatch(r"(?:\d+\. .*(?:\n|$))+", block):
        lines = block.strip().splitlines()
        i = 1

        for line in lines:
            if int((line.split(". "))[0]) == i:
                i+=1
                continue
            else:
                return BlockType.PARAGRAPH

        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
