"""Test print tokens."""

from app import scanner


class TestPrint:
    """Test printing."""

    def test_scan_and_print_empty(self) -> None:
        """Scan and print an empty string."""
        tokens, lexical_errors = scanner.scan("")
        string = scanner.tokens_to_string(tokens)
        assert string == "EOF  null"
        assert len(lexical_errors) == 0

    def test_scan_and_print_parens(self) -> None:
        """Scan and print parenthesis."""
        tokens, lexical_errors = scanner.scan("(()")
        string = scanner.tokens_to_string(tokens)
        assert (
            string
            == "LEFT_PAREN ( null\n"
            + "LEFT_PAREN ( null\n"
            + "RIGHT_PAREN ) null\n"
            + "EOF  null"
        )
        assert len(lexical_errors) == 0

    def test_scan_with_lexical_errors(self) -> None:
        """Scan with lexical errors."""
        tokens, lexical_errors = scanner.scan(",.$(#")
        string = scanner.tokens_to_string(tokens)
        assert (
            string
            == "COMMA , null\n"
            + "DOT . null\n"
            + "LEFT_PAREN ( null\n"
            + "EOF  null"
        )
        assert lexical_errors == [
            "[line 1] Error: Unexpected character: $",
            "[line 1] Error: Unexpected character: #",
        ]
