import logging
from typing import Any, Dict, List, Optional, Tuple

import attr
import requests

from labels.exceptions import GitHubException


@attr.s(auto_attribs=True, frozen=True)
class Repository:
    """Represents a GitHub repository."""

    owner: str
    name: str


def not_read_only(attr: attr.Attribute, value: Any) -> bool:
    """Filter for attr that checks for a leading underscore."""
    return not attr.name.startswith("_")


@attr.s(auto_attribs=True, frozen=True)
class Label:
    """Represents a GitHub issue label."""

    color: str
    name: str
    description: str = ""

    # Read-only attributes
    _default: bool = False
    _id: int = 0
    _node_id: str = ""
    _url: str = ""

    @property
    def params_dict(self) -> Dict[str, Any]:
        """Return label parameters as a dict."""
        return attr.asdict(self, recurse=True, filter=not_read_only)

    @property
    def params_tuple(self) -> Tuple[Any, ...]:
        """Return label parameters as a tuple."""
        return attr.astuple(self, recurse=True, filter=not_read_only)


class Client:
    base_url: str
    session: requests.Session

    def __init__(
        self, auth: requests.auth.AuthBase, base_url: str = "https://api.github.com"
    ) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = auth

    def list_labels(self, repo: Repository) -> List[Label]:
        """Return the list of Labels from the repository.

        GitHub API docs:
        https://developer.github.com/v3/issues/labels/#list-all-labels-for-this-repository
        """
        logger = logging.getLogger("labels")
        logger.debug(f"Requesting labels for {repo.owner}/{repo.name}")

        headers = {"Accept": "application/vnd.github.symmetra-preview+json"}

        response = self.session.get(
            f"{self.base_url}/repos/{repo.owner}/{repo.name}/labels", headers=headers
        )

        if response.status_code != 200:
            raise GitHubException(
                f"Error retrieving labels: "
                f"{response.status_code} - "
                f"{response.reason}"
            )

        repo_labels: List[Dict] = response.json()

        next_page: Optional[Dict] = response.links.get("next", None)

        while next_page is not None:

            logger.debug(f"Requesting next page of labels")
            response = self.session.get(next_page["url"], headers=headers)

            if response.status_code != 200:
                raise GitHubException(
                    f"Error retrieving next page of labels: "
                    f"{response.status_code} - "
                    f"{response.reason}"
                )

            repo_labels.extend(response.json())

            next_page = response.links.get("next", None)

        return [Label(**label) for label in repo_labels]

    def get_label(self, repo: Repository, *, name: str) -> Label:
        """Return a single Label from the repository.

        GitHub API docs:
        https://developer.github.com/v3/issues/labels/#get-a-single-label
        """
        logger = logging.getLogger("labels")
        logger.debug(f"Requesting label '{name}' for {repo.owner}/{repo.name}")

        response = self.session.get(
            f"{self.base_url}/repos/{repo.owner}/{repo.name}/labels/{name}",
            headers={"Accept": "application/vnd.github.symmetra-preview+json"},
        )

        if response.status_code != 200:
            raise GitHubException(
                f"Error retrieving label {name}: "
                f"{response.status_code} - "
                f"{response.reason}"
            )

        return Label(**response.json())

    def create_label(self, repo: Repository, *, label: Label) -> Label:
        """Create a new Label for the repository.

        GitHub API docs:
        https://developer.github.com/v3/issues/labels/#create-a-label
        """
        logger = logging.getLogger("labels")
        logger.debug(f"Creating label '{label.name}' for {repo.owner}/{repo.name}")

        response = self.session.post(
            f"{self.base_url}/repos/{repo.owner}/{repo.name}/labels",
            headers={"Accept": "application/vnd.github.symmetra-preview+json"},
            json=label.params_dict,
        )

        if response.status_code != 201:
            raise GitHubException(
                f"Error creating label {label.name}: "
                f"{response.status_code} - "
                f"{response.reason}"
            )

        return Label(**response.json())

    def edit_label(self, repo: Repository, *, name: str, label: Label) -> Label:
        """Update a GitHub issue label.

        GitHub API docs:
        https://developer.github.com/v3/issues/labels/#update-a-label
        """
        logger = logging.getLogger("labels")
        logger.debug(f"Editing label '{name}' for {repo.owner}/{repo.name}")

        response = self.session.patch(
            f"{self.base_url}/repos/{repo.owner}/{repo.name}/labels/{name}",
            headers={"Accept": "application/vnd.github.symmetra-preview+json"},
            json=label.params_dict,
        )

        if response.status_code != 200:
            raise GitHubException(
                f"Error editing label {name}: "
                f"{response.status_code} - "
                f"{response.reason}"
            )

        return Label(**response.json())

    def delete_label(self, repo: Repository, *, name: str) -> None:
        """Delete a GitHub issue label.

        GitHub API docs:
        https://developer.github.com/v3/issues/labels/#delete-a-label
        """
        logger = logging.getLogger("labels")
        logger.debug(f"Deleting label '{name}' for {repo.owner}/{repo.name}")

        response = self.session.delete(
            f"{self.base_url}/repos/{repo.owner}/{repo.name}/labels/{name}"
        )

        if response.status_code != 204:
            raise GitHubException(
                f"Error deleting label {name}: "
                f"{response.status_code} - "
                f"{response.reason}"
            )
