from textnode import TextNode, TextType
import re


def main():
    random_node = TextNode("Some random text", TextType.LINK, "www.random.com")
    print(random_node)


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)



if __name__ == "__main__":
    main()
