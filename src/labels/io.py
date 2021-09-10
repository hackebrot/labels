import logging
import typing

import tomli
import tomli_w

from labels.github import Label


def write_labels(filename: str, labels: typing.List[Label]) -> None:
    """Dump labels to the given TOML file."""
    logger = logging.getLogger("labels")
    logger.debug(f"Writing labels to {filename}")

    obj = {label.name: label.params_dict for label in labels}

    with open(filename, "wb") as labels_file:
        tomli_w.dump(obj, labels_file)


def read_labels(filename: str) -> typing.Dict[str, Label]:
    """Load labels from the given TOML file."""
    logger = logging.getLogger("labels")
    logger.debug(f"Reading labels from {filename}")

    with open(filename, "rb") as labels_file:
        obj = tomli.load(labels_file)

    return {name: Label(**values) for name, values in obj.items()}
