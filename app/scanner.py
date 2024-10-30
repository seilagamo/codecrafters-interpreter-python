"""Scanner

This module contains the functionality to scan a string.

"""

from . import tokens


class Scanner:
    """Scanner"""

    def __init__(self, source: str) -> None:
        self.source: str = source
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.tokens: list[tokens.Token] = []
        self.lexical_errors: list[str] = []

    def is_at_end(self) -> bool:
        """Check if we are at the end of the source."""
        return self.current >= len(self.source)

    def scan_tokens(self) -> list[tokens.Token]:
        """Scan the tokens."""
        while not self.is_at_end():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.scan_token()
        self.tokens.append(
            tokens.Token(tokens.TokenType.EOF, "", None, self.line)
        )
        return self.tokens

    def scan_token(self) -> None:
        """Scan a token."""
        c: str = self.advance()
        match c:
            case "(":
                self.add_token(tokens.TokenType.LEFT_PAREN)
            case ")":
                self.add_token(tokens.TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(tokens.TokenType.LEFT_BRACE)
            case "}":
                self.add_token(tokens.TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(tokens.TokenType.COMMA)
            case ".":
                self.add_token(tokens.TokenType.DOT)
            case "-":
                self.add_token(tokens.TokenType.MINUS)
            case "+":
                self.add_token(tokens.TokenType.PLUS)
            case ";":
                self.add_token(tokens.TokenType.SEMICOLON)
            case "*":
                self.add_token(tokens.TokenType.STAR)
            case "!":
                self.add_token(
                    tokens.TokenType.BANG_EQUAL
                    if self.match("=")
                    else tokens.TokenType.BANG
                )
            case "=":
                self.add_token(
                    tokens.TokenType.EQUAL_EQUAL
                    if self.match("=")
                    else tokens.TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    tokens.TokenType.LESS_EQUAL
                    if self.match("=")
                    else tokens.TokenType.LESS
                )
            case ">":
                self.add_token(
                    tokens.TokenType.GREATER_EQUAL
                    if self.match("=")
                    else tokens.TokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    # A comment goes until the end of the line.
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(tokens.TokenType.SLASH)
            case _:
                self.add_lexical_error(c)

    def advance(self) -> str:
        """Advance a character."""
        c = self.source[self.current]
        self.current += 1
        return c

    def match(self, expected: str) -> bool:
        """
        It's like a conditional advance(). We only consume the current character
          if it's what we're looking for.
        """
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        """Advance but doesn't consume the character."""
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def add_token(
        self, token_type: tokens.TokenType, literal: object = None
    ) -> None:
        """Add a token to the token list."""
        text: str = self.source[self.start : self.current]
        self.tokens.append(tokens.Token(token_type, text, literal, self.line))

    def add_lexical_error(self, c: str) -> None:
        """Add an error to the lexical error list."""
        self.lexical_errors.append(
            f"[line {self.line}] Error: Unexpected character: {c}"
        )
