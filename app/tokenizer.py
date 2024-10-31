"""Tokenizer

Collection of functions to manage the tokens returned by the scan.

"""

import sys

from . import scanner, tokens


def tokenize(content: str) -> None:
    """Tokenize and print the content."""
    if content:
        toks, lexical_errors = scan(content)
        print_lexical_errors(lexical_errors)
        print_tokens(toks)
        if lexical_errors:
            sys.exit(65)
    else:
        print("EOF  null")


def tokens_to_string(toks: list[tokens.Token]) -> str:
    """Transform a list of tokens in a string."""
    return "\n".join([str(x) for x in toks])


def print_tokens(toks: list[tokens.Token]) -> None:
    """Print a list of tokens."""
    print(tokens_to_string(toks))


def print_lexical_errors(errors: list[str]) -> None:
    """Print a list of lexical errors"""
    for error in errors:
        print(error, file=sys.stderr)


def scan(contents: str) -> tuple[list[tokens.Token], list[str]]:
    """Scan a string.

    Return a tuple containing the list of tokens and
    the list of lexical errors"""
    sc = scanner.Scanner(contents)
    return sc.scan_tokens(), sc.lexical_errors
