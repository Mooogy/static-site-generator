import os
import shutil
from block_funcs import markdown_to_block, markdown_to_html_node

def copy_files_to_dir(source_dir, target_dir):
    # Clear target directory
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)

    # Copy every file or directory from source to target
    if not os.path.exists(source_dir): raise ValueError("Source directory does not exist")
    source_paths = os.listdir(source_dir)
    if len(source_paths) == 0: raise ValueError("Source directory is empty")
    for path in source_paths:
        combined_source_path = os.path.join(source_dir, path)
        destination_path = os.path.join(target_dir, path)

        # If source path leads to a file, copy over to destination
        if os.path.isfile(combined_source_path):
            print(f"Copying {combined_source_path} to {destination_path}")
            shutil.copy(combined_source_path, destination_path)
        # Source path leads to directory so use recursion
        else:
            if not os.path.exists(destination_path): os.mkdir(destination_path)
            copy_files_to_dir(combined_source_path, destination_path)

def extract_title(markdown):
    blocks = markdown_to_block(markdown)
    for block in blocks:
        if block.startswith("# ") and len(block) > 2:
            return block.lstrip("# ").rstrip()
    raise ValueError("No title was found in the markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} as a template")

    # Read markdown from file
    if not os.path.exists(from_path): raise ValueError("Source path does not exist")
    source_file = open(from_path, "r", encoding="utf-8")
    markdown = source_file.read()
    if markdown == "": raise ValueError("Source path is empty (blank file)")
    source_file.close()

    # Extract page title and content from markdown
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown)

    # Read template from file
    if not os.path.exists(template_path): raise ValueError("Template path does not exist")
    template_file = open(template_path, "r", encoding="utf-8")
    template = template_file.read()
    if template == "": raise ValueError("Template path is empty (blank file)")
    template_file.close()

    # Insert title and content into template
    template = template.replace("{{ Title }}", title)
    filled_template = template.replace("{{ Content }}", content.to_html())

    # Need to create destination directories if non-existing

    dest_dirname = os.path.dirname(dest_path)
    if not os.path.exists(dest_dirname):
        os.makedirs(dest_dirname)

    dest_file = open(dest_path, "w", encoding="utf-8")
    dest_file.write(filled_template)
    dest_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_path):
    if not os.path.exists(dir_path_content): raise ValueError("Content path does not exist")
    content_paths = os.listdir(dir_path_content)

    for path in content_paths:
        combined_path = dir_path_content + "/" + path
        combined_dest = dest_path + "/" + path
        if os.path.isfile(combined_path):
            html_file_path = combined_dest.rsplit(".", 1)[0] + ".html"
            generate_page(combined_path, template_path, html_file_path)
        elif os.path.isdir(combined_path):
            generate_pages_recursive(combined_path, template_path, combined_dest)