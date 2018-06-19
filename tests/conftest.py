# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner

from labels.cli import labels


@pytest.fixture
def run_cli() -> callable:
    runner = CliRunner()

    def run(*args, **kwargs):
        return runner.invoke(labels, [*args])

    return run
