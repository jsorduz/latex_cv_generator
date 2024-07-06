import os


def create_file_if_not_exists(path):
    if not os.path.exists(path):
        with open(path, "w+") as file:
            file.write("")


def remove_left_spaces(text: str, separator: str = "\n"):
    return separator.join(line.lstrip() for line in text.split(separator))
