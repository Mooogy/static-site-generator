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
        return f"HTMLNode(<{self.tag}>, {f"\"{self.value}\"" if self.value else None}, {self.children}, {self.props_to_html()})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None: raise ValueError("Leaf node has NONE value")
        if not self.tag: return self.value

        attributes = (f" {self.props_to_html()}" if self.props else "")

        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag: raise ValueError("ParentNode has no tag")
        if not self.children: raise ValueError("ParentNode has no children") 

        attributes = (f" {self.props_to_html()}" if self.props else "")
        innerContent = "".join(map(lambda leaf : leaf.to_html(), self.children))

        return f"<{self.tag}{attributes}>{innerContent}</{self.tag}>"