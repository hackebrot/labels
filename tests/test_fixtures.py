import subprocess
from pathlib import Path


def test_fixture_tmp_local_repo(tmp_local_repo, owner: str, repo: str) -> None:
    """Test that the tmp_local_repo fixture mocks a git repo cloned from
    https://github.com/audreyr/cookiecutter.git
    """
    _origin_url = subprocess.check_output(
        ["git", "-C", str(tmp_local_repo), "remote", "get-url", "origin"]
    )
    got_url = _origin_url.strip().decode()

    expected_url = f"https://github.com/{owner}/{repo}.git"

    assert expected_url == got_url


def test_fixture_tmp_local_repo_contains_sync_file(
    tmp_local_repo, labels_file_sync: str
) -> None:
    """Test that labels file for the sync test exists in the temp_local_repo fixture.
    """
    sync_file = Path(str(tmp_local_repo), labels_file_sync)

    assert sync_file.exists()
    assert sync_file.is_file()


def test_sync_file_in_tmp_local_repo_is_appropriately_populated(
    tmp_local_repo, labels_file_sync: str
) -> None:
    """Test that the labels file in the temporary directory is an
    exact copy of the permanent labels file at labels/tests/sync.toml
    """
    with Path(str(tmp_local_repo), labels_file_sync).open() as f_tmp:
        with Path(__file__).parent.joinpath("sync.toml").open() as f_perm:

            assert f_tmp.readlines() == f_perm.readlines()
