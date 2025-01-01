from textnode import *
from htmlnode import *

def main():
    dummy_text = TextNode("This is *italic* text", TextType.NORMAL)
    dummy_text2 = TextNode("This is **bold**", TextType.NORMAL)
    split_nodes_delimiter([dummy_text, dummy_text2], "*", TextType.ITALIC)

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

# Must check for bold (**) first to avoid problems with italic(*)
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimiter_length = len(delimiter)
    
    for old_node in old_nodes:
        # If not of type normal, no need to split it
        if old_node.type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        content = old_node.content

        start = 0
        end = 0
        delimiter_open = False

        while start < len(content) and end != -1:
            end = content.find(delimiter, start)

            text = content[start:(end if end != -1 else len(content))]
            node_type = (text_type if delimiter_open else TextType.NORMAL)

            if text != "": new_nodes.append(TextNode(text, node_type))

            if end != -1:
                delimiter_open = (True if not delimiter_open else False)

            start = end + delimiter_length

    return new_nodes

if __name__ == "__main__":
    main()