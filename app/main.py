"""Lox interpreter

This is an interpreted based on the book Crafting Interpreters.

"""

import sys

from . import interpreter, parser, scanner


def main() -> None:

    if len(sys.argv) < 3:
        printhelp()
        sys.exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    match command:
        case "tokenize":
            scanner.tokenize_cmd(get_contents_from_file(filename))
        case "parse":
            parser.parse_cmd(get_contents_from_file(filename))
        case "evaluate":
            interpreter.interpret_cmd(get_contents_from_file(filename))
        case "run":
            interpreter.run_cmd(get_contents_from_file(filename))
        case _:
            print(f"Unknown command: {command}", file=sys.stderr)
            printhelp()
            sys.exit(1)


def get_contents_from_file(filename: str) -> str:
    """Read a file and extract its content."""
    with open(filename, encoding="utf-8") as file:
        file_contents = file.read()
    return file_contents


def printhelp() -> None:
    """Print the help."""
    print(
        """
usage: ./your_program.sh <command> <filename>

Available commands:
    tokenize    Tokenize the input
    parse       Parse the input
    evaluate    Evaluate the input
""",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
