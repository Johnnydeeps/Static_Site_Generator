from copystatic import copy_files_recursive


def main():
    copy_files_recursive("static", "public")


if __name__ == "__main__":
    main()
