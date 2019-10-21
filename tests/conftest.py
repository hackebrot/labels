import typing

import pytest
import responses
from click.testing import CliRunner
from requests.auth import HTTPBasicAuth

from labels.cli import labels
from labels.github import Client, Label

Response_Label = typing.Dict[str, typing.Any]
Response_Labels = typing.List[Response_Label]


@pytest.fixture(name="run_cli")
def fixture_run_cli() -> typing.Callable:
    """Return a function that invokes a click CLI runner."""
    runner = CliRunner()

    def run(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        """Run the CLI with the given parameters and return the result."""
        return runner.invoke(labels, [*args])

    return run


@pytest.fixture(name="base_url")
def fixture_base_url() -> str:
    """Return a URL to be used for creating a client."""
    return "https://api.github.com"


@pytest.fixture(name="client")
def fixture_client(base_url: str) -> Client:
    """Return a GitHub API client."""
    return Client(HTTPBasicAuth("", ""), base_url=base_url)


@pytest.fixture(name="owner")
def fixture_owner() -> str:
    """Return a repository owner."""
    return "audreyr"


@pytest.fixture(name="repo")
def fixture_repo() -> str:
    """Return a repository name."""
    return "cookiecutter"


@pytest.fixture(name="response_get_bug")
def fixture_response_get_bug(base_url: str, owner: str, repo: str) -> Response_Label:
    """Return a dict respresenting the GitHub API response body for the bug
    label.
    """
    return {
        "id": 8888,
        "node_id": "1010",
        "url": f"{base_url}/repos/{owner}/{repo}/labels/bug",
        "name": "bug",
        "description": "Bugs and problems with cookiecutter",
        "color": "ea707a",
        "default": True,
    }


@pytest.fixture(name="response_get_docs")
def fixture_response_get_docs(base_url: str, owner: str, repo: str) -> Response_Label:
    """Return a dict respresenting the GitHub API response body for the docs
    label.
    """
    return {
        "id": 2222,
        "node_id": "4444",
        "url": f"{base_url}/repos/{owner}/{repo}/labels/docs",
        "name": "docs",
        "description": "Tasks to write and update documentation",
        "color": "2abf88",
        "default": False,
    }


@pytest.fixture(name="response_get_infra")
def fixture_response_get_infra(base_url: str, owner: str, repo: str) -> Response_Label:
    """Return a dict respresenting the GitHub API response body for the infra
    label.
    """
    return {
        "id": 1234,
        "node_id": "5678",
        "url": f"{base_url}/repos/{owner}/{repo}/labels/infra",
        "name": "infra",
        "description": "Tasks related to Docker/CI etc.",
        "color": "f9d03b",
        "default": False,
    }


@pytest.fixture(name="response_list_labels")
def fixture_response_list_labels(
    response_get_infra: Response_Label,
    response_get_docs: Response_Label,
    response_get_bug: Response_Label,
) -> Response_Labels:
    """Response body for list_labels()."""
    return [response_get_infra, response_get_docs, response_get_bug]


@pytest.fixture(name="mock_list_labels")
def fixture_mock_list_labels(
    base_url: str, owner: str, repo: str, response_list_labels: Response_Labels
) -> None:
    """Mock requests for list labels."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"{base_url}/repos/{owner}/{repo}/labels",
            json=response_list_labels,
            status=200,
            content_type="application/json",
        )
        yield


@pytest.fixture(name="mock_get_label")
def fixture_mock_get_label(
    base_url: str, owner: str, repo: str, response_get_bug: Response_Label
) -> None:
    """Mock requests for get label."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"{base_url}/repos/{owner}/{repo}/labels/bug",
            json=response_get_bug,
            status=200,
            content_type="application/json",
        )
        yield


@pytest.fixture(name="mock_edit_label")
def fixture_mock_edit_label(
    base_url: str, owner: str, repo: str, response_get_bug: Response_Label
) -> None:
    """Mock requests for edit label."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.PATCH,
            f"{base_url}/repos/{owner}/{repo}/labels/bug",
            json=response_get_bug,
            status=200,
            content_type="application/json",
        )
        yield


@pytest.fixture(name="label")
def fixture_label() -> Label:
    """Return a single Label instance."""
    return Label(
        color="ea707a", description="Bugs and problems with cookiecutter", name="bug"
    )


@pytest.fixture(name="mock_create_label")
def fixture_mock_create_label(
    base_url: str, owner: str, repo: str, label: Label, response_get_bug: Response_Label
) -> None:
    """Mock requests for create label."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            f"{base_url}/repos/{owner}/{repo}/labels",
            json=response_get_bug,
            status=201,
            content_type="application/json",
        )
        yield


@pytest.fixture(name="mock_delete_label")
def fixture_mock_delete_label(base_url: str, owner: str, repo: str) -> None:
    """Mock requests for delete label."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.DELETE, f"{base_url}/repos/{owner}/{repo}/labels/bug", status=204
        )
        yield


@pytest.fixture(name="mock_sync")
def fixture_mock_sync(
    base_url: str, owner: str, repo: str, response_list_labels: Response_Labels
) -> None:
    with responses.RequestsMock() as rsps:
        # Response mock for when sync requests the existing remote labels
        rsps.add(
            responses.GET,
            f"{base_url}/repos/{owner}/{repo}/labels",
            json=response_list_labels,
            status=200,
            content_type="application/json",
        )

        # Response mock for when sync creates the "dependencies" label
        rsps.add(
            responses.POST,
            f"{base_url}/repos/{owner}/{repo}/labels",
            json={
                "id": 8080,
                "node_id": "4848",
                "url": f"{base_url}/repos/{owner}/{repo}/labels/dependencies",
                "name": "dependencies",
                "description": "Tasks related to managing dependencies",
                "color": "43a2b7",
                "default": False,
            },
            status=201,
            content_type="application/json",
        )

        # Response mock for when sync edits the "bug" label
        rsps.add(
            responses.PATCH,
            f"{base_url}/repos/{owner}/{repo}/labels/bug",
            json={
                "id": 8888,
                "node_id": "1010",
                "url": f"{base_url}/repos/{owner}/{repo}/labels/bug",
                "name": "bug",
                "description": "Bugs and problems with cookiecutter",
                "color": "fcc4db",
                "default": True,
            },
            status=200,
            content_type="application/json",
        )

        # Response mock for when sync deletes the "infra" label
        rsps.add(
            responses.DELETE,
            f"{base_url}/repos/{owner}/{repo}/labels/infra",
            status=204,
        )

        yield


@pytest.fixture(name="labels")
def fixture_labels() -> typing.List[Label]:
    """Return a list of Label instances."""
    return [
        Label(
            color="ea707a",
            description="Bugs and problems with cookiecutter",
            name="bug",
        ),
        Label(
            color="fcc4db",
            description="Tasks related to linting, type checks",
            name="code quality",
        ),
        Label(
            color="43a2b7",
            description="Tasks related to managing dependencies",
            name="dependencies",
        ),
        Label(
            color="8f7ad6",
            description="Issues for discussing ideas for features",
            name="discussion",
        ),
        Label(
            color="2abf88",
            description="Tasks to write and update documentation",
            name="docs",
        ),
        Label(
            color="bfdadc",
            description="Tasks to pick up by newcomers to the project",
            name="good first issue",
        ),
        Label(
            color="f9d03b",
            description="Tasks related to Docker/CI etc.",
            name="infra"
        ),
        Label(
            color="f9d03b",
            name="no description"
        ),
        Label(
            color="f9d03b",
            description="",
            name="empty description"
        ),
    ]


@pytest.fixture(name="labels_file_dict")
def fixture_labels_file_content() -> typing.Dict[str, typing.Any]:
    """Return a mapping from label names to dicts representing Labels."""
    return {
        "bug": {
            "color": "ea707a",
            "description": "Bugs and problems with cookiecutter",
            "name": "bug",
        },
        "code quality": {
            "color": "fcc4db",
            "description": "Tasks related to linting, type checks",
            "name": "code quality",
        },
        "dependencies": {
            "color": "43a2b7",
            "description": "Tasks related to managing dependencies",
            "name": "dependencies",
        },
        "discussion": {
            "color": "8f7ad6",
            "description": "Issues for discussing ideas for features",
            "name": "discussion",
        },
        "docs": {
            "color": "2abf88",
            "description": "Tasks to write and update documentation",
            "name": "docs",
        },
        "good first issue": {
            "color": "bfdadc",
            "description": "Tasks to pick up by newcomers to the project",
            "name": "good first issue",
        },
        "infra": {
            "color": "f9d03b",
            "description": "Tasks related to Docker/CI etc.",
            "name": "infra",
        },
        "no description": {
            "color": "f9d03b",
            "description": "",
            "name": "no description",
        },
        "empty description": {
            "color": "f9d03b",
            "description": "",
            "name": "empty description",
        },
    }


@pytest.fixture(name="labels_file_write")
def fixture_labels_file_write(tmpdir) -> str:
    """Return a filepath to a temporary file."""
    labels_file = tmpdir.join("labels.toml")
    return str(labels_file)


@pytest.fixture(name="labels_file_load")
def fixture_labels_file_load() -> str:
    """Return a filepath to an existing labels file."""
    return "tests/labels.toml"


@pytest.fixture(name="labels_file_sync")
def fixture_labels_file_sync(tmpdir) -> str:
    """Return a filepath to an existing labels file for the sync test."""
    return "tests/sync.toml"
