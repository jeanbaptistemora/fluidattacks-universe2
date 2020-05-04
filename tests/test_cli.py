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


def test_resources_2(relocate, cli_runner):
    result = cli_runner(f'resources --mailmap {GROUP}'.split())
    assert result.exit_code == 0
    assert 'Mailmap sorted' in result.output


def test_resources_3(relocate, cli_runner):
    result = cli_runner(f'resources --read {GROUP}'.split())
    assert result.exit_code == 0


def test_forces_1(relocate, cli_runner):
    result = cli_runner(f'forces --run -d all bad-repo'.split())
    assert 'the group bad-repo does not exist' in result.output


def test_forces_2(relocate, cli_runner):
    result = cli_runner(f'forces --check-sync all {GROUP}'.split())
    assert result.exit_code == 0, result.output


def test_forces_3(relocate, cli_runner):
    result = cli_runner(f'forces --lint-exps all {GROUP}'.split())
    assert result.exit_code == 0, result.output


def test_forces_4(relocate, cli_runner):
    result = cli_runner(f'forces --run-exps --static all {GROUP}'.split())
    assert result.exit_code == 0
    assert '975673437.exp' in result.output


def test_forces_5(relocate, cli_runner):
    result = cli_runner(f'forces --run-exps --dynamic all {GROUP}'.split())
    assert result.exit_code == 0
    assert '720412598.exp' in result.output


def test_forces_6(relocate, cli_runner):
    plain_text = f'groups/{GROUP}/forces/dynamic/resources/plaintext.yml'

    result = cli_runner(f'forces --decrypt {GROUP}'.split())
    assert result.exit_code == 0
    assert os.path.isfile(plain_text)

    secretest = yaml.load(open(plain_text))
    assert secretest['secrets']['test_user'] == 'Einstein'
    assert secretest['secrets']['test_password'] == 'E=m*C^2'

    result = cli_runner(f'forces --encrypt {GROUP}'.split())
    assert result.exit_code == 0


def test_forces_7(relocate, cli_runner):
    result = cli_runner([
        'forces', '--upload-exps-from-repo-to-integrates', GROUP,
    ])

    assert result.exit_code == 0, result.output


def test_forces_8(relocate, cli_runner):
    result = cli_runner([
        'forces', '--upload-exps-from-repo-to-integrates', GROUP_BAD,
    ])

    assert result.exit_code != 0, result.output


def test_integrates_1(relocate, cli_runner):
    result = cli_runner(f'integrates --get-static-dict {GROUP}'.split())
    assert result.exit_code == 0
