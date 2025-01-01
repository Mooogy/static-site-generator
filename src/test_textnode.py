import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertEqual(node, node2)
    
    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_neq_link(self):
        node = TextNode("This is a text node", TextType.NORMAL, "bing.com")
        node2 = TextNode("This is a text node", TextType.NORMAL, "google.com")
        self.assertNotEqual(node, node2)

    def test_neq_content(self):
        node = TextNode("Hello!", TextType.ITALIC)
        node2 = TextNode("Hello.", TextType.ITALIC)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()