import typing

import tomli

from labels.github import Label
from labels.io import write_labels, read_labels


def test_write_labels(
    labels_file_write: str, labels: typing.List[Label], labels_file_dict: str
) -> None:
    """Test that write_labels() writes a TOML file, mapping names to Label
    parameters.
    """
    write_labels(labels_file_write, labels)

    with open(labels_file_write, "rb") as labels_file:
        obj = tomli.load(labels_file)

    assert obj == labels_file_dict


def test_load_labels(labels_file_load: str, labels: typing.List[Label]) -> None:
    """Test that read_lables() correctly reads the TOML file and returns a
    mapping of names to Label instances.
    """
    want = {label.name: label for label in labels}
    got = read_labels(labels_file_load)

    assert got == want
