"""Environment.

The bindings that associate variables to values.
"""

from .exceptions import InterpreterError
from .tokens import Token


class Environment:
    """Environment."""

    def __init__(self, enclosing: "Environment | None" = None) -> None:
        self._values: dict[str, object] = {}
        self.enclosing: Environment | None = enclosing

    def define(self, name: str, value: object) -> None:
        """Define the value of a variable."""
        self._values[name] = value

    def get(self, name: Token) -> object:
        """Get the value of a variable."""
        if name.lexeme not in self._values:
            if self.enclosing is not None:
                return self.enclosing.get(name)
            raise InterpreterError(
                name, "Undefined variable '" + name.lexeme + "'."
            )
        return self._values.get(name.lexeme)

    def assign(self, name: Token, value: object) -> None:
        """Assign the value of a variable."""
        if name.lexeme in self._values:
            self._values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise InterpreterError(name, f"Undefined variable '{name.lexeme}'.")
