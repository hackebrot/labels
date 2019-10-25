import subprocess


def test_fixture_tmp_local_repo(tmp_local_repo) -> None:
    """Test that the tmp_local_repo fixture mocks a git repo cloned from
    https://github.com/hackebrot/pytest-covfefe.git
    """
    _origin_url = subprocess.check_output(
        ["git", "-C", str(tmp_local_repo), "remote", "get-url", "origin"]
    )
    got_url = _origin_url.strip().decode()

    expected_url = "https://github.com/hackebrot/pytest-covfefe.git"

    assert expected_url == got_url
