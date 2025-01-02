from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.content = text
        self.type = text_type
        self.url = url

    def __eq__(self, rhs):
        return (True if self.content == rhs.content and self.type == rhs.type and self.url == rhs.url else False)
    
    def __repr__(self):
        return f"TextNode(\"{self.content}\", {self.type.value}, {self.url})"

def text_node_to_html_node(text_node):
    value = text_node.content
    url = text_node.url
    match text_node.type:
        case TextType.NORMAL:
            return LeafNode(None, value)
        case TextType.BOLD:
            return LeafNode("b", value)
        case TextType.ITALIC:
            return LeafNode("i", value)
        case TextType.CODE:
            return LeafNode("code", value)
        case TextType.LINK:
            return LeafNode("a", value, {"href": url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"alt": value, "src": url})
        case _:
            raise ValueError("Input TextNode has invalid TextType")

from inline_funcs import *

def text_to_text_node(text):
    text_nodes = [TextNode(text, TextType.NORMAL)]

    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)

    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    
    return text_nodes