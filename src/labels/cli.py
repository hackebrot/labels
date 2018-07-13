import logging
import operator
import sys
import typing

import click
from requests.auth import HTTPBasicAuth

from labels import __version__
from labels.exceptions import LabelsException
from labels.github import Client, Label
from labels.io import write_labels, read_labels
from labels.log import create_logger

Labels_Dict = typing.Dict[str, Label]


@click.group()
@click.pass_context
@click.version_option(__version__, "-V", "--version", prog_name="labels")
@click.option("-v", "--verbose", help="Print debug information", is_flag=True)
@click.option(
    "-u",
    "--username",
    help="GitHub username",
    type=str,
    required=True,
    envvar="LABELS_USERNAME",
)
@click.option(
    "-t",
    "--token",
    help="GitHub access token",
    type=str,
    required=True,
    envvar="LABELS_TOKEN",
)
def labels(ctx, username: str, token: str, verbose: bool) -> None:
    """labels - CLI to manage GitHub issue labels."""

    logger = create_logger()
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Logger initialized")
    else:
        logger.setLevel(logging.INFO)

    ctx.obj = Client(HTTPBasicAuth(username, token))


@labels.command("fetch")
@click.pass_obj
@click.option("-o", "--owner", help="GitHub owner name", type=str, required=True)
@click.option("-r", "--repo", help="GitHub repository name", type=str, required=True)
@click.option(
    "-f",
    "--filename",
    help="Filename for labels",
    default="labels.toml",
    type=click.Path(),
    required=True,
)
def fetch_cmd(client: Client, owner: str, repo: str, filename: str) -> None:
    """Fetch labels for a GitHub repository.

    This will write the labels information to disk to the specified filename.
    """
    try:
        labels = client.list_labels(owner, repo)
    except LabelsException as exc:
        click.echo(str(exc))
        sys.exit(1)

    write_labels(
        filename,
        sorted(labels, key=operator.attrgetter("name", "description", "color")),
    )


@labels.command("sync")
@click.pass_obj
@click.option("-o", "--owner", help="GitHub owner name", type=str, required=True)
@click.option("-r", "--repo", help="GitHub repository name", type=str, required=True)
@click.option("-n", "--dryrun", help="Do not modify remote labels", is_flag=True)
@click.option(
    "-f",
    "--filename",
    help="Filename for labels",
    default="labels.toml",
    type=click.Path(exists=True),
    required=True,
)
def sync_cmd(
    client: Client, owner: str, repo: str, filename: str, dryrun: bool
) -> None:
    """Sync labels with a GitHub repository.

    On success this will also update the local labels file, so that section
    names match the `name` parameter.
    """
    labels_to_delete = {}
    labels_to_update = {}
    labels_to_create = {}
    labels_to_ignore = {}

    local_labels = read_labels(filename)

    try:
        remote_labels = {l.name: l for l in client.list_labels(owner, repo)}
    except LabelsException as exc:
        click.echo(str(exc), err=True)
        sys.exit(1)

    for remote_name, local_label in local_labels.items():
        if remote_name in remote_labels:

            remote_label = remote_labels[remote_name]

            if local_label.params_dict == remote_label.params_dict:
                labels_to_ignore[remote_name] = local_label
            else:
                labels_to_update[remote_name] = local_label
        else:
            if remote_name == local_label.name:
                labels_to_create[local_label.name] = local_label
            else:
                click.echo(
                    f'There is no remote label "{remote_name}" and '
                    f"this name does not match the name "
                    f'parameter: "{local_label.name}"',
                    err=True,
                )
                sys.exit(1)

    for remote_name, remote_label in remote_labels.items():
        if remote_name in labels_to_update:
            continue

        if remote_name in labels_to_ignore:
            continue

        labels_to_delete[remote_name] = remote_label

    if dryrun:
        # Do not modify remote labels, but only print info
        dryrun_echo(
            labels_to_delete, labels_to_update, labels_to_create, labels_to_ignore
        )
        sys.exit(0)

    failures = []

    for name in labels_to_delete.keys():
        try:
            client.delete_label(owner, repo, name=name)
        except LabelsException as exc:
            click.echo(str(exc), err=True)
            failures.append(name)

    for name, label in labels_to_update.items():
        try:
            client.edit_label(owner, repo, name=name, label=label)
        except LabelsException as exc:
            click.echo(str(exc), err=True)
            failures.append(name)

    for name, label in labels_to_create.items():
        try:
            client.create_label(owner, repo, label=label)
        except LabelsException as exc:
            click.echo(str(exc), err=True)
            failures.append(name)

    if failures:
        sys.exit(1)

    # Make sure to write the local labels file to update TOML sections
    write_labels(
        filename,
        sorted(
            local_labels.values(),
            key=operator.attrgetter("name", "description", "color"),
        ),
    )


def dryrun_echo(
    labels_to_delete: Labels_Dict,
    labels_to_update: Labels_Dict,
    labels_to_create: Labels_Dict,
    labels_to_ignore: Labels_Dict,
) -> None:
    """Print information about how labels would be updated on sync."""

    if labels_to_delete:
        click.echo(f"This would delete the following labels:")
        for name in labels_to_delete:
            click.echo(f"  - {name}")

    if labels_to_update:
        click.echo(f"This would update the following labels:")
        for name in labels_to_update:
            click.echo(f"  - {name}")

    if labels_to_create:
        click.echo(f"This would create the following labels:")
        for name in labels_to_create:
            click.echo(f"  - {name}")

    if labels_to_ignore:
        click.echo(f"This would NOT modify the following labels:")
        for name in labels_to_ignore:
            click.echo(f"  - {name}")
