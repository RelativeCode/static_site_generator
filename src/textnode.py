from enum import Enum
from htmlnode import *

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
        return LeafNode("img", "", {"src": text_node.url})
    else:
        raise ValueError("Invalid text type")



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    if not delimiter:
        raise ValueError("Delimiter cannot be empty")

    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            parts = node.text.split(delimiter)
            
            if len(parts) % 2 == 0:  # Unmatched delimiter
                raise ValueError(f"Unmatched delimiter in text: {node.text}")

            for i, part in enumerate(parts):
                if part:  # Avoid adding empty text nodes
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, TextType.NORMAL))  # Outside delimiters
                    else:
                        new_nodes.append(TextNode(part, text_type))  # Inside delimiters
        else:
            new_nodes.append(node)  # Keep other text types unchanged

    return new_nodes
