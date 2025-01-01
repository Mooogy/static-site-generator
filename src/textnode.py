from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.content = text
        self.type = text_type
        self.url = url

    def __eq__(self, rhs):
        return (True if self.content == rhs.content and self.type == rhs.type and self.url == rhs.url else False)
    
    def __repr__(self):
        return f"TextNode({self.content}, {self.type.value}, {self.url})"
    