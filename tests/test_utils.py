import pytest

from labels import utils


@pytest.mark.parametrize(
    "remote_url",
    [
        "git@github.com:pytest-dev/pytest.git\n",
        "https://github.com/pytest-dev/pytest.git\n",
    ],
    ids=["ssh", "https"],
)
def test_load_repository_info(mock_repo_info):
    """Test that load_repository_info() works for both SSH and HTTPS URLs."""

    repo = utils.load_repository_info()
    assert repo.owner == "pytest-dev"
    assert repo.name == "pytest"
    assert mock_repo_info.called


def test_load_repository_info_error(mock_repo_info_error):
    """Test that load_repository_info() handles errors."""

    repo = utils.load_repository_info()
    assert repo is None
    assert mock_repo_info_error.called


def test_load_repository_bad_url(mock_repo_info_bad_url):
    """Test that load_repository_info() handles bad URLs."""

    repo = utils.load_repository_info()
    assert repo is None
    assert mock_repo_info_bad_url.called
