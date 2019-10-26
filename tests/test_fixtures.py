import subprocess


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
