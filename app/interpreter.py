"""Interpreter

Module to evaluate.
"""

import sys
from typing import Any

from gen import expr, stmt

from . import parser
from .environment import Environment
from .exceptions import InterpreterError
from .tokens import Token, TokenType


class Interpreter(expr.Visitor, stmt.Visitor):
    """Interpreter"""

    def __init__(self, _statements: list[stmt.Stmt | None] | None = None):
        self._statements = _statements
        self.runtime_errors: list[str] = []
        self._environment = Environment()

    def interpret(self) -> None:
        """Interpret a list of statements."""
        if self._statements is None:
            return
        try:
            for statement in self._statements:
                if statement is not None:
                    self._execute(statement)
        except InterpreterError as e:
            self.runtime_error(e)

    def visit_assign_expr(self, _expr: "expr.AssignExpr") -> object:
        value = self.evaluate(_expr.value)
        self._environment.assign(_expr.name, value)
        return value

    def visit_binary_expr(self, _expr: "expr.BinaryExpr") -> object:
        left = self.evaluate(_expr.left)
        right = self.evaluate(_expr.right)

        value: bool | float | str | None = None
        match _expr.operator.type:
            case TokenType.GREATER:
                left, right = _check_number_operands(
                    _expr.operator, left, right
                )
                value = left > right
            case TokenType.GREATER_EQUAL:
                left, right = _check_number_operands(
                    _expr.operator, left, right
                )
                value = left >= right
            case TokenType.LESS:
                left, right = _check_number_operands(
                    _expr.operator, left, right
                )
                value = left < right
            case TokenType.LESS_EQUAL:
                left, right = _check_number_operands(
                    _expr.operator, left, right
                )
                value = left <= right
            case TokenType.BANG_EQUAL:
                value = not isequal(left, right)
            case TokenType.EQUAL_EQUAL:
                value = isequal(left, right)
            case TokenType.MINUS:
                left, right = _check_number_operands(
                    _expr.operator, left, right
                )
                value = left - right
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    value = float(left) + float(right)
                elif isinstance(left, str) and isinstance(right, str):
                    value = str(left) + str(right)
                else:
                    raise InterpreterError(
                        _expr.operator,
                        "Operands must be two numbers or two strings.",
                    )
            case TokenType.SLASH:
                left, right = _check_number_operands(
                    _expr.operator, left, right
                )
                value = left / right
            case TokenType.STAR:
                left, right = _check_number_operands(
                    _expr.operator, left, right
                )
                value = left * right

        return value

    def visit_grouping_expr(self, _expr: "expr.GroupingExpr") -> object:
        return self.evaluate(_expr.expression)

    def visit_literal_expr(self, _expr: "expr.LiteralExpr") -> object:
        return _expr.value

    def visit_unary_expr(self, _expr: "expr.UnaryExpr") -> object:
        right = self.evaluate(_expr.right)

        match _expr.operator.type:
            case TokenType.BANG:
                return not istruthy(right)
            case TokenType.MINUS:
                right = _check_number_operand(_expr.operator, right)
                return -right

        # Unreachable.
        return None

    def visit_variable_expr(self, _expr: "expr.VariableExpr") -> object:
        return self._environment.get(_expr.name)

    def visit_expression_stmt(self, _stmt: "stmt.ExpressionStmt") -> None:
        self.evaluate(_stmt.expression)

    def visit_print_stmt(self, _stmt: "stmt.PrintStmt") -> None:
        value = self.evaluate(_stmt.expression)
        print(stringify(value))

    def visit_var_stmt(self, _stmt: "stmt.VarStmt") -> None:
        value = None
        if _stmt.initializer is not None:
            value = self.evaluate(_stmt.initializer)
        self._environment.define(_stmt.name.lexeme, value)

    def evaluate(self, _expr: expr.Expr) -> object:
        """Evaluate an expression."""
        return _expr.accept(self)

    def runtime_error(self, err: InterpreterError) -> None:
        """Create a runtime error."""
        self.runtime_errors.append(f"{err.msg}\n[line {err.token.line}]")

    def _execute(self, _stmt: stmt.Stmt) -> None:
        _stmt.accept(self)


expr.Visitor.register(Interpreter)
stmt.Visitor.register(Interpreter)


def istruthy(obj: object) -> bool:
    """Check if an object is an istruthy expression."""
    if obj is None:
        return False
    if isinstance(obj, bool):
        return bool(obj)
    return True


def isequal(left: object, right: object) -> bool:
    """Compare if two objects are equals."""
    if left is None and right is None:
        return True
    if left is None:
        return False
    outcome: bool = left == right
    return outcome


def _check_number_operand(operator: Token, operand: object) -> float:
    """Check if an operand is a number."""
    if isinstance(operand, float):
        return float(operand)
    raise InterpreterError(operator, "Operand must be a number.")


def _check_number_operands(
    operator: Token, left: object, right: object
) -> tuple[float, float]:
    """Check if both operands are numbers."""
    if isinstance(left, float) and isinstance(right, float):
        return float(left), float(right)
    raise InterpreterError(operator, "Operands must be numbers.")


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
        except InterpreterError as e:
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
        parser.print_parse_errors(parse_errors)
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
