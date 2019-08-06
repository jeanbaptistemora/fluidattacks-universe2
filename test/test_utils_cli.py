# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.sca packages."""

# standard imports
import os
import pytest
import sys
from unittest.mock import patch

# 3rd party imports
# None

# local imports
from fluidasserts.utils import cli

# Constants
OPEN_EXP = 'test/static/example/test_open.py'
CLOSED_EXP = 'test/static/example/test_closed.py'
UNKNOWN_EXP = 'test/static/example/test_unknown.py'
ERROR_EXP = 'test/static/example/test_with_errors.py'
NO_EXP = 'non-existing-exploit'

#
# Open tests
#


def test_cli():
    """Run CLI."""
    os.environ['FA_STRICT'] = 'false'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", OPEN_EXP]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            assert not cli.main()


def test_cli_strict():
    """Run CLI in strict mode."""
    os.environ['FA_STRICT'] = 'true'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", OPEN_EXP]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            assert cli.main()


def test_cli_strict_with_rich_exit_codes():
    """Run CLI in strict mode."""
    os.environ['FA_STRICT'] = 'true'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", "--enrich-exit-codes", OPEN_EXP]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            assert cli.main()


def test_cli_strict_bad():
    """Run CLI with a bad FA_STRICT value."""
    os.environ['FA_STRICT'] = 'badvalue'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", OPEN_EXP]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            assert cli.main()


def test_cli_noargs():
    """Run CLI with no args."""
    os.environ['FA_STRICT'] = 'false'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            assert cli.main()


def test_cli_quiet():
    """Run CLI in quiet mode."""
    os.environ['FA_STRICT'] = 'false'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", "-q", OPEN_EXP]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            assert not cli.main()


def test_cli_output():
    """Run CLI output option."""
    log_file = "log.asserts"
    os.environ['FA_STRICT'] = 'false'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", "-q", "-O", log_file, OPEN_EXP]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            cli.main()
            assert os.path.exists(log_file)
            os.unlink(log_file)


def test_cli_color():
    """Run CLI in without colors."""
    os.environ['FA_STRICT'] = 'false'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", "-n", OPEN_EXP]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            assert not cli.main()


def test_cli_http():
    """Run CLI http option."""
    os.environ['FA_STRICT'] = 'true'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", "-eec", "-mp", "--http", 'https://127.0.0.1']
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code in (
            cli.RICH_EXIT_CODES[x] for x in ('open', 'closed', 'unknown'))


def test_cli_ssl():
    """Run CLI ssl option."""
    os.environ['FA_STRICT'] = 'true'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", "-eec", "-mp", "--ssl", '127.0.0.1:443']
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code in (
            cli.RICH_EXIT_CODES[x] for x in ('open', 'closed', 'unknown'))


def test_cli_aws():
    """Run CLI aws option."""
    os.environ['FA_STRICT'] = 'true'
    os.environ['FA_NOTRACK'] = 'true'
    key = os.environ['AWS_ACCESS_KEY_ID']
    secret = os.environ['AWS_SECRET_ACCESS_KEY']
    testargs = ["asserts", "-eec", "-mp", "--aws", f'{key}:{secret}']
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code in (
            cli.RICH_EXIT_CODES[x] for x in ('open', 'closed', 'unknown'))


def test_cli_dns():
    """Run CLI dns option."""
    os.environ['FA_STRICT'] = 'false'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", "-D", '127.0.0.1']
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            assert not cli.main()


def test_cli_lang():
    """Run CLI lang option."""
    os.environ['FA_STRICT'] = 'true'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", "-eec", "-mp", "--lang", 'test/static/lang']
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code in (
            cli.RICH_EXIT_CODES[x] for x in ('open', 'closed', 'unknown'))


def test_cli_filtered():
    """Run CLI with filtered results."""
    os.environ['FA_STRICT'] = 'false'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", "-cou", OPEN_EXP]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            assert not cli.main()


def test_cli_method_stats():
    """Run CLI with method stats flag."""
    os.environ['FA_STRICT'] = 'false'
    os.environ['FA_NOTRACK'] = 'true'
    testargs = ["asserts", "-ms", OPEN_EXP]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            assert not cli.main()


def test_exec_wrapper_success():
    """Run the exec wrapper and expects it catches the error."""
    with pytest.raises(BaseException):
        # The method should not propagate any exploit errors and handle them
        assert not cli.exec_wrapper(
            cli.get_exploit_content(OPEN_EXP))


def test_exec_wrapper_failure():
    """Run the exec wrapper and expects it catches the error."""
    with pytest.raises(BaseException):
        # The method should not propagate any exploit errors and handle them
        assert not cli.exec_wrapper(
            cli.get_exploit_content(ERROR_EXP))


def test_exit_codes_strict():
    """Test the exit codes running in strict mode."""
    os.environ['FA_STRICT'] = 'true'
    tests = [
        ('config-error', ["asserts"]),
        ('open', ["asserts", OPEN_EXP]),
        ('closed', ["asserts", CLOSED_EXP]),
        ('unknown', ["asserts", UNKNOWN_EXP]),
        ('exploit-error', ["asserts", ERROR_EXP]),
        ('exploit-not-found', ["asserts", NO_EXP]),

        ('open', ["asserts", UNKNOWN_EXP, OPEN_EXP, CLOSED_EXP]),
        ('open', ["asserts", OPEN_EXP, CLOSED_EXP]),
        ('open', ["asserts", UNKNOWN_EXP, OPEN_EXP]),

        ('exploit-error', ["asserts", ERROR_EXP, CLOSED_EXP]),
    ]
    for reason, argv in tests:
        with patch.object(sys, 'argv', argv):
            with pytest.raises(SystemExit) as exc:
                cli.main()
            assert exc.value.code == cli.EXIT_CODES[reason]


def test_exit_codes_non_strict():
    """Test the exit codes running in non strict mode."""
    os.environ['FA_STRICT'] = 'false'
    with patch.object(sys, 'argv', ["asserts"]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
    with patch.object(sys, 'argv', ["asserts", OPEN_EXP]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
    with patch.object(sys, 'argv', ["asserts", CLOSED_EXP]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
    with patch.object(sys, 'argv', ["asserts", UNKNOWN_EXP]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
    with patch.object(sys, 'argv', ["asserts", ERROR_EXP]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
    with patch.object(sys, 'argv', ["asserts", NO_EXP]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0


def test_rich_exit_codes_strict():
    """Test the rich exit codes running in strict mode."""
    os.environ['FA_STRICT'] = 'true'
    tests = [
        ('config-error', ["asserts", "-eec"]),
        ('open', ["asserts", "-eec", OPEN_EXP]),
        ('closed', ["asserts", "-eec", CLOSED_EXP]),
        ('unknown', ["asserts", "-eec", UNKNOWN_EXP]),
        ('exploit-error', ["asserts", "-eec", ERROR_EXP]),
        ('exploit-not-found', ["asserts", "-eec", NO_EXP]),

        ('unknown', ["asserts", "-eec", UNKNOWN_EXP, OPEN_EXP, CLOSED_EXP]),
        ('open', ["asserts", "-eec", OPEN_EXP, CLOSED_EXP]),
        ('unknown', ["asserts", "-eec", UNKNOWN_EXP, OPEN_EXP]),

        ('exploit-error', ["asserts", "-eec", ERROR_EXP, CLOSED_EXP]),
    ]
    for reason, argv in tests:
        with patch.object(sys, 'argv', argv):
            with pytest.raises(SystemExit) as exc:
                cli.main()
            assert exc.value.code == cli.RICH_EXIT_CODES[reason]


def test_rich_exit_codes_non_strict():
    """Test the rich exit codes running in non strict mode."""
    os.environ['FA_STRICT'] = 'false'
    with patch.object(sys, 'argv', ["asserts", "-eec"]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
    with patch.object(sys, 'argv', ["asserts", "-eec", OPEN_EXP]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
    with patch.object(sys, 'argv', ["asserts", "-eec", CLOSED_EXP]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
    with patch.object(sys, 'argv', ["asserts", "-eec", UNKNOWN_EXP]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
    with patch.object(sys, 'argv', ["asserts", "-eec", ERROR_EXP]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
    with patch.object(sys, 'argv', ["asserts", "-eec", NO_EXP]):
        with pytest.raises(SystemExit) as exc:
            cli.main()
        assert exc.value.code == 0
