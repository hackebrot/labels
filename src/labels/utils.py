import logging
import re
import shlex
import subprocess
import typing


from labels.github import Repository


REMOTE_REGEX = re.compile(
    r"^(https|git)(:\/\/|@)github\.com[\/:](?P<owner>[^\/:]+)\/(?P<name>.*?)(\.git)?$"
)


def load_repository_info(remote_name: str = "origin") -> typing.Optional[Repository]:
    """Load repository information from the local working tree.

    HTTPS url format -> 'https://github.com/owner/name.git'
    SSH   url format -> 'git@github.com:owner/name.git'
    """
    logger = logging.getLogger("labels")
    logger.debug(f"Load repository information for '{remote_name}'.")

    proc = subprocess.run(
        shlex.split(f"git remote get-url {remote_name}"),
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )

    if proc.returncode != 0:
        logger.debug(f"Error running git remote get-url.")
        return None

    remote_url = proc.stdout.strip()
    match = REMOTE_REGEX.match(remote_url)

    if match is None:
        logger.debug(f"No match for remote URL: {remote_url}.")
        return None

    return Repository(owner=match.group("owner"), name=match.group("name"))
