from textnode import TextNode, TextType, text_to_text_node

def main():
    text = "This has **bold text**, *italic text*, `code text`, a [link](link), and an image ![image](image)"
    print(text_to_text_node(text))

if __name__ == "__main__":
    main()