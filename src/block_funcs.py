from enum import Enum

from htmlnode import ParentNode
from textnode import text_to_text_node, text_node_to_html_node

class BLOCKTYPE(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_block(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)

    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BLOCKTYPE.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BLOCKTYPE.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BLOCKTYPE.PARAGRAPH
        return BLOCKTYPE.QUOTE
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BLOCKTYPE.PARAGRAPH
        return BLOCKTYPE.ULIST
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BLOCKTYPE.PARAGRAPH
        return BLOCKTYPE.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BLOCKTYPE.PARAGRAPH
            i += 1
        return BLOCKTYPE.OLIST
    return BLOCKTYPE.PARAGRAPH

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BLOCKTYPE.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BLOCKTYPE.HEADING:
            return heading_to_html_node(block)
        case BLOCKTYPE.CODE:
            return code_to_html_node(block)
        case BLOCKTYPE.ULIST:
            return ulist_to_html_node(block)
        case BLOCKTYPE.OLIST:
            return olist_to_html_node(block)
        case BLOCKTYPE.QUOTE:
            return quote_to_html_node(block)

def text_to_children(text):
    text_nodes = text_to_text_node(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    
    text = block[level + 1:]
    children = text_to_children(text)

    return ParentNode("h1", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def ulist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        children = text_to_children(line[2:])
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)

def olist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        children = text_to_children(line[2:])
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        quote_lines.append(line.lstrip(">").rstrip())
    
    text = " ".join(quote_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)