"""Tools to generate an ast
"""

import sys
from pathlib import Path


def main() -> None:

    if len(sys.argv) not in [2, 3]:
        printhelp()
        sys.exit(64)

    command = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) == 3 else "gen"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Creates the init file
    with open(Path(output_dir) / "__init__.py", "w", encoding="utf-8"):
        pass

    match command:
        case "generate_ast":
            basename = "Expr"
            ast = define_ast(
                basename,
                [
                    "Binary   : Expr[T] left, Token operator, Expr[T] right",
                    "Grouping : Expr[T] expression",
                    "Literal  : object value",
                    "Unary    : Token operator, Expr[T] right",
                ],
            )
            path = Path(output_dir) / f"{basename.lower()}.py"
            with open(path, "w", encoding="utf-8") as file:
                file.writelines(ast)

        case _:
            print(f"Unknown command: {command}", file=sys.stderr)
            printhelp()
            sys.exit(1)


def define_ast(basename: str, types: list[str]) -> list[str]:
    """Define the ast."""
    ast = [
        "import abc\n",
        "from typing import Any\n",
        "from app.tokens import Token\n",
        "\n",
    ]
    ast.extend(define_visitor(basename, types))
    ast.extend(
        [
            f"class {basename}[T](abc.ABC):\n",
            "    @abc.abstractmethod\n",
            "    def accept(self, visitor: Visitor[T]) -> T:\n",
            "        pass\n\n",
        ]
    )

    # The AST classes.
    for _type in types:
        classname = _type.split(":")[0].strip()
        fields = _type.split(":")[1].strip()
        ast.extend(define_type(basename, classname, fields))
    return ast


def define_type(basename: str, classname: str, fieldlist: str) -> list[str]:
    """Define the types."""
    fieldnames = [
        f"{field.split(" ")[1]}: {field.split(" ")[0]}"
        for field in fieldlist.split(", ")
    ]
    _type = [
        f"class {classname}{basename}[T]({basename}[T]):\n",
        f"    def __init__(self, {", ".join(fieldnames)}) -> None:\n",
    ]

    fields = fieldlist.split(", ")
    for field in fields:
        name = field.split(" ")[1]
        _type.append(f"        self.{name} = {name}\n")
    _type.append("\n")

    _type.extend(
        [
            "    def accept(self, visitor: Visitor[T]) -> T:\n",
            "        return visitor.visit_",
            f"{classname.lower()}_{basename.lower()}(self)\n\n",
        ]
    )

    return _type


def define_visitor(basename: str, types: list[str]) -> list[str]:
    """Generate the abstract class Visitor."""

    # visitors
    methods: list[str] = [
        "class Visitor[T](metaclass=abc.ABCMeta):\n",
        "    @classmethod\n",
        "    def __subclasshook__(cls, subclass: Any) -> bool:\n",
        "        subclasses = (\n",
    ]

    for _type in types:
        typename = _type.split(":")[0].strip().lower()
        methods.extend(
            [
                "            hasattr(subclass, ",
                f'"visit_{typename.lower()}_{basename.lower()}") and\n',
                "            callable(subclass.",
                f"visit_{typename.lower()}_{basename.lower()}) and\n",
            ]
        )

    methods.extend(
        [
            '            hasattr(subclass, "accept") and\n',
            "            callable(subclass.accept)\n",
            "        )\n",
            "        return (subclasses)\n",
            "\n",
        ]
    )

    for _type in types:
        typename = _type.split(":")[0].strip()
        methods.extend(
            [
                "    @abc.abstractmethod\n",
                f"    def visit_{typename.lower()}_{basename.lower()}",
                f"(self, _{basename.lower()}: {typename}{basename}[T]) -> T:\n",
                "        raise NotImplementedError\n",
                "\n",
            ]
        )

    return methods


def printhelp() -> None:
    """Print the help."""
    print(
        """
usage: generate_ast <output directory>
        """,
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
