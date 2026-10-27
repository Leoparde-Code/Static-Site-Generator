from textnode import TextNode, TextType
from markdown_images_and_links import extract_markdown_images, extract_markdown_links

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_images(old_node.text)
            remaining_text = old_node.text
            for match in matches:
                alt_text, url = match[0], match[1]
                image_markdown = f"![{alt_text}]({url})"
                sections = remaining_text.split(image_markdown, 1)
                before_text, after_text = sections[0], sections[1]
                image = TextNode(alt_text, TextType.IMAGE, url)
                if before_text != "":
                    new_nodes.append(TextNode(before_text, TextType.TEXT))
                new_nodes.append(image)
                remaining_text = after_text
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))




    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_links(old_node.text)
            remaining_text = old_node.text
            for match in matches:
                alt_text, url = match[0], match[1]
                link_markdown = f"[{alt_text}]({url})"
                sections = remaining_text.split(link_markdown, 1)
                before_text, after_text = sections[0], sections[1]
                link = TextNode(alt_text, TextType.LINK, url)
                if before_text != "":
                    new_nodes.append(TextNode(before_text, TextType.TEXT))
                new_nodes.append(link)
                remaining_text = after_text
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))




    return new_nodes
