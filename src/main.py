from textnode import TextNode, TextType


def main():
    random_node = TextNode("Some random text", TextType.LINK, "www.random.com")
    print(random_node)



if __name__ == "__main__":
    main()
