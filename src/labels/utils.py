import re
import subprocess
import typing


def get_owner_and_repo_from_cwd() -> typing.Tuple[str, str]:
    """Return the owner and name of the remote named origin in the cwd."""
    origin_url = (
        subprocess.check_output(["git", "remote", "get-url", "origin"]).decode().strip()
    )
    return _extract_o_and_r(origin_url)


def _extract_o_and_r(url: str) -> typing.Tuple[str, str]:
    """Return the owner and repo name of a remote given its SSH or HTTPS url.

    HTTPS url format -> 'https://github.com/user/repo.git'
    SSH   url format -> 'git@github.com:user/repo.git'
    """
    parts = re.split(r"[@/:.]+", url)
    return (parts[-3], parts[-2])
