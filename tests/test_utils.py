import attr
import pytest

from labels import utils


@attr.s(auto_attribs=True, kw_only=True, frozen=True)
class FakeProc:
    """Fake for a CompletedProcess instance."""

    code: int = 0
    stdout: str = ""


@pytest.fixture(name="mock_repo_info")
def fixture_mock_repo_info(mocker, return_value):
    """Patch the subprocess call to git remote get-url."""

    return mocker.patch(
        "labels.utils.subprocess.run", autospec=True, return_value=return_value
    )


@pytest.mark.parametrize(
    "return_value",
    [
        FakeProc(code=0, stdout="git@github.com:hackebrot/pytest-emoji.git\n"),
        FakeProc(code=0, stdout="https://github.com/hackebrot/pytest-emoji.git\n"),
    ],
    ids=["ssh", "https"],
)
def test_load_repository_info(mock_repo_info):
    """Test that load_repository_info() works for both SSH and HTTPS URLs."""

    repo = utils.load_repository_info()
    assert repo.owner == "hackebrot"
    assert repo.name == "pytest-emoji"
    assert mock_repo_info.called


@pytest.mark.parametrize(
    "return_value",
    [FakeProc(code=1, stdout=""), FakeProc(code=0, stdout="abcd")],
    ids=["run_error", "no_match"],
)
def test_load_repository_info_run_error(mock_repo_info):
    """Test that load_repository_info() handles errors."""

    repo = utils.load_repository_info()
    assert repo is None
    assert mock_repo_info.called
