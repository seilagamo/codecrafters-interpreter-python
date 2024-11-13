"""Auto generated code to produce an ast."""

import abc
from typing import Any

from .expr import Expr


class Visitor[T](metaclass=abc.ABCMeta):
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
        )
        return subclasses

    @abc.abstractmethod
    def visit_expression_stmt(self, _stmt: "ExpressionStmt[T]") -> T:
        """Visitor visit_expression_stmt."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_print_stmt(self, _stmt: "PrintStmt[T]") -> T:
        """Visitor visit_print_stmt."""
        raise NotImplementedError


class Stmt[T](abc.ABC):
    """Class Stmt."""

    @abc.abstractmethod
    def accept(self, visitor: Visitor[T]) -> T:
        """Accept the node."""


class ExpressionStmt[T](Stmt[T]):
    """Class ExpressionStmt."""

    def __init__(self, expression: Expr[T]) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_expression_stmt(self)


class PrintStmt[T](Stmt[T]):
    """Class PrintStmt."""

    def __init__(self, expression: Expr[T]) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_print_stmt(self)
