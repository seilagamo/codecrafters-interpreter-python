"""Interpreter

Module to evaluate.
"""

import sys
from typing import Any

from gen import expr, stmt

from . import parser
from .tokens import Token, TokenType


class Interpreter(expr.Visitor[object], stmt.Visitor[None]):
    """Interpreter"""

    class InterpreterError(RuntimeError):
        """A custom exception for interpreter errors."""

        def __init__(self, token: Token, msg: str) -> None:
            super().__init__(msg)
            self.msg = msg
            self.token = token

    def __init__(self, _statements: list[stmt.Stmt[Any]] | None = None):
        self._statements = _statements
        self.runtime_errors: list[str] = []

    def interpret(self) -> None:
        """Interpret a list of statements."""
        if self._statements is None:
            return
        try:
            for statement in self._statements:
                self._execute(statement)
        except Interpreter.InterpreterError as e:
            self.runtime_error(e)

    def visit_binary_expr(self, _expr: "expr.BinaryExpr[Any]") -> Any:
        left = self.evaluate(_expr.left)
        right = self.evaluate(_expr.right)

        value: bool | float | str | None = None
        match _expr.operator.type:
            case TokenType.GREATER:
                _check_number_operands(_expr.operator, left, right)
                value = float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                _check_number_operands(_expr.operator, left, right)
                value = float(left) >= float(right)
            case TokenType.LESS:
                _check_number_operands(_expr.operator, left, right)
                value = float(left) < float(right)
            case TokenType.LESS_EQUAL:
                _check_number_operands(_expr.operator, left, right)
                value = float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                value = not isequal(left, right)
            case TokenType.EQUAL_EQUAL:
                value = isequal(left, right)
            case TokenType.MINUS:
                _check_number_operands(_expr.operator, left, right)
                value = float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    value = float(left) + float(right)
                elif isinstance(left, str) and isinstance(right, str):
                    value = str(left) + str(right)
                else:
                    raise Interpreter.InterpreterError(
                        _expr.operator,
                        "Operands must be two numbers or two strings.",
                    )
            case TokenType.SLASH:
                _check_number_operands(_expr.operator, left, right)
                value = float(left) / float(right)
            case TokenType.STAR:
                _check_number_operands(_expr.operator, left, right)
                value = float(left) * float(right)

        return value

    def visit_grouping_expr(self, _expr: "expr.GroupingExpr[Any]") -> Any:
        return self.evaluate(_expr.expression)

    def visit_literal_expr(self, _expr: "expr.LiteralExpr[Any]") -> Any:
        return _expr.value

    def visit_unary_expr(self, _expr: "expr.UnaryExpr[Any]") -> Any:
        right = self.evaluate(_expr.right)

        match _expr.operator.type:
            case TokenType.BANG:
                return not istruthy(right)
            case TokenType.MINUS:
                _check_number_operand(_expr.operator, right)
                return -float(right)

        # Unreachable.
        return None

    def visit_expression_stmt(self, _stmt: "stmt.ExpressionStmt[Any]") -> None:
        self.evaluate(_stmt.expression)

    def visit_print_stmt(self, _stmt: "stmt.PrintStmt[Any]") -> None:
        value = self.evaluate(_stmt.expression)
        print(stringify(value))

    def evaluate(self, _expr: expr.Expr[Any]) -> Any:
        """Evaluate an expression."""
        return _expr.accept(self)

    def runtime_error(self, err: InterpreterError) -> None:
        """Create a runtime error."""
        self.runtime_errors.append(f"{err.msg}\n[line {err.token.line}]")

    def _execute(self, _stmt: stmt.Stmt[Any]) -> None:
        _stmt.accept(self)


def istruthy(obj: Any) -> bool:
    """Check if an object is an istruthy expression."""
    if obj is None:
        return False
    if isinstance(obj, bool):
        return bool(obj)
    return True


def isequal(left: Any, right: Any) -> bool:
    """Compare if two objects are equals."""
    if left is None and right is None:
        return True
    if left is None:
        return False
    outcome: bool = left == right
    return outcome


def _check_number_operand(operator: Token, operand: Any) -> None:
    """Check if an operand is a number."""
    if isinstance(operand, float):
        return
    raise Interpreter.InterpreterError(operator, "Operand must be a number.")


def _check_number_operands(operator: Token, left: Any, right: Any) -> None:
    """Check if both operands are numbers."""
    if isinstance(left, float) and isinstance(right, float):
        return
    raise Interpreter.InterpreterError(operator, "Operands must be numbers.")


def stringify(obj: Any) -> str:
    """Convert an object to a string."""
    if obj is None:
        return "nil"

    if isinstance(obj, float):
        text = str(obj)
        if text.endswith(".0"):
            text = text[0 : len(text) - 2]
        return text

    if isinstance(obj, bool):
        return str(obj).lower()

    return str(obj)


def interpret_cmd(content: str) -> None:
    """Interpret command."""
    value, runtime_errors = _interpret(content)
    if runtime_errors:
        _print_runtime_errors(runtime_errors)
        sys.exit(70)
    print(stringify(value))


def _interpret(content: str) -> tuple[Any, list[str]]:
    """Interpret the content."""
    expression, parse_errors = parser.parse_expression(content)
    if parse_errors:
        sys.exit(65)
    if expression is not None:
        interpreter = Interpreter()
        value = None
        try:
            value = interpreter.evaluate(expression)
        except Interpreter.InterpreterError as e:
            interpreter.runtime_error(e)
        return value, interpreter.runtime_errors
    return None, []


def run_cmd(content: str) -> None:
    """Run command."""
    runtime_errors = _run(content)
    if runtime_errors:
        _print_runtime_errors(runtime_errors)
        sys.exit(70)


def _run(content: str) -> list[str]:
    """Interpret the content."""
    statements, parse_errors = parser.parse(content)
    if parse_errors:
        sys.exit(65)
    if statements:
        interpreter = Interpreter(statements)
        interpreter.interpret()
        return interpreter.runtime_errors
    return []


def _print_runtime_errors(errors: list[str]) -> None:
    """Print a list of runtime errors"""
    for error in errors:
        print(error, file=sys.stderr)
