"""Auto generated code to produce an ast."""

import abc
from typing import Any

from app.tokens import Token


class Visitor[T](metaclass=abc.ABCMeta):
    """Interface Visitor."""

    @classmethod
    def __subclasshook__(cls, subclass: Any) -> bool:
        """Check the subclases."""
        subclasses = (
            hasattr(subclass, "accept")
            and callable(subclass.accept)
            and hasattr(subclass, "visit_binary_expr")
            and callable(subclass.visit_binary_expr)
            and hasattr(subclass, "visit_grouping_expr")
            and callable(subclass.visit_grouping_expr)
            and hasattr(subclass, "visit_literal_expr")
            and callable(subclass.visit_literal_expr)
            and hasattr(subclass, "visit_unary_expr")
            and callable(subclass.visit_unary_expr)
        )
        return subclasses

    @abc.abstractmethod
    def visit_binary_expr(self, _expr: "BinaryExpr[T]") -> T:
        """Visitor visit_binary_expr."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_grouping_expr(self, _expr: "GroupingExpr[T]") -> T:
        """Visitor visit_grouping_expr."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_literal_expr(self, _expr: "LiteralExpr[T]") -> T:
        """Visitor visit_literal_expr."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_unary_expr(self, _expr: "UnaryExpr[T]") -> T:
        """Visitor visit_unary_expr."""
        raise NotImplementedError


class Expr[T](abc.ABC):
    """Class Expr."""

    @abc.abstractmethod
    def accept(self, visitor: Visitor[T]) -> T:
        """Accept the node."""


class BinaryExpr[T](Expr[T]):
    """Class BinaryExpr."""

    def __init__(self, left: Expr[T], operator: Token, right: Expr[T]) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_binary_expr(self)


class GroupingExpr[T](Expr[T]):
    """Class GroupingExpr."""

    def __init__(self, expression: Expr[T]) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_grouping_expr(self)


class LiteralExpr[T](Expr[T]):
    """Class LiteralExpr."""

    def __init__(self, value: object) -> None:
        self.value = value

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_literal_expr(self)


class UnaryExpr[T](Expr[T]):
    """Class UnaryExpr."""

    def __init__(self, operator: Token, right: Expr[T]) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_unary_expr(self)
