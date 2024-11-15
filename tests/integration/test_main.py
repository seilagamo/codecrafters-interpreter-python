"""Test the main program."""

import os
import re

import pytest

from app import main

from . import DATA_FOLDER


def list_test_files(subfolder: str) -> list[tuple[str, str, str]]:
    """Build the list of files to test."""
    test_files: list[tuple[str, str, str]] = []
    for file in os.listdir(DATA_FOLDER / subfolder):
        if file.endswith(".lox"):
            test_files.append(
                (
                    file,
                    re.sub(r"(\.[^.]+)$", ".out", file),
                    re.sub(r"(\.[^.]+)$", ".err", file),
                )
            )
    return test_files


@pytest.mark.parametrize("lox,output,error", list_test_files("tokenize"))
def test_cli_tokenize(
    lox: str,
    output: str,
    error: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test the tokenize command."""
    monkeypatch.setattr(
        "sys.argv", ["", "tokenize", str(DATA_FOLDER / "tokenize" / lox)]
    )

    output_content = ""
    try:
        with open(
            str(DATA_FOLDER / "tokenize" / output), encoding="utf-8"
        ) as file:
            output_content = file.read()
    except FileNotFoundError:
        pass

    error_content = ""
    try:
        with open(
            str(DATA_FOLDER / "tokenize" / error), encoding="utf-8"
        ) as file:
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


@pytest.mark.parametrize("lox,output,error", list_test_files("parse"))
def test_cli_parse(
    lox: str,
    output: str,
    error: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test the parse command."""
    monkeypatch.setattr(
        "sys.argv", ["", "parse", str(DATA_FOLDER / "parse" / lox)]
    )

    output_content = ""
    try:
        with open(
            str(DATA_FOLDER / "parse" / output), encoding="utf-8"
        ) as file:
            output_content = file.read()
    except FileNotFoundError:
        pass

    error_content = ""
    try:
        with open(str(DATA_FOLDER / "parse" / error), encoding="utf-8") as file:
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


@pytest.mark.parametrize("lox,output,error", list_test_files("evaluate"))
def test_cli_evaluate(
    lox: str,
    output: str,
    error: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test the evaluate command."""
    monkeypatch.setattr(
        "sys.argv", ["", "evaluate", str(DATA_FOLDER / "evaluate" / lox)]
    )

    output_content = ""
    try:
        with open(
            str(DATA_FOLDER / "evaluate" / output), encoding="utf-8"
        ) as file:
            output_content = file.read()
    except FileNotFoundError:
        pass

    error_content = ""
    try:
        with open(
            str(DATA_FOLDER / "evaluate" / error), encoding="utf-8"
        ) as file:
            error_content = file.read()
    except FileNotFoundError:
        pass

    if error_content:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main.main()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 70
    else:
        main.main()

    captured = capsys.readouterr()
    stdout = captured.out
    stderr = captured.err
    assert stdout == output_content
    assert stderr == error_content


@pytest.mark.parametrize("lox,output,error", list_test_files("run"))
def test_cli_run(
    lox: str,
    output: str,
    error: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test the evaluate command."""
    monkeypatch.setattr("sys.argv", ["", "run", str(DATA_FOLDER / "run" / lox)])

    output_content = ""
    try:
        with open(str(DATA_FOLDER / "run" / output), encoding="utf-8") as file:
            output_content = file.read()
    except FileNotFoundError:
        pass

    error_content = ""
    try:
        with open(str(DATA_FOLDER / "run" / error), encoding="utf-8") as file:
            error_content = file.read()
    except FileNotFoundError:
        pass

    if error_content:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main.main()

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 70
    else:
        main.main()

    captured = capsys.readouterr()
    stdout = captured.out
    stderr = captured.err
    assert stdout == output_content
    assert stderr == error_content
