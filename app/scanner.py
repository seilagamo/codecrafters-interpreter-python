"""Scanner

This module contains the functionality to scan a string.

"""

import sys

from .tokens import KEYWORDS, Token, TokenType


class Scanner:
    """Scanner"""

    def __init__(self, source: str) -> None:
        self._source: str = source
        self._start: int = 0
        self._current: int = 0
        self._line: int = 1
        self._tokens: list[Token] = []
        self.lexical_errors: list[str] = []

    def _is_at_end(self) -> bool:
        """Check if we are at the end of the source."""
        return self._current >= len(self._source)

    def scan_tokens(self) -> list[Token]:
        """Scan the contents."""
        while not self._is_at_end():
            # We are at the beginning of the next lexeme.
            self._start = self._current
            self._scan_token()
        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens

    def _scan_token(self) -> None:
        """Scan a token."""
        c: str = self._advance()
        match c:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL
                    if self._match("=")
                    else TokenType.EQUAL
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL
                    if self._match("=")
                    else TokenType.GREATER
                )
            case "/":
                if self._match("/"):
                    # A comment goes until the end of the line.
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self._line += 1
            case '"':
                self._string()
            case c if c.isdigit():
                self._number()
            case c if isalpha(c):
                self._identifier()
            case _:
                self._lexical_error(f"Unexpected character: {c}")

    def _advance(self) -> str:
        """Advance a character."""
        c = self._source[self._current]
        self._current += 1
        return c

    def _match(self, expected: str) -> bool:
        """
        It's like a conditional advance(). We only consume the current character
          if it's what we're looking for.
        """
        if self._is_at_end():
            return False
        if self._source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _peek(self) -> str:
        """Advance but doesn't consume the character."""
        if self._is_at_end():
            return "\0"
        return self._source[self._current]

    def _peek_next(self) -> str:
        """Lookahead"""
        if self._current + 1 >= len(self._source):
            return "\0"
        return self._source[self._current + 1]

    def _add_token(self, token_type: TokenType, literal: object = None) -> None:
        """Add a token to the token list."""
        text: str = self._source[self._start : self._current]
        self._tokens.append(Token(token_type, text, literal, self._line))

    def _lexical_error(self, msg: str) -> None:
        """Add an error to the lexical error list."""
        self.lexical_errors.append(f"[line {self._line}] Error: {msg}")

    def _string(self) -> None:
        """
        We consume characters until we hit the " that ends the string. We also
        gracefully handle running out of input before the string is closed and
        report an error for that.
        """
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self._line += 1
            self._advance()

        if self._is_at_end():
            self._lexical_error("Unterminated string.")
            return

        # The closing ".
        self._advance()

        # Trim the surrounding quotes.
        value = self._source[self._start + 1 : self._current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self) -> None:
        """
        We consume as many digits as we find for the integer part of the
        literal. Then we look for a fractional part, which is a decimal
        point (.) followed by at least one digit. If we do have a fractional
        part, again, we consume as many digits as we can find.
        """
        while self._peek().isdigit():
            self._advance()

        # Look for a fractional part.
        if self._peek() == "." and self._peek_next().isdigit():
            #  Consume the "."
            self._advance()

            while self._peek().isdigit():
                self._advance()

        self._add_token(
            TokenType.NUMBER,
            float(self._source[self._start : self._current]),
        )

    def _identifier(self) -> None:
        """Consume an identifier."""
        while isalphanumeric(self._peek()):
            self._advance()

        text = self._source[self._start : self._current]
        token_type = KEYWORDS.get(text)
        if not token_type:
            token_type = TokenType.IDENTIFIER
        self._add_token(token_type)


def isalpha(c: str) -> bool:
    """Check if c is alphabetic or _"""
    return c.isalpha() or c == "_"


def isalphanumeric(c: str) -> bool:
    """Check if c is alphanumeric or _"""
    return isalpha(c) or c.isdigit()


def tokenize_cmd(content: str) -> None:
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
    sc = Scanner(contents)
    return sc.scan_tokens(), sc.lexical_errors
