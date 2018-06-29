import typing

import attr
import requests

from labels.exceptions import GitHubException


def not_read_only(attr: attr.Attribute, value: typing.Any) -> bool:
    """Filter for attr that checks for a leading underscore."""
    return not attr.name.startswith("_")


@attr.s(auto_attribs=True, frozen=True)
class Label:
    """Represents a GitHub issue label."""

    color: str
    description: str
    name: str

    # Read-only attributes
    _default: bool = False
    _id: int = 0
    _node_id: str = ""
    _url: str = ""

    @property
    def params_dict(self) -> typing.Dict[str, typing.Any]:
        """Return label parameters as a dict."""
        return attr.asdict(self, recurse=True, filter=not_read_only)

    @property
    def params_tuple(self) -> typing.Tuple[typing.Any, ...]:
        """Return label parameters as a tuple."""
        return attr.astuple(self, recurse=True, filter=not_read_only)

    def __eq__(self, other: typing.Any) -> typing.Any:
        """Check for equality with the given object."""
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.params_tuple == other.params_tuple

    def __hash__(self) -> int:
        """Return a hash for the Label."""
        return hash((self.__class__, *self.params_tuple))


class Client:
    base_url: str
    session: requests.Session

    def __init__(
        self,
        auth: requests.auth.AuthBase,
        base_url: str = "https://api.github.com",
    ) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = auth

    def list_labels(self, owner: str, repo: str) -> typing.List[Label]:
        """Return the list of Labels from the repository.

        GitHub API docs:
        https://developer.github.com/v3/issues/labels/#list-all-labels-for-this-repository
        """
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/labels"

        response = self.session.get(
            endpoint,
            headers={"Accept": "application/vnd.github.symmetra-preview+json"},
        )

        if response.status_code != 200:
            raise GitHubException(
                f"Error retrieving labels: "
                "{response.status_code} - "
                "{response.reason}"
            )

        return [Label(**data) for data in response.json()]

    def get_label(self, owner: str, repo: str, name: str) -> Label:
        """Return a single Label from the repository.

        GitHub API docs:
        https://developer.github.com/v3/issues/labels/#get-a-single-label
        """
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/labels/{name}"

        response = self.session.get(
            endpoint,
            headers={"Accept": "application/vnd.github.symmetra-preview+json"},
        )

        if response.status_code != 200:
            raise GitHubException(
                f"Error retrieving label: "
                "{response.status_code} - "
                "{response.reason}"
            )

        return Label(**response.json())

    def create_label(self, owner: str, repo: str, *, label: Label) -> Label:
        """Create a new Label for the repository.

        GitHub API docs:
        https://developer.github.com/v3/issues/labels/#create-a-label
        """

        endpoint = f"{self.base_url}/repos/{owner}/{repo}/labels"

        response = self.session.post(
            endpoint,
            headers={"Accept": "application/vnd.github.symmetra-preview+json"},
            data=label.params_dict,
        )

        if response.status_code != 201:
            raise GitHubException(
                f"Error creating label: "
                "{response.status_code} - "
                "{response.reason}"
            )

        return Label(**response.json())

    def edit_label(
        self, owner: str, repo: str, name: str, *, label: Label
    ) -> Label:
        """Update a GitHub issue label.

        GitHub API docs:
        https://developer.github.com/v3/issues/labels/#update-a-label
        """
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/labels/{name}"

        response = self.session.patch(
            endpoint,
            headers={"Accept": "application/vnd.github.symmetra-preview+json"},
            data=label.params_dict,
        )

        if response.status_code != 200:
            raise GitHubException(
                f"Error editing label: "
                "{response.status_code} - "
                "{response.reason}"
            )

        return Label(**response.json())
