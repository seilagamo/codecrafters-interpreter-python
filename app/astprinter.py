"""
Convert a tree to a string.
"""

from gen import expr

from .tokens import Token, TokenType


class AstPrinter(expr.Visitor):
    """Ast Printer
    Convert a tree to string.
    """

    def print(self, _expr: expr.Expr) -> object:
        """Print"""
        return _expr.accept(self)

    def visit_binary_expr(self, _expr: expr.BinaryExpr) -> str:
        """Visit Binary Expression"""
        return self.parenthesize(_expr.operator.lexeme, _expr.left, _expr.right)

    def visit_grouping_expr(self, _expr: expr.GroupingExpr) -> str:
        """Visit Grouping Expression"""
        return self.parenthesize("group", _expr.expression)

    def visit_literal_expr(self, _expr: expr.LiteralExpr) -> object:
        """Visit Literal Expression"""
        if _expr.value is None:
            return "nil"
        if isinstance(_expr.value, bool):
            return str(_expr.value).lower()
        return str(_expr.value)

    def visit_unary_expr(self, _expr: expr.UnaryExpr) -> str:
        """Visit Unary Expression"""
        return self.parenthesize(_expr.operator.lexeme, _expr.right)

    def visit_variable_expr(self, _expr: "expr.VariableExpr") -> str:
        """Visit Variable Expression"""
        return self.parenthesize(_expr.name.lexeme)

    def parenthesize(self, name: str, *exprs: expr.Expr) -> str:
        """Parenthesize"""
        builder: str = f"({name}"

        for _expr in exprs:
            builder += " "
            builder += str(_expr.accept(self))

        builder += ")"

        return builder


expr.Visitor.register(AstPrinter)


def main() -> None:
    expression = expr.BinaryExpr(
        expr.UnaryExpr(
            Token(TokenType.MINUS, "-", None, 1),
            expr.LiteralExpr(123),
        ),
        Token(TokenType.STAR, "*", None, 1),
        expr.GroupingExpr(expr.LiteralExpr(45.67)),
    )

    print(AstPrinter().print(expression))


if __name__ == "__main__":
    main()
