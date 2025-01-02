import unittest

from textnode import TextNode, TextType
from inline_funcs import (
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    extract_markdown_images,
    extract_markdown_links
    )

class TestSplitDelim(unittest.TestCase):
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
    
    def test_link_and_image(self):
        text = "[This is a link](https://youtube.com) and ![this is an image](image link)"

        self.assertEqual(
            [
                ("This is a link", "https://youtube.com")
            ],
            extract_markdown_links(text))

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
    
    def test_img_and_link(self):
        text= "![dog picture](link to dog photo) or [a link to a cat themed website](link)"

        self.assertEqual(
            [
                ("dog picture", "link to dog photo"),
            ],
            extract_markdown_images(text))
    
    def test_img_no_alt(self):
        text = "Dog photo: ![](link to dog photo)"

        self.assertRaises(ValueError, extract_markdown_images, text)
    
    def test_img_no_link(self):
        text = "Dog photo: ![yay]()"

        self.assertRaises(ValueError, extract_markdown_images, text)

class TestSplitLink(unittest.TestCase):
    def test_middle(self):
        old_nodes = [TextNode("This text node has a link [to YouTube](https://youtube.com). Watch now!", TextType.NORMAL)]

        self.assertEqual(
            [
                TextNode("This text node has a link ", TextType.NORMAL),
                TextNode("to YouTube", TextType.LINK, "https://youtube.com"),
                TextNode(". Watch now!", TextType.NORMAL)
            ],
            split_nodes_link(old_nodes))
    
    def test_start_end(self):
        old_nodes = [TextNode("[Go to YouTube](https://youtube.com) or [go to Spotify](https://spotify.com)", TextType.NORMAL)]

        self.assertEqual(
            [
                TextNode("Go to YouTube", TextType.LINK, "https://youtube.com"),
                TextNode(" or ", TextType.NORMAL),
                TextNode("go to Spotify", TextType.LINK, "https://spotify.com")
            ],
            split_nodes_link(old_nodes))
    
    def test_double_middle(self):
        old_nodes = [TextNode("Do you listen to music on [YouTube](https://youtube.com) or [Spotify](https://spotify.com)? I use both!", TextType.NORMAL)]

        self.assertEqual(
            [
                TextNode("Do you listen to music on ", TextType.NORMAL),
                TextNode("YouTube", TextType.LINK, "https://youtube.com"),
                TextNode(" or ", TextType.NORMAL),
                TextNode("Spotify", TextType.LINK, "https://spotify.com"),
                TextNode("? I use both!", TextType.NORMAL)
            ],
            split_nodes_link(old_nodes))

class TestSplitImage(unittest.TestCase):
    def test_middle(self):
        old_nodes = [TextNode("This text has an image! ![image of a cat](cat link) How cute!!", TextType.NORMAL)]

        self.assertEqual([
            TextNode("This text has an image! ", TextType.NORMAL),
            TextNode("image of a cat", TextType.IMAGE, "cat link"),
            TextNode(" How cute!!", TextType.NORMAL)
            ],
            split_nodes_image(old_nodes))

    def test_start_end(self):
        old_nodes = [TextNode("![image of a cat](cat link) or ![image of a dog](dog link)", TextType.NORMAL)]

        self.assertEqual([
            TextNode("image of a cat", TextType.IMAGE, "cat link"),
            TextNode(" or ", TextType.NORMAL),
            TextNode("image of a dog", TextType.IMAGE, "dog link")
            ],
            split_nodes_image(old_nodes))

    def test_double_middle(self):
        old_nodes = [TextNode("This ![image of a cat](cat link) or ![image of a dog](dog link)? Choose now.", TextType.NORMAL)]

        self.assertEqual([
            TextNode("This ", TextType.NORMAL),
            TextNode("image of a cat", TextType.IMAGE, "cat link"),
            TextNode(" or ", TextType.NORMAL),
            TextNode("image of a dog", TextType.IMAGE, "dog link"),
            TextNode("? Choose now.", TextType.NORMAL)
            ],
            split_nodes_image(old_nodes))
    
    def test_single(self):
        old_nodes = [TextNode("![image](image link)", TextType.NORMAL)]

        self.assertEqual([
            TextNode("image", TextType.IMAGE, "image link"),
            ],
            split_nodes_image(old_nodes))
    
    def test_with_link(self):
        old_nodes = [TextNode("![image](image link) and [link](link)", TextType.NORMAL)]

        self.assertEqual([
            TextNode("image", TextType.IMAGE, "image link"),
            TextNode(" and [link](link)", TextType.NORMAL)
            ],
            split_nodes_image(old_nodes))

if __name__ == "__main__":
    unittest.main()