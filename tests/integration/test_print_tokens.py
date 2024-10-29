"""Test print tokens."""

from app import tokenizer


class TestPrint:
    """Test printing."""

    def test_scan_and_print_empty(self) -> None:
        """Scan and print an empty string."""
        tokens = tokenizer.tokens_to_string(tokenizer.scan(""))
        assert tokens == "EOF  null"

    def test_scan_and_print_parens(self) -> None:
        """Scan and print parenthesis."""
        tokens = tokenizer.tokens_to_string(tokenizer.scan("(()"))
        assert (
            tokens
            == "LEFT_PAREN ( null\n"
            + "LEFT_PAREN ( null\n"
            + "RIGHT_PAREN ) null\n"
            + "EOF  null"
        )
