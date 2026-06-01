def markdown_to_blocks(markdown):
    # remove block separation, ie. new paragraphs "\n\n" in md text.
    markdown_split = markdown.split("\n\n")
    # removing any potential whitespace ie. " " with .strip()
    striped_blocks = []
    for block in markdown_split:
        # When you call .strip() with no arguments, it strips all leading and
        # trailing whitespace — spaces, tabs, newlines (\n), carriage returns, etc.
        strip_result = block.strip()
        if strip_result:
            striped_blocks.append(strip_result)
        else:
            continue
    return striped_blocks
