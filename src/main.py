from textnode import TextNode, TextType

from pathlib import Path
import os
import shutil
import argparse
import sys

from blocks import markdown_to_html_node

def extract_title(markdown:str)->str:
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path,basepath='/'):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_path, template_path, dest_path = os.path.join(basepath,from_path),os.path.join(basepath,template_path),os.path.join(basepath,dest_path)
    if not os.path.exists(from_path) or not os.path.exists(template_path):
        raise FileNotFoundError(f"{from_path} or {template_path} doesnt exist")
    src, template = "",""
    with open(from_path,'r') as f:
        src= f.read()
    with open(template_path,'r') as f:
        template=f.read()
    
    content = markdown_to_html_node(src).to_html()
    title = extract_title(src)
    final_doc = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    final_doc = final_doc.replace("href=\"/",f"href=\"{basepath}").replace("src=\"/",f"src=\"{basepath}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path,'w') as f:
        f.write(final_doc)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath='/'):
    for item in os.listdir(os.path.join(basepath,dir_path_content)):
        item_path = os.path.join(dir_path_content,item)
        dest_item_path = os.path.join(dest_dir_path,item)
        if os.path.isfile(os.path.join(basepath,item_path)):
            generate_page(item_path,template_path,dest_item_path.replace('.md','.html'),basepath=basepath)
        else:
            generate_pages_recursive(item_path,template_path,dest_item_path,basepath=basepath)

def clean(verbose=False):
    root = Path(__file__).parent.parent.resolve()
    public = root / "docs/"
    static = root / "static/"
    if os.path.exists(public):
        shutil.rmtree(public)
    def copy_file(src_path, dest_path,verbose=False):
        os.makedirs(os.path.dirname(dest_path),exist_ok=True)
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"No file as {src_path}")
        if not os.path.isfile(src_path):
            raise ValueError(f"Expected {src_path} to be a file")
        shutil.copy(src_path,dest_path)
        if verbose:
            print(f"Copied {src_path} to {dest_path}")
    def copy_dir(src, dest, verbose=False):
        if not os.path.exists(src):
            raise NotADirectoryError(f"We've been tricked in {src}")
        for child in os.listdir(src):
            src_path, dest_path = os.path.join(src,child), os.path.join(dest,child)
            if os.path.isfile(src_path):
                copy_file(src_path,dest_path,verbose)
            else:
                copy_dir(src_path,dest_path,verbose)
        if verbose:
            print(f"Succesfully copied {src} to {dest}")        
    copy_dir(static,public,verbose)


def main():
    TextNode1 = TextNode("Hello", TextType.TEXT, "")
    print(TextNode1)
    parser = argparse.ArgumentParser(description="static site generator")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("basepath",type=str,help="basepath",default="/")
    args = parser.parse_args()
    clean(args.verbose)
    basepath=args.basepath
    generate_pages_recursive("content","template.html","docs",basepath=basepath)

if __name__ == "__main__":
    main()