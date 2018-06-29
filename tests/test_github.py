import pytest


from labels.github import Client, Label


@pytest.mark.usefixtures("mock_list_labels")
def test_list_labels(client: Client, owner: str, repo: str) -> None:
    """Test that list_labels() requests the labels for the specified repo and
    returns a list of Label instances.
    """
    labels = client.list_labels(owner, repo)

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
def test_get_label(client: Client, owner: str, repo: str) -> None:
    """Test that get_label() requests the specified label for the repo and
    returns a Label instance.
    """
    label = client.get_label(owner, repo, name="bug")

    expected_params = {
        "name": "bug",
        "description": "Bugs and problems with cookiecutter",
        "color": "ea707a",
    }

    assert label.params_dict == expected_params


@pytest.mark.usefixtures("mock_create_label")
def test_create_label(client: Client, owner: str, repo: str, label: Label) -> None:
    """Test that create_label() requests the label to be created and returns
    a Label instance.
    """
    created_label = client.create_label(owner, repo, label=label)

    assert created_label.params_dict == label.params_dict


@pytest.mark.usefixtures("mock_edit_label")
def test_edit_label(client: Client, owner: str, repo: str, label: Label) -> None:
    """Test that edit_label() requests the label to be updated and returns
    the updated Label instance.
    """
    label = client.edit_label(owner, repo, name="bug", label=label)

    expected_params = {
        "name": "bug",
        "description": "Bugs and problems with cookiecutter",
        "color": "ea707a",
    }

    assert label.params_dict == expected_params


@pytest.mark.usefixtures("mock_delete_label")
def test_delete_label(client: Client, owner: str, repo: str) -> None:
    """Test that delete_label() performs the correct request."""

    client.delete_label(owner, repo, name="bug")
