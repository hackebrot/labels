from pathlib import Path
from typing import Any, Dict, Generator, List

import attr
import pytest
import responses

from labels.github import Label

ResponseLabel = Dict[str, Any]
ResponseLabels = List[ResponseLabel]


@pytest.fixture(name="username", scope="session")
def fixture_username() -> str:
    """Return a username for GitHub API authentication."""
    return "hackebrot"


@pytest.fixture(name="token", scope="session")
def fixture_token() -> str:
    """Return a token for GitHub API authentication."""
    return "1234"


@pytest.fixture(name="repo_owner", scope="session")
def fixture_repo_owner() -> str:
    """Return a repository owner."""
    return "hackebrot"


@pytest.fixture(name="repo_name", scope="session")
def fixture_repo_name() -> str:
    """Return a repository name."""
    return "turtle"


@pytest.fixture(name="repo_id", scope="session")
def fixture_repo_id() -> int:
    """Return a repository ID."""
    return 102909380


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class FakeProc:
    """Fake for a CompletedProcess instance."""

    returncode: int
    stdout: str


@pytest.fixture(name="mock_repo_info")
def fixture_mock_repo_info(mocker: Any, remote_url: str) -> Any:
    """Patch the subprocess call to git remote get-url."""

    return mocker.patch(
        "labels.utils.subprocess.run",
        autospec=True,
        return_value=FakeProc(returncode=0, stdout=remote_url),
    )


@pytest.fixture(name="mock_repo_info_error")
def fixture_mock_repo_info_error(mocker: Any) -> Any:
    """Patch the subprocess call to git remote get-url with an error."""

    return mocker.patch(
        "labels.utils.subprocess.run",
        autospec=True,
        return_value=FakeProc(returncode=1, stdout="error"),
    )


@pytest.fixture(name="mock_repo_info_bad_url")
def fixture_mock_repo_info_bad_url(mocker: Any) -> Any:
    """Patch the subprocess call to git remote get-url with a bad URL."""

    return mocker.patch(
        "labels.utils.subprocess.run",
        autospec=True,
        return_value=FakeProc(returncode=0, stdout="abcd"),
    )


@pytest.fixture(name="base_url", scope="session")
def fixture_base_url() -> str:
    """Return a URL to the GitHub API."""
    return "https://api.github.com"


@pytest.fixture(name="response_get_bug")
def fixture_response_get_bug(
    base_url: str, repo_owner: str, repo_name: str
) -> ResponseLabel:
    """Return a dict respresenting the GitHub API response body for the bug
    label.
    """
    return {
        "id": 8888,
        "node_id": "1010",
        "url": f"{base_url}/repos/{repo_owner}/{repo_name}/labels/bug",
        "name": "bug",
        "description": "Bugs and problems with cookiecutter",
        "color": "ea707a",
        "default": True,
    }


@pytest.fixture(name="response_get_docs")
def fixture_response_get_docs(
    base_url: str, repo_owner: str, repo_name: str
) -> ResponseLabel:
    """Return a dict respresenting the GitHub API response body for the docs
    label.
    """
    return {
        "id": 2222,
        "node_id": "4444",
        "url": f"{base_url}/repos/{repo_owner}/{repo_name}/labels/docs",
        "name": "docs",
        "description": "Tasks to write and update documentation",
        "color": "2abf88",
        "default": False,
    }


@pytest.fixture(name="response_get_infra")
def fixture_response_get_infra(
    base_url: str, repo_owner: str, repo_name: str
) -> ResponseLabel:
    """Return a dict respresenting the GitHub API response body for the infra
    label.
    """
    return {
        "id": 1234,
        "node_id": "5678",
        "url": f"{base_url}/repos/{repo_owner}/{repo_name}/labels/infra",
        "name": "infra",
        "description": "Tasks related to Docker/CI etc.",
        "color": "f9d03b",
        "default": False,
    }


@pytest.fixture(name="response_list_labels")
def fixture_response_list_labels(
    response_get_infra: ResponseLabel,
    response_get_docs: ResponseLabel,
    response_get_bug: ResponseLabel,
) -> ResponseLabels:
    """Response body for list_labels()."""
    return [response_get_infra, response_get_docs, response_get_bug]


@pytest.fixture(name="mock_list_labels")
def fixture_mock_list_labels(
    base_url: str, repo_owner: str, repo_name: str, response_list_labels: ResponseLabels
) -> Generator:
    """Mock requests for list labels."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"{base_url}/repos/{repo_owner}/{repo_name}/labels",
            json=response_list_labels,
            status=200,
            content_type="application/json",
        )
        yield


@pytest.fixture(name="mock_list_labels_paginated")
def fixture_mock_list_labels_paginated(
    base_url: str,
    repo_owner: str,
    repo_name: str,
    repo_id: int,
    response_get_infra: ResponseLabel,
    response_get_docs: ResponseLabel,
    response_get_bug: ResponseLabel,
) -> Generator:
    """Mock requests for list labels with pagination."""

    with responses.RequestsMock() as rsps:

        rsps.add(
            responses.GET,
            f"{base_url}/repos/{repo_owner}/{repo_name}/labels",
            json=[response_get_bug, response_get_docs],
            status=200,
            content_type="application/json",
            headers={
                "Link": (
                    f'<{base_url}/repositories/{repo_id}/labels?page=2>; rel="next", '
                    f'<{base_url}/repositories/{repo_id}/labels?page=2>; rel="last"'
                )
            },
        )

        rsps.add(
            responses.GET,
            f"{base_url}/repositories/{repo_id}/labels?page=2",
            json=[response_get_infra],
            status=200,
            content_type="application/json",
            headers={
                "Link": (
                    f'<{base_url}/repositories/{repo_id}/labels?page=1>; rel="prev", '
                    f'<{base_url}/repositories/{repo_id}/labels?page=1>; rel="first"'
                )
            },
        )

        yield


@pytest.fixture(name="mock_get_label")
def fixture_mock_get_label(
    base_url: str, repo_owner: str, repo_name: str, response_get_bug: ResponseLabel
) -> Generator:
    """Mock requests for get label."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"{base_url}/repos/{repo_owner}/{repo_name}/labels/bug",
            json=response_get_bug,
            status=200,
            content_type="application/json",
        )
        yield


@pytest.fixture(name="mock_edit_label")
def fixture_mock_edit_label(
    base_url: str, repo_owner: str, repo_name: str, response_get_bug: ResponseLabel
) -> Generator:
    """Mock requests for edit label."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.PATCH,
            f"{base_url}/repos/{repo_owner}/{repo_name}/labels/bug",
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
    base_url: str,
    repo_owner: str,
    repo_name: str,
    label: Label,
    response_get_bug: ResponseLabel,
) -> Generator:
    """Mock requests for create label."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            f"{base_url}/repos/{repo_owner}/{repo_name}/labels",
            json=response_get_bug,
            status=201,
            content_type="application/json",
        )
        yield


@pytest.fixture(name="mock_delete_label")
def fixture_mock_delete_label(
    base_url: str, repo_owner: str, repo_name: str
) -> Generator:
    """Mock requests for delete label."""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.DELETE,
            f"{base_url}/repos/{repo_owner}/{repo_name}/labels/bug",
            status=204,
        )
        yield


@pytest.fixture(name="mock_sync")
def fixture_mock_sync(
    base_url: str, repo_owner: str, repo_name: str, response_list_labels: ResponseLabels
) -> Generator:
    with responses.RequestsMock() as rsps:
        # Response mock for when sync requests the existing remote labels
        rsps.add(
            responses.GET,
            f"{base_url}/repos/{repo_owner}/{repo_name}/labels",
            json=response_list_labels,
            status=200,
            content_type="application/json",
        )

        # Response mock for when sync creates the "dependencies" label
        rsps.add(
            responses.POST,
            f"{base_url}/repos/{repo_owner}/{repo_name}/labels",
            json={
                "id": 8080,
                "node_id": "4848",
                "url": f"{base_url}/repos/{repo_owner}/{repo_name}/labels/dependencies",
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
            f"{base_url}/repos/{repo_owner}/{repo_name}/labels/bug",
            json={
                "id": 8888,
                "node_id": "1010",
                "url": f"{base_url}/repos/{repo_owner}/{repo_name}/labels/bug",
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
            f"{base_url}/repos/{repo_owner}/{repo_name}/labels/infra",
            status=204,
        )

        yield


@pytest.fixture(name="labels")
def fixture_labels() -> List[Label]:
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
            color="f9d03b", description="Tasks related to Docker/CI etc.", name="infra"
        ),
        Label(color="f9d03b", name="no description"),
        Label(color="f9d03b", description="", name="empty description"),
    ]


@pytest.fixture(name="labels_file_dict")
def fixture_labels_file_content() -> Dict[str, Any]:
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
def fixture_labels_file_write(tmpdir: Any) -> str:
    """Return a filepath to a temporary file."""
    labels_file = tmpdir.join("labels.toml")
    return Path(labels_file).as_posix()


@pytest.fixture(name="labels_file_load")
def fixture_labels_file_load() -> str:
    """Return a filepath to an existing labels file."""
    return "tests/labels.toml"


@pytest.fixture(name="labels_file_sync")
def fixture_labels_file_sync(tmpdir: Any) -> str:
    """Return a filepath to an existing labels file for the sync test."""
    return "tests/sync.toml"
