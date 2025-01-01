class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return "None"

        attributes = ""
        for pair in self.props.items():
            attributes = attributes + f"{pair[0]}=\"{pair[1]}\" "

        return attributes[:len(attributes) - 1]

    def __repr__(self):
        return f"HTMLNode(<{self.tag}>, {self.value}, {self.children}, {self.props_to_html()})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None: raise ValueError("All leaf nodes must have a value")
        if self.tag == None: return self.value

        return f"<{self.tag}{f" {self.props_to_html()}" if self.props else ""}>{self.value}</{self.tag}>"
    