from enum import Enum

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
        return f"TextNode({self.content}, {self.type.value}, {self.url})"
    