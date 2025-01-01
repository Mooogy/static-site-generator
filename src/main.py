from textnode import *
from htmlnode import *

def main():
    dummy_text = TextNode("This is a bold text node", TextType.BOLD)
    print(dummy_text)
    dummy_html = text_node_to_html_node(dummy_text)
    print(dummy_html.to_html())

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

if __name__ == "__main__":
    main()