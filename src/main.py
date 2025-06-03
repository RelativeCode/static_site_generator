from textnode import TextNode, TextType, markdown_to_html_node
from textnode import extract_title
import os
import shutil
import sys

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


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as md_file:
        markdown_content = md_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()


    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()


    try:
        title = extract_title(markdown_content)
    except Exception as e:
        print(f"Error extracting title from {from_path}: {e}")
        return


    full_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # 🔁 Replace root-relative URLs with basepath
    full_page = full_page.replace('href="/', f'href="{basepath}/')
    full_page = full_page.replace('src="/', f'src="{basepath}/')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)


    with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(full_page)

    print(f"Page generated at {dest_path}")



def generate_pages_recursive(content_dir, template_path, dest_dir, basepath):
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                
                rel_path = os.path.relpath(from_path, content_dir)
                new_file_name = os.path.splitext(rel_path)[0] + ".html"
                dest_path = os.path.join(dest_dir, new_file_name)

                print(f"Generating page for: {from_path} -> {dest_path}")
                generate_page(from_path, template_path, dest_path, basepath)



def main():
    # Default to root if no base path is provided
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Using basepath: {basepath}")

    copy_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()

