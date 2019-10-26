import subprocess


def get_owner_from_cwd() -> str:
    """Return owner of the remote named origin in the current working directory."""
    origin_url = (
        subprocess.check_output(["git", "remote", "get-url", "origin"]).decode().strip()
    )
    return origin_url.split("/")[-2]
