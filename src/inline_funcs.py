from textnode import TextNode, TextType
import re

# Must check for bold (**) first to avoid problems with italic(*)
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimiter_length = len(delimiter)
    
    for old_node in old_nodes:
        # If not of type normal, no need to split it
        if old_node.type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        content = old_node.content

        start = 0
        end = 0
        delimiter_open = False

        while start < len(content) and end != -1:
            end = content.find(delimiter, start)

            text = content[start:(end if end != -1 else len(content))]
            node_type = (text_type if delimiter_open else TextType.NORMAL)

            if text != "": new_nodes.append(TextNode(text, node_type))

            if end != -1:
                delimiter_open = (True if not delimiter_open else False)

            start = end + delimiter_length

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        # If the node isn't a normal type, no need to split
        if old_node.type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        content = old_node.content
        links = extract_markdown_links(content)

        # If text has no links, no need to split
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        for link in links:
            # Split content by link ["{string}","{string}"]
            sections = content.split(f"[{link[0]}]({link[1]})", 1)

            if len(sections) != 2: raise ValueError("Unclosed link")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))

            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            # Content to split becomes the right-side section
            content = sections[1]
        
        # Attach last section to new nodes if not empty
        if content != "":
            new_nodes.append(TextNode(content, TextType.NORMAL))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        content = old_node.content
        images = extract_markdown_images(content)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            sections = content.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) != 2: raise ValueError("Unclosed image")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))

            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            content = sections[1]

        if content != "":
            new_nodes.append(TextNode(content, TextType.NORMAL))

    return new_nodes

def extract_markdown_links(text):
    md_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    if len(md_links) == 0: return []

    for pair in md_links:
        if pair[0] == "": raise ValueError("Contains unaccessible link ( empty content between [] )")
        if pair[1] == "": raise ValueError("Contains link with no destination ( empty content between () )")

    # List[(text, link)]
    return md_links

def extract_markdown_images(text):
    images = re.findall(r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    if len(images) == 0: return []

    for pair in images:
        if pair[0] == "": raise ValueError("Contains image with no alt text ( empty content between [] )")
        if pair[1] == "": raise ValueError("Contains image with no source ( empty content between () )")

    return images
