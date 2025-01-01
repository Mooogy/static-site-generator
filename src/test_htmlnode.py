import unittest

from htmlnode import HTMLNode

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
        expected_repr = "HTMLNode(<a>, Google, None,  href=\"https://google.com\" target=\"blank\")"

        self.assertEqual(repr(node), expected_repr)
    
    def test_props_to_html(self):

        props = {
            "href": "https://google.com", 
            "target": "blank"
            }

        node = HTMLNode(props=props)
        expected_output = " href=\"https://google.com\" target=\"blank\""

        self.assertEqual(node.props_to_html(), expected_output)
    
    def test_props_to_html_fail(self):

        props = {
            "href": "https://google.com", 
            "target": "blank",
            }

        node = HTMLNode(props=props)
        expected_output = " href=\"https://bing.com\" target=\"blank\""

        self.assertNotEqual(node.props_to_html(), expected_output)