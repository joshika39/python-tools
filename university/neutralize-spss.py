import os
import argparse
import re


# This file meant to convert the string values from lime survey to numeric values for SPSS
# e.g. "A1" -> 1, "A2" -> 2, "A3" -> 3, "A4" -> 4, "A5" -> 5

def regex_replace_word(text: str, word: str, replacement: str) -> str:
    """
    Replace a word in a text using regex

    Replacing A2 with F2
    Replaces A2 with F2 but not A21 with F2
    """
    return re.sub(rf"\b{word}\b", replacement, text)

def neutralize_data(file: str, overwrite: bool = False):
    with open(file, "r") as f:
        content = f.read()

    for i in range(1, 10):
        content = content.replace(f"'A{i}'", str(i))
        content = content.replace(f'"A{i}"', str(i))

    if overwrite:
        with open(file, "w") as f:
            f.write(content)
    else:
        name, extension = os.path.splitext(file)
        with open(f"{name}_neutralized{extension}", "w") as f:
            f.write(content)

def neutralize_sps(file: str, overwrite: bool = False):
    with open(file, "r") as f:
        content = f.read()

    for i in range(1, 10):
        content = regex_replace_word(content, f"'A{i}'", str(i))
        content = regex_replace_word(content, f'"A{i}"', str(i))

    content = regex_replace_word(content, "A1", "F1")
    content = regex_replace_word(content, "A2", "F2")

    if overwrite:
        with open(file, "w") as f:
            f.write(content)
    else:
        name, extension = os.path.splitext(file)
        with open(f"{name}_neutralized{extension}", "w") as f:
            f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description="Neutralize the string values from lime survey to numeric values for SPSS")
    parser.add_argument("file", type=str, help="The file to neutralize")
    parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite the original file")
    args = parser.parse_args()

    if args.file.endswith(".sps"):
        neutralize_sps(args.file, args.overwrite)
    else:
        neutralize_data(args.file, args.overwrite)


if __name__ == "__main__":
    main()
