from textnode import TextNode, TextType, text_to_text_node
from block_funcs import markdown_to_block

def main():
    text = "# This is a heading\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"

    print(markdown_to_block(text))

if __name__ == "__main__":
    main()