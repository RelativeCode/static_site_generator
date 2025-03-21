from enum import Enum
from htmlnode import *
import re

# Function to extract the title from markdown
def extract_title(markdown):
    """Extract the H1 title from the markdown. Raises an exception if not found."""
    lines = markdown.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("# "):  # H1 header starts with '# '
            return line[2:].strip()  # Remove the '# ' and strip any leading/trailing whitespace
    raise ValueError("No H1 header found in markdown.")

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if any(block.startswith(prefix + ' ') for prefix in ['#', '##', '###', '####', '#####', '######']):
        return BlockType.HEADING
    elif block.startswith('```') and block.endswith('```') and block.count('```') == 2:
        return BlockType.CODE
    elif all(line.startswith('>') for line in block.split('\n') if line.strip()):
        return BlockType.QUOTE
    elif all(line.startswith('- ') for line in block.split('\n')):
        return BlockType.UNORDERED_LIST
    elif all(line.strip() and line.strip()[0].isdigit() and '. ' in line.strip() for line in block.split('\n')):
        try:
            lines = block.split('\n')
            for line in lines:
                num_part = line.strip().split('.')[0]
                int(num_part)
            return BlockType.ORDERED_LIST
        except ValueError:
            return BlockType.PARAGRAPH
    return BlockType.PARAGRAPH

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", " ", {"src": text_node.url, "alt": text_node.text or "Image"})
    else:
        raise ValueError("Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        segments = []
        current_index = 0
        while True:
            start_index = text.find(delimiter, current_index)
            if start_index == -1:
                if current_index < len(text):
                    segments.append((text[current_index:], False))
                break
            if start_index > current_index:
                segments.append((text[current_index:start_index], False))
            end_index = text.find(delimiter, start_index + len(delimiter))
            if end_index == -1:
                segments.append((text[start_index:], False))
                break
            content = text[start_index + len(delimiter):end_index]
            segments.append((content, True))
            current_index = end_index + len(delimiter)
        for segment_text, is_delimited in segments:
            if is_delimited:
                new_nodes.append(TextNode(segment_text, text_type))
            else:
                new_nodes.append(TextNode(segment_text, TextType.NORMAL))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            parts = extract_markdown_images(node.text)
            if not parts:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for alt_text, url in parts:
                    image_syntax = f"![{alt_text}]({url})"
                    before, _, after = remaining_text.partition(image_syntax)
                    if before:
                        new_nodes.append(TextNode(before, TextType.NORMAL))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                    remaining_text = after
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            parts = extract_markdown_links(node.text)
            if not parts:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for alt_text, url in parts:
                    link_syntax = f"[{alt_text}]({url})"
                    before, _, after = remaining_text.partition(link_syntax)
                    if before:
                        new_nodes.append(TextNode(before, TextType.NORMAL))
                    new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                    remaining_text = after
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    # Kept this one-liner for basic feedback
    print(f"Processed nodes: {[(node.text, node.text_type) for node in nodes]}")
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split('\n\n') if block.strip()]
    return blocks

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes if text_node_to_html_node(node) is not None]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    # Print only block count and first block preview
    print(f"Processing {len(blocks)} blocks...")

    parent_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            parent_node.children.append(ParentNode("p", text_to_children(block)))
        elif block_type == BlockType.HEADING:
            level = len(block.split(' ')[0])
            content = block.lstrip('#').lstrip()
            parent_node.children.append(ParentNode(f"h{level}", text_to_children(content)))
        elif block_type == BlockType.CODE:
            parent_node.children.append(ParentNode("pre", [LeafNode("code", block.strip())]))
        elif block_type == BlockType.QUOTE:
            clean_content = "\n".join([line.lstrip(">").lstrip() for line in block.split("\n")])
            parent_node.children.append(ParentNode("blockquote", text_to_children(clean_content)))
        elif block_type == BlockType.UNORDERED_LIST:
            ul_node = ParentNode("ul", [ParentNode("li", text_to_children(line.strip()[2:])) for line in block.split("\n")])
            parent_node.children.append(ul_node)
        elif block_type == BlockType.ORDERED_LIST:
            ol_node = ParentNode("ol", [ParentNode("li", text_to_children(line.split('. ', 1)[1].strip())) for line in block.split("\n")])
            parent_node.children.append(ol_node)

    return parent_node
