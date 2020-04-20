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

SUBS = 'continuoustest'


# test resources command
def test_resources(relocate):
    runner = CliRunner()

    test_does_subs_exist = runner.invoke(
        cli, f'resources --does-subs-exist {SUBS}'.split())
    assert test_does_subs_exist.exit_code == 0

    test_mailmap = runner.invoke(cli,
                                 f'resources --mailmap {SUBS}'.split())

    assert test_mailmap.exit_code == 0
    assert 'Mailmap sorted' in test_mailmap.output

    test_read = runner.invoke(cli, f'resources --read {SUBS}'.split())
    assert test_read.exit_code == 0


# test forces command
def test_forces(relocate):
    runner = CliRunner()

    bad_subs = runner.invoke(cli, f'forces --run -d all bad-repo'.split())

    assert 'the subscription bad-repo does not exist' in bad_subs.output

    test_check_sync = runner.invoke(
        cli, f'forces --check-sync all {SUBS}'.split())
    assert test_check_sync.exit_code == 0, test_check_sync.output

    test_lint_exps = runner.invoke(
        cli, f'forces --lint-exps all {SUBS}'.split())
    assert test_lint_exps.exit_code == 0

    test_run_static = runner.invoke(
        cli, f'forces --run-exps --static all {SUBS}'.split())
    assert test_run_static.exit_code == 0
    assert 'fin-0002-975673437.exp' in test_run_static.output
    assert 'fin-0077-508273958.cannot.exp' in test_run_static.output

    test_run_dynamic = runner.invoke(
        cli, f'forces --run-exps --dynamic all {SUBS}'.split())
    assert test_run_dynamic.exit_code == 0
    assert 'fin-0001-720412598.exp' in test_run_dynamic.output
    assert 'fin-0002-975673437.cannot.exp' in test_run_dynamic.output

    plain_text = (f'subscriptions/{SUBS}/break-build/'
                  'dynamic/resources/plaintext.yml')
    test_decrypt = runner.invoke(cli,
                                 f'forces --decrypt {SUBS}'.split())
    assert test_decrypt.exit_code == 0
    assert os.path.isfile(plain_text)

    secretest = yaml.load(open(plain_text))
    assert secretest['secrets']['test_user'] == 'Einstein'
    assert secretest['secrets']['test_password'] == 'E=m*C^2'

    test_encrypt = runner.invoke(cli,
                                 f'forces --encrypt {SUBS}'.split())
    assert test_encrypt.exit_code == 0


# test integrates command
def test_integrates(relocate):
    runner = CliRunner()

    test_get_dict = runner.invoke(
        cli, f'integrates --get-static-dict {SUBS}'.split())
    assert test_get_dict.exit_code == 0
