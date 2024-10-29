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
        self.line: int = 0
        self.tokens: list[tokens.Token] = []

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
            case _:
                raise ValueError(f"Line: {self.line}: Unexpected character.")

    def advance(self) -> str:
        """Advance a character."""
        c = self.source[self.current]
        self.current += 1
        return c

    def add_token(
        self, token_type: tokens.TokenType, literal: object = None
    ) -> None:
        """Add a token to the token list."""
        text: str = self.source[self.start : self.current]
        self.tokens.append(tokens.Token(token_type, text, literal, self.line))
