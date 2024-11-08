"""
Convert a tree to a string.
"""

from gen import expr

from . import tokens


class AstPrinter(expr.Visitor[str]):
    """Ast Printer
    Convert a tree to string.
    """

    def print(self, _expr: expr.Expr[str]) -> str:
        """Print"""
        return _expr.accept(self)

    def visit_binary_expr(self, _expr: expr.BinaryExpr[str]) -> str:
        """Visit Binary Expression"""
        return self.parenthesize(_expr.operator.lexeme, _expr.left, _expr.right)

    def visit_grouping_expr(self, _expr: expr.GroupingExpr[str]) -> str:
        """Visit Grouping Expression"""
        return self.parenthesize("group", _expr.expression)

    def visit_literal_expr(self, _expr: expr.LiteralExpr[str]) -> str:
        """Visit Literal Expression"""
        if _expr.value is None:
            return "nil"
        if isinstance(_expr.value, bool):
            return str(_expr.value).lower()
        return str(_expr.value)

    def visit_unary_expr(self, _expr: expr.UnaryExpr[str]) -> str:
        """Visit Unary Expression"""
        return self.parenthesize(_expr.operator.lexeme, _expr.right)

    def parenthesize(self, name: str, *exprs: expr.Expr[str]) -> str:
        """Parenthesize"""
        builder: str = f"({name}"

        for _expr in exprs:
            builder += " "
            builder += _expr.accept(self)

        builder += ")"

        return builder


expr.Visitor.register(AstPrinter)


def main() -> None:
    expression = expr.BinaryExpr[str](
        expr.UnaryExpr[str](
            tokens.Token(tokens.TokenType.MINUS, "-", None, 1),
            expr.LiteralExpr[str](123),
        ),
        tokens.Token(tokens.TokenType.STAR, "*", None, 1),
        expr.GroupingExpr[str](expr.LiteralExpr[str](45.67)),
    )

    print(AstPrinter().print(expression))


if __name__ == "__main__":
    main()
