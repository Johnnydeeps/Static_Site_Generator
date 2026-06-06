from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive


def main():
    copy_files_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
