# -*- coding: utf-8 -*-

import logging
import click

from labels import __version__
from labels.log import create_logger


@click.group()
@click.pass_context
@click.option("-v", "--verbose", help="Print debug information", is_flag=True)
@click.version_option(__version__, "-V", "--version", prog_name="labels")
def labels(ctx, verbose: bool) -> None:
    """labels - CLI to manage GitHub issue labels."""
    logger = create_logger()
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Logger initialized")
    else:
        logger.setLevel(logging.INFO)


@labels.command("download")
@click.option("-u", "--username", help="GitHub user name", required=True)
@click.option("-p", "--project", help="GitHub project name", required=True)
def download_cmd(username: str, project: str) -> None:
    logger = logging.getLogger("labels")
    logger.debug(f"https://github.com/{username}/{project}")
