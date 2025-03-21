from textnode import TextNode, TextType, markdown_to_html_node
from textnode import extract_title
import os
import shutil


def copy_directory(source, destination):
    """ Recursively copy the contents from source to destination. """
    
    # Step 1: Remove all contents from the destination directory
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Deleted all contents of '{destination}'")

    # Step 2: Create the destination directory
    os.mkdir(destination)
    print(f"Created destination directory: {destination}")

    # Step 3: Recursively copy files and directories
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied file: {source_path} -> {destination_path}")
        
        elif os.path.isdir(source_path):
            os.mkdir(destination_path)
            print(f"Created directory: {destination_path}")
            copy_directory(source_path, destination_path)


def generate_page(from_path, template_path, dest_path):
    """Generates an HTML page from a markdown file using a template."""
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, "r", encoding="utf-8") as md_file:
        markdown_content = md_file.read()
    
    print("Raw markdown content:")
 

    # Read the template file
    with open(template_path, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract the title
    try:
        title = extract_title(markdown_content)
    except Exception as e:
        print(f"Error extracting title from {from_path}: {e}")
        return

    # Replace placeholders in the template
    full_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Create the destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the full HTML page to the destination path
    with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(full_page)

    print(f"Page generated at {dest_path}")


def main():
    # Testing the TextNode class
    random_node = TextNode("Some random text", TextType.LINK, "www.random.com")
    print(random_node)

    # Copy the static content to public directory
    copy_directory("static", "public")

    # Generate the webpage
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()

