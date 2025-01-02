import unittest

from textnode import TextNode, TextType, text_node_to_html_node, text_to_text_node

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

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_normal_text(self):
        text_node = TextNode("This is normal text", TextType.NORMAL)
        converted_html = text_node_to_html_node(text_node).to_html()
        expected = "This is normal text"
        self.assertEqual(expected, converted_html)
    
    def test_bold_text(self):
        text_node = TextNode("This is bold text", TextType.BOLD)
        converted_html = text_node_to_html_node(text_node).to_html()
        expected = "<b>This is bold text</b>"
        self.assertEqual(expected, converted_html)

    def test_italic_text(self):
        text_node = TextNode("This is italic text", TextType.ITALIC)
        converted_html = text_node_to_html_node(text_node).to_html()
        expected = "<i>This is italic text</i>"
        self.assertEqual(expected, converted_html)
    
    def test_code_text(self):
        text_node = TextNode("This is code text", TextType.CODE)
        converted_html = text_node_to_html_node(text_node).to_html()
        expected = "<code>This is code text</code>"
        self.assertEqual(expected, converted_html)
    
    def test_link_text(self):
        text_node = TextNode("This is a link", TextType.LINK, "https://google.com")
        converted_html = text_node_to_html_node(text_node).to_html()
        expected = "<a href=\"https://google.com\">This is a link</a>"
        self.assertEqual(expected, converted_html)
    
    def test_image_text(self):
        text_node = TextNode("Alt text for a 200x200 image", TextType.IMAGE, "https://picsum.photos/200")
        converted_html = text_node_to_html_node(text_node).to_html()
        expected = "<img alt=\"Alt text for a 200x200 image\" src=\"https://picsum.photos/200\"></img>"
        self.assertEqual(expected, converted_html)
    
    def test_none_type(self):
        text_node = TextNode("This doesn't have a TextType!", None)
        self.assertRaises(ValueError, text_node_to_html_node, text_node)

class TestTextToTextNode(unittest.TestCase):
    def test_all_styles(self):
        text = "This has **bold text**, *italic text*, `code text`, a [link](link), and an image ![image](image)"

        self.assertEqual(
            [
                TextNode("This has ", TextType.NORMAL),
                TextNode("bold text", TextType.BOLD),
                TextNode(", ", TextType.NORMAL),
                TextNode("italic text", TextType.ITALIC),
                TextNode(", ", TextType.NORMAL),
                TextNode("code text", TextType.CODE),
                TextNode(", a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "link"),
                TextNode(", and an image ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "image")
            ],
            text_to_text_node(text))

if __name__ == "__main__":
    unittest.main()