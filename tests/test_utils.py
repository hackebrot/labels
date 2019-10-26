from labels import utils


def test_get_owner_and_repo_from_cwd(tmp_local_repo, owner: str, repo: str) -> None:
    """Test that repo owner and name can be inferred from the
    local git repo in the current working directory.
    """
    with tmp_local_repo.as_cwd():
        assert utils.get_owner_and_repo_from_cwd() == (owner, repo)


def test_extract_o_and_r_from_remote_https_url() -> None:
    """Test extraction of owner and repo names from HTTPS remote url string."""
    remote_url = "https://github.com/hackebrot/pytest-covfefe.git"
    expected_owner = "hackebrot"
    expected_repo = "pytest-covfefe"

    gotten_owner, gotten_repo = utils._extract_o_and_r(remote_url)

    assert gotten_owner == expected_owner
    assert gotten_repo == expected_repo


def test_extract_o_and_r_from_remote_ssh_url() -> None:
    """Test extraction of owner and repo names from SSH remote url string."""
    remote_url = "git@github.com:hackebrot/pytest-covfefe.git"
    expected_owner = "hackebrot"
    expected_repo = "pytest-covfefe"

    gotten_owner, gotten_repo = utils._extract_o_and_r(remote_url)

    assert gotten_owner == expected_owner
    assert gotten_repo == expected_repo
