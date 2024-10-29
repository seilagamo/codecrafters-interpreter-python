"""Tokenizer

Collection of functions to manage the tokens returned by the scan.

"""

from . import scanner, tokens


def tokens_to_string(toks: list[tokens.Token]) -> str:
    """Transform a list of tokens in a string."""
    return "\n".join([str(x) for x in toks])


def print_tokens(toks: list[tokens.Token]) -> None:
    """Print a list of tokens."""
    print(tokens_to_string(toks))


def scan(contents: str) -> list[tokens.Token]:
    """Scan a string."""
    sc = scanner.Scanner(contents)
    return sc.scan_tokens()
