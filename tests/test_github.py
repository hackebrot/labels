import pytest

from requests.auth import HTTPBasicAuth

from labels.github import Client, Label, Repository


@pytest.fixture(name="client")
def fixture_client(base_url: str, username: str, token: str) -> Client:
    """Return a GitHub API client."""
    return Client(HTTPBasicAuth(username, token), base_url=base_url)


@pytest.fixture(name="repo")
def fixture_repo(repo_owner: str, repo_name: str) -> Repository:
    """Return a GitHub repository."""
    return Repository(repo_owner, repo_name)


@pytest.mark.usefixtures("mock_list_labels")
def test_list_labels(client: Client, repo: Repository) -> None:
    """Test that list_labels() requests the labels for the specified repo and
    returns a list of Label instances.
    """
    labels = client.list_labels(repo)

    expected_params = [
        {
            "name": "infra",
            "description": "Tasks related to Docker/CI etc.",
            "color": "f9d03b",
        },
        {
            "name": "docs",
            "description": "Tasks to write and update documentation",
            "color": "2abf88",
        },
        {
            "name": "bug",
            "description": "Bugs and problems with cookiecutter",
            "color": "ea707a",
        },
    ]

    assert [l.params_dict for l in labels] == expected_params


@pytest.mark.usefixtures("mock_get_label")
def test_get_label(client: Client, repo: Repository) -> None:
    """Test that get_label() requests the specified label for the repo and
    returns a Label instance.
    """
    label = client.get_label(repo, name="bug")

    expected_params = {
        "name": "bug",
        "description": "Bugs and problems with cookiecutter",
        "color": "ea707a",
    }

    assert label.params_dict == expected_params


@pytest.mark.usefixtures("mock_create_label")
def test_create_label(client: Client, repo: Repository, label: Label) -> None:
    """Test that create_label() requests the label to be created and returns
    a Label instance.
    """
    created_label = client.create_label(repo, label=label)

    assert created_label.params_dict == label.params_dict


@pytest.mark.usefixtures("mock_edit_label")
def test_edit_label(client: Client, repo: Repository, label: Label) -> None:
    """Test that edit_label() requests the label to be updated and returns
    the updated Label instance.
    """
    label = client.edit_label(repo, name="bug", label=label)

    expected_params = {
        "name": "bug",
        "description": "Bugs and problems with cookiecutter",
        "color": "ea707a",
    }

    assert label.params_dict == expected_params


@pytest.mark.usefixtures("mock_delete_label")
def test_delete_label(client: Client, repo: Repository) -> None:
    """Test that delete_label() performs the correct request."""

    client.delete_label(repo, name="bug")
