# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.php."""

# standard imports
# None

# 3rd party imports
import pytest
pytestmark = pytest.mark.lang

# local imports
from fluidasserts.lang import php

# Constants

CODE_DIR = 'test/static/lang/php/'
SECURE_CODE = CODE_DIR + 'safe_code.php'
INSECURE_CODE = CODE_DIR + 'vuln_code.php'
NON_EXISTANT_CODE = CODE_DIR + 'not_exists.php'


#
# Open tests
#

def test_has_preg_rce_open():
    """Code uses unsafe preg_replace."""
    assert php.has_preg_ce(INSECURE_CODE).is_open()
    assert php.has_preg_ce(CODE_DIR).is_open()


#
# Closing tests
#


def test_has_preg_rce_close():
    """Code uses unsafe preg_replace."""
    assert php.has_preg_ce(SECURE_CODE).is_closed()
    assert php.has_preg_ce(CODE_DIR, exclude=['test']).is_closed()


#
# Unknown tests
#


def test_has_preg_rce_unknown():
    """Code uses unsafe preg_replace."""
    assert php.has_preg_ce(NON_EXISTANT_CODE).is_unknown()
