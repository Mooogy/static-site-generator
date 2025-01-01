import unittest

from textnode import *
from htmlnode import *
from inline_funcs import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextToHTML(unittest.TestCase):
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

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.NORMAL
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.NORMAL),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.NORMAL
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

class TestExtractMDLinks(unittest.TestCase):
    def test_link_middle(self):
        text = "This text has a link [to google.com](https://google.com). Check it out!"
        links = extract_markdown_links(text)

        self.assertEqual(
            [
                ("to google.com", "https://google.com")
            ],
            links)
    
    def test_link_middle_double(self):
        text = "Which one is better, [google.com](https://google.com) or [bing.com](https://bing.com)? The world may never know!"
        links = extract_markdown_links(text)

        self.assertEqual(
            [
                ("google.com", "https://google.com"),
                ("bing.com", "https://bing.com")
            ],
            links)

    def test_link_end(self):
        text = "I put this link at the end of the text, go watch some [YouTube](https://youtube.com)"
        links = extract_markdown_links(text)

        self.assertEqual(
            [
                ("YouTube", "https://youtube.com")
            ],
            links)
    
    def test_link_start_end(self):
        text = "Go watch some [YouTube](https://youtube.com) or listen to some [Spotify](https://spotify.com)"
        links = extract_markdown_links(text)

        self.assertEqual(
            [
                ("YouTube", "https://youtube.com"),
                ("Spotify", "https://spotify.com")
            ],
            links)
    
    def test_link_blank(self):
        text = "Can you even click this link? [](https://youtube.com)"

        self.assertRaises(ValueError, extract_markdown_links, text)
    
class TestExtractMDImages(unittest.TestCase):
    def test_img_middle(self):
        text = "Check out this cat: ![cat picture](link to cat photo) So cool!"

        self.assertEqual(
            [
                ("cat picture", "link to cat photo")
            ],
            extract_markdown_images(text))  
    
    def test_img_double_middle(self):
        text = "Cat picture: ![cat picture](link to cat photo) And a dog picture: ![dog picture](link to dog photo) So cute!"

        self.assertEqual(
            [
                ("cat picture", "link to cat photo"),
                ("dog picture", "link to dog photo")
            ], 
            extract_markdown_images(text))
    
    def test_img_end(self):
        text = "Cat picture again?: ![cat picture 2](link to cat photo 2)"

        self.assertEqual(
            [
                ("cat picture 2", "link to cat photo 2")
            ],
            extract_markdown_images(text))
    
    def test_img_begin_end(self):
        text= "![dog picture](link to dog photo) Or ![dog picture 2](link to dog photo 2)"

        self.assertEqual(
            [
                ("dog picture", "link to dog photo"),
                ("dog picture 2", "link to dog photo 2")
            ],
            extract_markdown_images(text))
    
    def test_img_no_alt(self):
        text = "Dog photo: ![](link to dog photo)"

        self.assertRaises(ValueError, extract_markdown_images, text)
    
    def test_img_no_link(self):
        text = "Dog photo: ![yay]()"

        self.assertRaises(ValueError, extract_markdown_images, text)

if __name__ == "__main__":
    unittest.main()