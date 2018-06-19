# -*- coding: utf-8 -*-

import pytest

from labels import __version__


@pytest.mark.parametrize("version_option", ["-V", "--version"])
def test_version_option(run_cli: callable, version_option: str) -> None:
    result = run_cli(version_option)
    assert result.exit_code == 0
    assert result.output == f"labels, version {__version__}\n"
