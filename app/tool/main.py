"""Tools to generate an ast
"""

import sys
from io import TextIOWrapper
from pathlib import Path


def main() -> None:

    if len(sys.argv) != 3:
        printhelp()
        sys.exit(64)

    command = sys.argv[1]
    output_dir = sys.argv[2]

    match command:
        case "generate_ast":
            define_ast(
                output_dir,
                "Expr",
                [
                    "Binary   : Expr left, Token operator, Expr right",
                    "Grouping : Expr expression",
                    "Literal  : Object value",
                    "Unary    : Token operator, Expr right",
                ],
            )
        case _:
            print(f"Unknown command: {command}", file=sys.stderr)
            printhelp()
            sys.exit(1)

    # TODO: Check if the output_dir exists. Or create it if it doesn't exist.
    # TODO: Write everything in a buffer and then write it in the file.


def define_ast(output_dir: str, base_name: str, types: list[str]) -> None:
    """Define the ast."""
    path = Path(output_dir) / f"{base_name.lower()}.py"

    with open(path, "w", encoding="utf-8") as file:
        file.writelines(
            [
                "import abc\n",
                "\n",
                f"class {base_name}(abc.ABC):\n",
                "    pass\n",
                "\n",
            ]
        )
        define_visitor(file, types)

        # The AST classes.
        for _type in types:
            classname = _type.split(":")[0].strip()
            fields = _type.split(":")[1].strip()
            define_type(file, base_name, classname, fields)


def define_type(
    file: TextIOWrapper, base_name: str, classname: str, fieldlist: str
) -> None:
    """Define the types."""
    fieldnames = [field.split(" ")[1] for field in fieldlist.split(", ")]
    file.writelines(
        [
            f"class {classname}({base_name}):\n",
            f"    def __init__(self, {", ".join(fieldnames)}):\n",
        ]
    )

    fields = fieldlist.split(", ")
    for field in fields:
        name = field.split(" ")[1]
        file.write(f"        self.{name} = {name}\n")
    file.write("\n")


def define_visitor(file: TextIOWrapper, types: list[str]) -> None:
    """Generate the abstract class Visitor."""
    file.writelines(
        [
            "class Visitor(metaclass=abc.ABCMeta):\n",
            "    @classmethod\n",
            "    def __subclasshook__(cls, subclass):\n",
            "        return (hasattr(subclass, 'visit') and\n",
            "                callable(subclass.visit) and\n",
            "                hasattr(subclass, 'accept') and \n",
            "                callable(subclass.accept))\n",
            "\n",
        ]
    )


def printhelp() -> None:
    print(
        """
usage: generate_ast <output directory>
        """,
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
