from htmlnode import HTMLNode, ParentNode
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node_list = []
    for block in blocks:
        block_type = block_to_block_type(block)


        if block_type == BlockType.PARAGRAPH:
            cleaned_block = block.replace("\n", " ")
            new_node = ParentNode("p", children=text_to_children(cleaned_block))
            html_node_list.append(new_node)


        elif block_type == BlockType.HEADING:
            counter = 0
            for i in block:
                if i == "#":
                    counter += 1
                else:
                    break
            cleaned_block = block[counter + 1:]
            new_node = ParentNode(f"h{counter}", children=text_to_children(cleaned_block))
            html_node_list.append(new_node)


        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                cleaned_lines.append(line[1:].strip())
            cleaned_block = " ".join(cleaned_lines)
            new_node = ParentNode("blockquote", children=text_to_children(cleaned_block))
            html_node_list.append(new_node)


        elif block_type == BlockType.CODE:
            stripped_block = block[4:-3]
            text_node = TextNode(stripped_block, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            new_node_code = ParentNode("code", children=[html_node])
            new_node = ParentNode("pre", children=[new_node_code])
            html_node_list.append(new_node)


        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                stripped_line = line[2:]
                inline_child = text_to_children(stripped_line)
                new_html = ParentNode("li", children=inline_child)
                cleaned_lines.append(new_html)
            new_node = ParentNode("ul", children=cleaned_lines)
            html_node_list.append(new_node)


        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                stripped_line = line[line.find(". ") + 2:]
                inline_child = text_to_children(stripped_line)
                new_html = ParentNode("li", children=inline_child)
                cleaned_lines.append(new_html)
            new_node = ParentNode("ol", children=cleaned_lines)
            html_node_list.append(new_node)

    final_html_node = ParentNode("div", children=html_node_list)
    return final_html_node





def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children
