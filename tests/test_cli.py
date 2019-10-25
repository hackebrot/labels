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


@pytest.mark.usefixtures("mock_list_labels")
def test_fetch_without_owner_option(
    run_cli: typing.Callable, owner: str, repo: str, labels_file_write: str
) -> None:
    """Test for the CLI fetch command without -o option supplied."""

    result = run_cli(
        "-u",
        "hackebrot",
        "-t",
        "1234",
        "fetch",
        "-r",
        repo,
        "-f",
        labels_file_write,
    )

    assert result.exit_code == 0


@pytest.mark.usefixtures("mock_sync")
def test_sync(
    run_cli: typing.Callable, owner: str, repo: str, labels_file_sync: str
) -> None:
    """Test for the CLI sync command."""

    result = run_cli(
        "-u",
        "hackebrot",
        "-t",
        "1234",
        "sync",
        "-o",
        owner,
        "-r",
        repo,
        "-f",
        labels_file_sync,
    )

    assert result.exit_code == 0
    assert result.output == ""


@pytest.mark.usefixtures("mock_list_labels")
def test_sync_dryrun(
    run_cli: typing.Callable, owner: str, repo: str, labels_file_sync: str
) -> None:
    """Test for the CLI sync command with the dryrun option."""

    result = run_cli(
        "-u",
        "hackebrot",
        "-t",
        "1234",
        "sync",
        "-n",
        "-o",
        owner,
        "-r",
        repo,
        "-f",
        labels_file_sync,
    )

    assert result.exit_code == 0
    assert result.output == (
        "This would delete the following labels:\n"
        "  - infra\n"
        "This would update the following labels:\n"
        "  - bug\n"
        "This would create the following labels:\n"
        "  - dependencies\n"
        "This would NOT modify the following labels:\n"
        "  - docs\n"
    )
