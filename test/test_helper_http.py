# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.helper.http."""

# 3rd party imports
import pytest

# local imports
from fluidasserts.helper.http import HTTPBot


#
# Functional tests
#


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_httpbot_login_1(get_mock_ip):
    """The goal here is to be able to authenticate to BWAPP easily."""
    with HTTPBot() as bot:
        # Install BWAPP
        bot.visit(f'http://{get_mock_ip}/install.php?install=yes')

        # Login to BWAPP
        bot.visit(f'http://{get_mock_ip}/login.php')

        # Test all cookies
        cookies = bot.get_cookies()
        assert cookies

        # Test single cookie
        cookie = bot.get_cookie('PHPSESSID')
        assert cookie

        # Usually you will be using this functions to inspect what buttons can
        #   be clicked on, and what fields can be filled
        #
        # If you set the development mode, you'll get this for free in
        #   human readable form
        fillables = bot.get_fillables()

        # Only two fields are fillable:
        #   the field for login
        assert fillables[0]['id'] == 'login'
        assert fillables[0]['name'] == 'login'
        #   the field for password
        assert fillables[1]['id'] == 'password'
        assert fillables[1]['name'] == 'password'
