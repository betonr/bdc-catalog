#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for BDC-Catalog CLI."""

import subprocess
import sys

from click.testing import CliRunner

from bdc_catalog.cli import cli


def test_basic_cli():
    """Test basic cli usage."""
    res = CliRunner().invoke(cli)

    assert res.exit_code == 0


def test_cli_module():
    """Test the BDCCatalog invoked as a module."""
    res = subprocess.call(f'{sys.executable} -m bdc_catalog', shell=True)

    assert res == 0
