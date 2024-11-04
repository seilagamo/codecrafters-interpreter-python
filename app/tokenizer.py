"""Tokenizer

Collection of functions to manage the tokens returned by the scan.

"""

import sys

from . import scanner
from .tokens import Token


def tokenize(content: str) -> None:
    """Tokenize and print the content."""
    if content:
        tokens, lexical_errors = scan(content)
        print_lexical_errors(lexical_errors)
        print_tokens(tokens)
        if lexical_errors:
            sys.exit(65)
    else:
        print("EOF  null")


def tokens_to_string(tokens: list[Token]) -> str:
    """Transform a list of tokens in a string."""
    return "\n".join([str(x) for x in tokens])


def print_tokens(tokens: list[Token]) -> None:
    """Print a list of tokens."""
    print(tokens_to_string(tokens))


def print_lexical_errors(errors: list[str]) -> None:
    """Print a list of lexical errors"""
    for error in errors:
        print(error, file=sys.stderr)


def scan(contents: str) -> tuple[list[Token], list[str]]:
    """Scan a string.

    Return a tuple containing the list of tokens and
    the list of lexical errors"""
    sc = scanner.Scanner(contents)
    return sc.scan_tokens(), sc.lexical_errors
