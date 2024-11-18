"""Auto generated code to produce an ast."""

import abc
from typing import Any

from app.tokens import Token


class Visitor(metaclass=abc.ABCMeta):
    """Interface Visitor."""

    # pylint: disable=R0801

    @classmethod
    def __subclasshook__(cls, subclass: Any) -> bool:
        """Check the subclasses."""
        subclasses = (
            hasattr(subclass, "accept")
            and callable(subclass.accept)
            and hasattr(subclass, "visit_assign_expr")
            and callable(subclass.visit_assign_expr)
            and hasattr(subclass, "visit_binary_expr")
            and callable(subclass.visit_binary_expr)
            and hasattr(subclass, "visit_grouping_expr")
            and callable(subclass.visit_grouping_expr)
            and hasattr(subclass, "visit_literal_expr")
            and callable(subclass.visit_literal_expr)
            and hasattr(subclass, "visit_unary_expr")
            and callable(subclass.visit_unary_expr)
            and hasattr(subclass, "visit_variable_expr")
            and callable(subclass.visit_variable_expr)
        )
        return subclasses

    @abc.abstractmethod
    def visit_assign_expr(self, _expr: "AssignExpr") -> Any:
        """Visitor visit_assign_expr."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_binary_expr(self, _expr: "BinaryExpr") -> Any:
        """Visitor visit_binary_expr."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_grouping_expr(self, _expr: "GroupingExpr") -> Any:
        """Visitor visit_grouping_expr."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_literal_expr(self, _expr: "LiteralExpr") -> Any:
        """Visitor visit_literal_expr."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_unary_expr(self, _expr: "UnaryExpr") -> Any:
        """Visitor visit_unary_expr."""
        raise NotImplementedError

    @abc.abstractmethod
    def visit_variable_expr(self, _expr: "VariableExpr") -> Any:
        """Visitor visit_variable_expr."""
        raise NotImplementedError


class Expr(abc.ABC):
    """Class Expr."""

    @abc.abstractmethod
    def accept(self, visitor: Visitor) -> Any:
        """Accept the node."""


class AssignExpr(Expr):
    """Class AssignExpr."""

    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_assign_expr(self)


class BinaryExpr(Expr):
    """Class BinaryExpr."""

    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_binary_expr(self)


class GroupingExpr(Expr):
    """Class GroupingExpr."""

    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_grouping_expr(self)


class LiteralExpr(Expr):
    """Class LiteralExpr."""

    def __init__(self, value: object) -> None:
        self.value = value

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_literal_expr(self)


class UnaryExpr(Expr):
    """Class UnaryExpr."""

    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_unary_expr(self)


class VariableExpr(Expr):
    """Class VariableExpr."""

    def __init__(self, name: Token) -> None:
        self.name = name

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_variable_expr(self)
