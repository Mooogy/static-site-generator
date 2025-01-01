import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode()
        expected_repr = 'HTMLNode(<None>, None, None, None)'

        self.assertEqual(repr(node), expected_repr)

    def test_repr_2(self):
        props = {
            "href": "https://google.com", 
            "target": "blank"
            }

        node = HTMLNode("a", "Google", props=props)
        expected_repr = "HTMLNode(<a>, Google, None, href=\"https://google.com\" target=\"blank\")"

        self.assertEqual(repr(node), expected_repr)
    
    def test_props_to_html(self):

        props = {
            "href": "https://google.com", 
            "target": "blank"
            }

        node = HTMLNode(props=props)
        expected_output = "href=\"https://google.com\" target=\"blank\""

        self.assertEqual(node.props_to_html(), expected_output)
    
    def test_props_to_html_fail(self):

        props = {
            "href": "https://google.com", 
            "target": "blank",
            }

        node = HTMLNode(props=props)
        expected_output = " href=\"https://bing.com\" target=\"blank\""

        self.assertNotEqual(node.props_to_html(), expected_output)

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        output = "<p>This is a paragraph of text.</p>"

        self.assertEqual(node.to_html(), output)

    def test_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        output = "<a href=\"https://www.google.com\">Click me!</a>"
        
        self.assertEqual(node.to_html(), output)

    def test_to_html_rawtext(self):
        node = LeafNode(None, "This is just raw text!")
        output = "This is just raw text!"

        self.assertEqual(node.to_html(), output)
    
    def test_to_html_no_value(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})

        self.assertRaises(ValueError, node.to_html)

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "Italic text")])
        expected_output = "<p><b>Bold text</b>Normal text<i>Italic text</i></p>"
        self.assertEqual(node.to_html(), expected_output)
    
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "Italic text")])
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_no_children(self):
        node = ParentNode("p", None, {"href": "https://www.google.com"})
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_nested_parent(self):
        node = ParentNode("a", [ParentNode("p", [LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "Italic text")]),
                                LeafNode(None, "Some more normal text")],
                                {"href": "https://www.google.com"})
        expected_output = "<a href=\"https://www.google.com\"><p><b>Bold text</b>Normal text<i>Italic text</i></p>Some more normal text</a>"
        self.assertEqual(node.to_html(), expected_output)
    
if __name__ == "__main__":
    unittest.main()