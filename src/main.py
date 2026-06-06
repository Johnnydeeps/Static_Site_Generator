import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive


def main():
    # changing base path to host on github.com starting with the base setting as "/" which in this
    # case is the project root.
    base_path = "/"
    # sys.argv is always len() = 1 because we have to run the main.py so this will be sys.argv[0] so the next
    # index will be the additional argument which will contain github info that we want to pass use,
    # instead of the project root directory.
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    # functional logic to generate the pages
    # # changed destination from "public" to "docs" for github page generation
    copy_files_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", base_path)


if __name__ == "__main__":
    main()
