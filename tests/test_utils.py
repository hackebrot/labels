from labels import utils


def test_get_owner_and_repo_from_cwd(tmp_local_repo, owner: str, repo: str) -> None:
    """Test that repo owner and name can be inferred from the
    local git repo in the current working directory.
    """
    with tmp_local_repo.as_cwd():
        assert utils.get_owner_and_repo_from_cwd() == (owner, repo)
