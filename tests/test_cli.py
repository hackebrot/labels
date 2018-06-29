import typing

import pytest

from labels import __version__


@pytest.mark.parametrize("version_option", ["-V", "--version"])
def test_version_option(run_cli: typing.Callable, version_option: str) -> None:
    """Test for the CLI version option."""

    result = run_cli(version_option)
    assert result.exit_code == 0
    assert result.output == f"labels, version {__version__}\n"


@pytest.mark.usefixtures("mock_list_labels")
def test_fetch(
    run_cli: typing.Callable, owner: str, repo: str, labels_file_write: str
) -> None:
    """Test for the CLI fetch command."""

    result = run_cli(
        "-u",
        "hackebrot",
        "-t",
        "1234",
        "fetch",
        "-o",
        owner,
        "-r",
        repo,
        "-f",
        labels_file_write,
    )

    assert result.exit_code == 0
