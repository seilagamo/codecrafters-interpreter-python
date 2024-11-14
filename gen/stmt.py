"""Auto generated code to produce an ast."""

import abc
from typing import Any

from app.tokens import Token

from .expr import Expr


class Visitor(metaclass=abc.ABCMeta):
    """Interface Visitor."""

    @classmethod
    def __subclasshook__(cls, subclass: Any) -> bool:
        """Check the subclasses."""
        subclasses = (
            hasattr(subclass, "accept")
            and callable(subclass.accept)
            and hasattr(subclass, "visit_expression_stmt")
            and callable(subclass.visit_expression_stmt)
            and hasattr(subclass, "visit_print_stmt")
            and callable(subclass.visit_print_stmt)
            and hasattr(subclass, "visit_var_stmt")
            and callable(subclass.visit_var_stmt)
        )
        return subclasses

    @abc.abstractmethod
    def visit_expression_stmt(self, _stmt: "ExpressionStmt") -> Any:
        """Visitor visit_expression_stmt."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_print_stmt(self, _stmt: "PrintStmt") -> Any:
        """Visitor visit_print_stmt."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_var_stmt(self, _stmt: "VarStmt") -> Any:
        """Visitor visit_var_stmt."""
        raise NotImplementedError


class Stmt(abc.ABC):
    """Class Stmt."""

    @abc.abstractmethod
    def accept(self, visitor: Visitor) -> Any:
        """Accept the node."""


class ExpressionStmt(Stmt):
    """Class ExpressionStmt."""

    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_expression_stmt(self)


class PrintStmt(Stmt):
    """Class PrintStmt."""

    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_print_stmt(self)


class VarStmt(Stmt):
    """Class VarStmt."""

    def __init__(self, name: Token, initializer: Expr | None) -> None:
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_var_stmt(self)
