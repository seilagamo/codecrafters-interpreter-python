"""Tools to generate an ast
"""

import sys
from pathlib import Path


def main() -> None:

    if len(sys.argv) not in [2, 3]:
        printhelp()
        sys.exit(64)

    command = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) == 3 else "ast"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    match command:
        case "generate_ast":
            base_name = "Expr"
            ast = define_ast(
                base_name,
                [
                    "Binary   : Expr left, Token operator, Expr right",
                    "Grouping : Expr expression",
                    "Literal  : Object value",
                    "Unary    : Token operator, Expr right",
                ],
            )
            path = Path(output_dir) / f"{base_name.lower()}.py"
            with open(path, "w", encoding="utf-8") as file:
                file.writelines(ast)

        case _:
            print(f"Unknown command: {command}", file=sys.stderr)
            printhelp()
            sys.exit(1)


def define_ast(base_name: str, types: list[str]) -> list[str]:
    """Define the ast."""
    ast = [
        "import abc\n",
        "\n",
        f"class {base_name}(abc.ABC):\n",
        "    pass\n",
        "\n",
    ]

    ast.extend(define_visitor())

    # The AST classes.
    for _type in types:
        classname = _type.split(":")[0].strip()
        fields = _type.split(":")[1].strip()
        ast.extend(define_type(base_name, classname, fields))
    return ast


def define_type(base_name: str, classname: str, fieldlist: str) -> list[str]:
    """Define the types."""
    fieldnames = [field.split(" ")[1] for field in fieldlist.split(", ")]
    _type = [
        f"class {classname}({base_name}):\n",
        f"    def __init__(self, {", ".join(fieldnames)}):\n",
    ]

    fields = fieldlist.split(", ")
    for field in fields:
        name = field.split(" ")[1]
        _type.append(f"        self.{name} = {name}\n")
    _type.append("\n")
    return _type


def define_visitor() -> list[str]:
    """Generate the abstract class Visitor."""
    return [
        "class Visitor(metaclass=abc.ABCMeta):\n",
        "    @classmethod\n",
        "    def __subclasshook__(cls, subclass):\n",
        "        return (hasattr(subclass, 'visit') and\n",
        "                callable(subclass.visit) and\n",
        "                hasattr(subclass, 'accept') and \n",
        "                callable(subclass.accept))\n",
        "\n",
    ]


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
