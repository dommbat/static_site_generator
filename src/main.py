import os
import shutil
from pathlib import Path
from textnode import extract_title
from htmlnode import markdown_to_html_node


def copy_dir_clean(src, dst):
    src_path = Path(src).resolve()
    dst_path = Path(dst).resolve()

    if not src_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {src_path}")

    if dst_path.exists():
        for child in dst_path.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        dst_path.mkdir(parents=True, exist_ok=True)

    for root, dirs, files in os.walk(src_path):
        root_path = Path(root)
        rel_root = root_path.relative_to(src_path)
        target_root = dst_path.joinpath(rel_root)
        target_root.mkdir(parents=True, exist_ok=True)

        for name in files:
            src_file = root_path / name
            dst_file = target_root / name
            shutil.copy2(src_file, dst_file)
            print(f"Copied {src_file} -> {dst_file}")

    print(f"Finished copying from {src_path} to {dst_path}")


def generate_page(from_path, template_path, dest_path):
    """Generate an HTML page from markdown content using a template.
    
    Args:
        from_path: Path to the markdown file
        template_path: Path to the HTML template file
        dest_path: Path where the generated HTML will be written
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Create destination directory if needed
    dest_file = Path(dest_path)
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the final HTML
    with open(dest_path, 'w') as f:
        f.write(full_html)
    
    print(f"Page generated successfully at {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Recursively generate HTML pages from markdown files in a directory tree.
    
    Args:
        dir_path_content: Path to the content directory containing markdown files
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory where HTML files will be written
    """
    content_path = Path(dir_path_content)
    dest_path = Path(dest_dir_path)
    template_file = Path(template_path)
    
    # Walk through the content directory
    for root, dirs, files in os.walk(content_path):
        root_path = Path(root)
        rel_root = root_path.relative_to(content_path)
        target_root = dest_path.joinpath(rel_root)
        target_root.mkdir(parents=True, exist_ok=True)
        
        # Process each markdown file
        for name in files:
            if name.endswith('.md'):
                src_file = root_path / name
                # Replace .md with .html
                dest_file = target_root / name.replace('.md', '.html')
                generate_page(src_file, template_file, dest_file)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    source = repo_root / "static"
    destination = repo_root / "public"
    copy_dir_clean(source, destination)
    
    # Generate pages recursively from content directory
    generate_pages_recursive(
        repo_root / "content",
        repo_root / "template.html",
        repo_root / "public"
    )


if __name__ == "__main__":
    main()
