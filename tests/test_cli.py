import typing
import shlex

import pytest
from click.testing import CliRunner

from labels import __version__
from labels.cli import labels


@pytest.fixture(name="set_username", autouse=True)
def fixture_set_username(monkeypatch: typing.Any, username: str) -> None:
    """Set the username environment variable."""
    monkeypatch.setenv("LABELS_USERNAME", username)


@pytest.fixture(name="set_token", autouse=True)
def fixture_set_token(monkeypatch: typing.Any, token: str) -> None:
    """Set the token environment variable."""
    monkeypatch.setenv("LABELS_TOKEN", token)


@pytest.fixture(name="run_cli")
def fixture_run_cli() -> typing.Callable:
    """Return a function that invokes a click CLI runner."""
    runner = CliRunner()

    def run(cli_options: str) -> typing.Any:
        """Run the CLI with the given options and return the result."""
        return runner.invoke(labels, shlex.split(cli_options))

    return run


@pytest.mark.parametrize("version_option", ["-V", "--version"])
def test_version_option(run_cli: typing.Callable, version_option: str) -> None:
    """Test for the CLI version option."""
    result = run_cli(version_option)
    assert result.exit_code == 0
    assert result.output == f"labels, version {__version__}\n"


@pytest.mark.usefixtures("mock_list_labels", "mock_repo_info")
@pytest.mark.parametrize(
    "repo_owner, repo_name, remote_url",
    [("hackebrot", "pytest-emoji", "git@github.com:hackebrot/pytest-emoji.git")],
    ids=["no_override"],
)
def test_fetch_default_owner_and_repo(
    run_cli: typing.Callable, repo_owner: str, repo_name: str, labels_file_write: str
) -> None:
    """Test that fetch loads repo_owner and repo info from the Git repository."""
    result = run_cli(f"-v fetch -f {labels_file_write}")
    assert result.exit_code == 0
    assert f"Requesting labels for {repo_owner}/{repo_name}" in result.output


@pytest.mark.usefixtures("mock_list_labels", "mock_repo_info")
@pytest.mark.parametrize(
    "repo_owner, repo_name, remote_url",
    [("hackebrot", "labels", "git@github.com:hackebrot/pytest-emoji.git")],
    ids=["override_repo"],
)
def test_fetch_default_owner(
    run_cli: typing.Callable, repo_owner: str, repo_name: str, labels_file_write: str
) -> None:
    """Test that fetch overrides the repo from the Git repository."""
    result = run_cli(f"-v fetch -r {repo_name} -f {labels_file_write}")
    assert result.exit_code == 0
    assert f"Requesting labels for {repo_owner}/{repo_name}" in result.output


@pytest.mark.usefixtures("mock_list_labels", "mock_repo_info")
@pytest.mark.parametrize(
    "repo_owner, repo_name, remote_url",
    [("pytest-dev", "pytest-emoji", "git@github.com:hackebrot/pytest-emoji.git")],
    ids=["override_owner"],
)
def test_fetch_default_repo(
    run_cli: typing.Callable, repo_owner: str, repo_name: str, labels_file_write: str
) -> None:
    """Test that fetch overrides the owner from the Git repository."""
    result = run_cli(f"-v fetch -o {repo_owner} -f {labels_file_write}")
    assert result.exit_code == 0, result.exc_info
    assert f"Requesting labels for {repo_owner}/{repo_name}" in result.output


@pytest.mark.usefixtures("mock_list_labels", "mock_repo_info")
@pytest.mark.parametrize(
    "repo_owner, repo_name, remote_url",
    [("pytest-dev", "pytest", "git@github.com:hackebrot/pytest-emoji.git")],
    ids=["override_owner_and_repo"],
)
def test_fetch(
    run_cli: typing.Callable, repo_owner: str, repo_name: str, labels_file_write: str
) -> None:
    """Test that fetch overrides the owner and repo from the Git repository."""
    result = run_cli(f"-v fetch -o {repo_owner} -r {repo_name} -f {labels_file_write}")
    assert result.exit_code == 0
    assert f"Requesting labels for {repo_owner}/{repo_name}" in result.output


@pytest.mark.usefixtures("mock_sync", "mock_repo_info")
@pytest.mark.parametrize(
    "repo_owner, repo_name, remote_url",
    [("hackebrot", "pytest-emoji", "git@github.com:hackebrot/pytest-emoji.git")],
    ids=["no_override"],
)
def test_sync_default_owner_and_repo(
    run_cli: typing.Callable, repo_owner: str, repo_name: str, labels_file_sync: str
) -> None:
    """Test that sync loads owner and repo info from the Git repository."""
    result = run_cli(f"-v sync -f {labels_file_sync}")
    assert result.exit_code == 0
    assert f"Requesting labels for {repo_owner}/{repo_name}" in result.output
    assert f"Deleting label 'infra' for {repo_owner}/{repo_name}" in result.output
    assert f"Editing label 'bug' for {repo_owner}/{repo_name}" in result.output
    assert (
        f"Creating label 'dependencies' for {repo_owner}/{repo_name}" in result.output
    )


@pytest.mark.usefixtures("mock_sync", "mock_repo_info")
@pytest.mark.parametrize(
    "repo_owner, repo_name, remote_url",
    [("hackebrot", "labels", "git@github.com:hackebrot/pytest-emoji.git")],
    ids=["override_repo"],
)
def test_sync_default_owner(
    run_cli: typing.Callable, repo_owner: str, repo_name: str, labels_file_sync: str
) -> None:
    """Test that sync overrides the repo from the Git repository."""
    result = run_cli(f"-v sync -r {repo_name} -f {labels_file_sync}")
    assert result.exit_code == 0
    assert f"Requesting labels for {repo_owner}/{repo_name}" in result.output
    assert f"Deleting label 'infra' for {repo_owner}/{repo_name}" in result.output
    assert f"Editing label 'bug' for {repo_owner}/{repo_name}" in result.output
    assert (
        f"Creating label 'dependencies' for {repo_owner}/{repo_name}" in result.output
    )


@pytest.mark.usefixtures("mock_sync", "mock_repo_info")
@pytest.mark.parametrize(
    "repo_owner, repo_name, remote_url",
    [("pytest-dev", "pytest-emoji", "git@github.com:hackebrot/pytest-emoji.git")],
    ids=["override_owner"],
)
def test_sync_default_repo(
    run_cli: typing.Callable, repo_owner: str, repo_name: str, labels_file_sync: str
) -> None:
    """Test that sync overrides the owner from the Git repository."""
    result = run_cli(f"-v sync -o {repo_owner} -f {labels_file_sync}")
    assert result.exit_code == 0
    assert f"Requesting labels for {repo_owner}/{repo_name}" in result.output
    assert f"Deleting label 'infra' for {repo_owner}/{repo_name}" in result.output
    assert f"Editing label 'bug' for {repo_owner}/{repo_name}" in result.output
    assert (
        f"Creating label 'dependencies' for {repo_owner}/{repo_name}" in result.output
    )


@pytest.mark.usefixtures("mock_sync", "mock_repo_info")
@pytest.mark.parametrize(
    "repo_owner, repo_name, remote_url",
    [("pytest-dev", "pytest", "git@github.com:hackebrot/pytest-emoji.git")],
    ids=["override_owner_and_repo"],
)
def test_sync(
    run_cli: typing.Callable, repo_owner: str, repo_name: str, labels_file_sync: str
) -> None:
    """Test that sync overrides the owner and repo from the Git repository."""
    result = run_cli(f"-v sync -o {repo_owner} -r {repo_name} -f {labels_file_sync}")
    assert result.exit_code == 0
    assert f"Requesting labels for {repo_owner}/{repo_name}" in result.output
    assert f"Deleting label 'infra' for {repo_owner}/{repo_name}" in result.output
    assert f"Editing label 'bug' for {repo_owner}/{repo_name}" in result.output
    assert (
        f"Creating label 'dependencies' for {repo_owner}/{repo_name}" in result.output
    )


@pytest.mark.usefixtures("mock_list_labels", "mock_repo_info")
@pytest.mark.parametrize(
    "repo_owner, repo_name, remote_url",
    [("pytest-dev", "pytest", "git@github.com:hackebrot/pytest-emoji.git")],
    ids=["override_owner_and_repo"],
)
def test_sync_dryrun(
    run_cli: typing.Callable, repo_owner: str, repo_name: str, labels_file_sync: str
) -> None:
    """Test that sync with the dryrun option works as designed."""
    result = run_cli(f"-v sync -n -o {repo_owner} -r {repo_name} -f {labels_file_sync}")
    assert result.exit_code == 0

    output = (
        "This would delete the following labels:\n"
        "  - infra\n"
        "This would update the following labels:\n"
        "  - bug\n"
        "This would create the following labels:\n"
        "  - dependencies\n"
        "This would NOT modify the following labels:\n"
        "  - docs\n"
    )
    assert output in result.output
