"""Scan tests."""

from app import scanner, tokens


class TestScan:
    """Test Scan"""

    def test_scan_empty_file(self) -> None:
        """test_scan_empty_file"""
        sc = scanner.Scanner("")
        t = sc.scan_tokens()
        assert len(t) == 1
        assert t[0].type == tokens.TokenType.EOF

    def test_scan_empty_parens(self) -> None:
        """test_scan_empty_parens"""
        expected = [
            tokens.Token(tokens.TokenType.LEFT_PAREN, "(", None, 0),
            tokens.Token(tokens.TokenType.LEFT_PAREN, "(", None, 0),
            tokens.Token(tokens.TokenType.RIGHT_PAREN, ")", None, 0),
            tokens.Token(tokens.TokenType.EOF, "", None, 0),
        ]

        sc = scanner.Scanner("(()")
        t = sc.scan_tokens()
        assert t == expected
