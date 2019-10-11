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

        # Fill the username
        bot.fill_by_id('login', 'bee')
        bot.fill_by_id('password', 'bug')

        # Click the login button
        bot.click_by_name('form')

        # Test cookies
        cookies = bot.get_cookies()
        assert cookies
        cookie = bot.get_cookie('PHPSESSID')
        assert cookie


@pytest.mark.parametrize('get_mock_ip', ['bwapp'], indirect=True)
def test_httpbot_login_2(get_mock_ip):
    """The goal here is to test another functionality."""
    with HTTPBot(developer_mode=True) as bot:
        # Install BWAPP
        bot.visit(f'http://{get_mock_ip}/install.php?install=yes')

        # Login to BWAPP
        bot.visit(f'http://{get_mock_ip}/login.php')

        # Test filling a field that does not exists
        assert not bot.fill_by_id('asdfasdf', 'bug')

        # Usually you will be using this functions to inspect what buttons can
        #   be clicked on, and what fields can be filled
        fillables = bot.get_fillables()

        # Only two fields are fillable, the field for login, and field for password
        assert fillables[0]['id'] == 'login'
        assert fillables[0]['name'] == 'login'
        assert fillables[1]['id'] == 'password'
        assert fillables[1]['name'] == 'password'

        clickables = bot.get_clickables()

        # Only one field is clickable, the login button
        assert clickables[0]['name'] == 'form'
        assert clickables[0]['type'] == 'submit'
        assert clickables[0]['value'] == 'submit'
