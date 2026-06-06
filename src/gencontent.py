import os
from pathlib import Path

from markdown_to_blocks import markdown_to_html_node


# extracts the raw text from the h1 title heading from the markdown.md text passed
# into the function.
def extract_title(markdown_text):
    lines = markdown_text.split("\n")

    for line in lines:
        if line.startswith("# "):
            title_text = line[2:]
            striped_title_text = title_text.strip()
            return striped_title_text
    raise Exception("no title found in markdown text")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # open and read (store in memory) the source file
    open_contents = open(from_path)
    contents = open_contents.read()
    open_contents.close()

    # open and read (store in memory) the template file
    open_contents_template = open(template_path)
    contents_template = open_contents_template.read()
    open_contents_template.close()

    # convert markdown contents into html using the helpers previously made
    contents_html_nodes = markdown_to_html_node(contents)
    html_string = contents_html_nodes.to_html()
    title = extract_title(contents)

    # converted markdown inserted into the template file
    replaced_title = contents_template.replace("{{ Title }}", title)
    replaced_html_string = replaced_title.replace("{{ Content }}", html_string)

    # **** Swaps the root-absolute paths (href="/ and src="/) so they point to the
    # repo subfolder on GitHub Pages instead of the domain root.
    # e.g. href="/index.css" becomes href="/Static_Site_Generator/index.css"
    # The browser adds the domain (https://Johnnydeeps.github.io) on its own. ****
    replaced_html_string = replaced_html_string.replace('href="/', f'href="{basepath}')
    replaced_html_string = replaced_html_string.replace('src="/', f'src="{basepath}')

    # takes the full path to a file ie. public/blog/majesty/index.html and removes the file name
    # leaving just the full path in the project folder and stores the path as a string in dir_name.
    dir_name = os.path.dirname(dest_path)

    #  **** checks if the string passed into the functino ie. dir_name is not empty ie. something was
    # passed into the fucntion call, it then creates the directory # ie. public/blog/majesty
    # established at the path above with dir_name = os.path.dirname(dest_path). ****
    if dir_name:
        # creates the directory on the computer with the file path in dir_name,
        # exist_ok=True allows python to continue if the directory is already present at the specified
        # file path. Directories need to be made first in order to write a file there or python
        # will crash.
        os.makedirs(dir_name, exist_ok=True)

    # we know the dest_path has a directory that either exists or has just been created
    # open(some_arg, "w") where "w" means write, will also create (ie. touch in CLI) a file with the
    # specified name ie. index.html if there is not one already. we then write all the above
    # information that is stored in memory with replaced_html_string to the file and close it.
    open_dest_path_file = open(dest_path, "w")
    open_dest_path_file.write(replaced_html_string)
    open_dest_path_file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # create an iterable list of strings corresponding to the files and directories at the specified
    # filepath string passed in as an argument to generate_pages_recursive() ie. dir_path_content
    filenames = os.listdir(dir_path_content)
    for filename in filenames:
        # for each of the list entries in filenames (ie. the list of directories and files at
        # dir_path_content) create the full file path and store it in memory.
        # ie. public/blog/majesty/index.html for dest_dir_path or source content for the same file
        # content/blog/majesty/index.md.
        full_path_content = os.path.join(dir_path_content, filename)
        full_path_destination = os.path.join(dest_dir_path, filename)

        # if there is a file at the full_path_content(ie. there is a source file in /content in this case)
        # that is passed into generate_page, with the destination file path contained as a value on a
        # Path object, which allows the use of the .with_suffix() method to change the file type ie.
        # .md => .html in this case. which is passed in as path_object_html to generate_page.
        if os.path.isfile(full_path_content):
            path_object = Path(full_path_destination)
            path_object_html = path_object.with_suffix(".html")
            generate_page(full_path_content, template_path, path_object_html, basepath)
        # if filename in the above for loop is not a file, else: triggers recursively until we find
        # another file.
        else:
            generate_pages_recursive(
                full_path_content, template_path, full_path_destination, basepath
            )
