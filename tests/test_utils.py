from labels import utils


def test_get_owner_from_cwd(tmp_local_repo) -> None:
    """Test that the repository owner can be infered from the
    local git repo in the current working directory.
    """
    with tmp_local_repo.as_cwd():
        assert utils.get_owner_from_cwd() == "hackebrot"
