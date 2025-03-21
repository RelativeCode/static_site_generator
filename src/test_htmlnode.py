# In test_htmlnode.py
import unittest
from htmlnode import *
from textnode import *

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_with_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_with_no_props(self):
        # Test with no properties (None)
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_with_empty_props(self):
        # Test with empty properties dictionary
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr_method(self):
        # Test the __repr__ method
        node = HTMLNode(tag="p", value="Hello", children=[], props={"class": "text"})
        expected = 'HTMLNode(tag=p, value=Hello, children=[], props={\'class\': \'text\'})'
        self.assertEqual(repr(node), expected)
    
    def test_to_html_raises_error(self):
        # Test that to_html raises NotImplementedError
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    


    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()