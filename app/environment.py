"""Environment.

The bindings that associate variables to values.
"""

from .exceptions import InterpreterError
from .tokens import Token


class Environment:
    """Environment."""

    def __init__(self) -> None:
        self.values: dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        """Define the value of a variable."""
        self.values[name] = value

    def get(self, name: Token) -> object:
        """Get the value of a variable."""
        if name.lexeme not in self.values:
            raise InterpreterError(
                name, "Undefined variable '" + name.lexeme + "'."
            )
        return self.values.get(name.lexeme)
