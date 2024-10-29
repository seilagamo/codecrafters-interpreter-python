"""Lox interpreter

This is a interpreted based on the book Crafting Interpreters.

"""

import sys

from . import tokenizer


def main() -> None:
    # You can use print statements as follows for debugging, they'll be visible
    # when running tests.

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

    with open(filename, encoding="utf-8") as file:
        file_contents = file.read()

    # Uncomment this block to pass the first stage
    if file_contents:
        tokens = tokenizer.scan(file_contents)
        tokenizer.print_tokens(tokens)
    else:
        print("EOF  null")


if __name__ == "__main__":
    main()
