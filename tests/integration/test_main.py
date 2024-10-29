"""Test the main program."""

import os
import re

import pytest

from app import main

from . import DATA_FOLDER


def list_test_files() -> list[tuple[str, str, str]]:
    """Build the list of files to test."""
    test_files: list[tuple[str, str, str]] = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".lox"):
            test_files.append(
                (
                    file,
                    re.sub(r"(\.[^.]+)$", ".out", file),
                    re.sub(r"(\.[^.]+)$", ".err", file),
                )
            )
    return test_files


@pytest.mark.parametrize("lox,output,error", list_test_files())
def test_cli(
    lox: str,
    output: str,
    error: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test the cli."""
    monkeypatch.setattr("sys.argv", ["", "tokenize", str(DATA_FOLDER / lox)])

    output_content = ""
    try:
        with open(str(DATA_FOLDER / output), encoding="utf-8") as file:
            output_content = file.read()
    except FileNotFoundError:
        pass

    error_content = ""
    try:
        with open(str(DATA_FOLDER / error), encoding="utf-8") as file:
            error_content = file.read()
    except FileNotFoundError:
        pass

    if error_content:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main.main()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 65
    else:
        main.main()

    captured = capsys.readouterr()
    stdout = captured.out
    stderr = captured.err
    assert stdout == output_content
    assert stderr == error_content
