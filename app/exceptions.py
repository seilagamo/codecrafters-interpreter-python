"""Lox Interpreter exceptions."""

from .tokens import Token


class InterpreterError(RuntimeError):
    """A custom exception for interpreter errors."""

    def __init__(self, token: Token, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg
        self.token = token
