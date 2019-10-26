import subprocess
import typing


def get_owner_and_repo_from_cwd() -> typing.Tuple[str, str]:
    """Return the owner and name of the remote named origin in the cwd."""
    origin_url = (
        subprocess.check_output(["git", "remote", "get-url", "origin"]).decode().strip()
    )
    parts = origin_url.split("/")
    return (parts[-2], parts[-1].split('.')[-2])
