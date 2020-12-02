# Standard library
import sys
import shlex
import os
import yaml

# Third parties libraries
import pytest
import unittest.mock
from click.testing import CliRunner

# Local libraries
from toolbox.cli import entrypoint as cli

# constants

GROUP = 'continuoustest'
GROUP_BAD = 'does-not-exist'


def test_resources_1(relocate, cli_runner):
    result = cli_runner(f'utils --does-subs-exist {GROUP}'.split())
    assert result.exit_code == 0


def test_resources_3(relocate, cli_runner):
    result = cli_runner(f'resources --read-dev {GROUP}'.split())
    assert result.exit_code == 0


def test_integrates_1(relocate, cli_runner):
    result = cli_runner(
        f'integrates --get-static-dict all all {GROUP}'.split())
    assert result.exit_code == 0
