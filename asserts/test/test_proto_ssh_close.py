# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Modulo para pruebas de SSH.

Este modulo contiene las funciones necesarias para probar si el modulo de
SSH se encuentra adecuadamente implementado.
"""


from __future__ import (
    print_function,
)

import pytest

pytestmark = pytest.mark.asserts_module("proto_ssh")


from fluidasserts.proto import (
    ssh,
)

#
# Constants
#

SSH_PORT = 22
ADMIN_USER = "nonpriv"
ADMIN_PASS = "ahgh7xee9eewaeGh"
NON_EXISTANT_SERVER = "0.0.0.0"
USER_LIST = ["root", "faustino"]
FAKE_USERS = ["AAAAA", "bbbbb"]

#
# Open tests
#


@pytest.mark.parametrize("get_mock_ip", ["os_hard"], indirect=True)
def test_is_hmac_used_close(get_mock_ip):
    """Server SSH uses HMAC?."""
    assert not ssh.is_hmac_used(
        get_mock_ip, username=ADMIN_USER, password=ADMIN_PASS
    )
    assert not ssh.is_hmac_used(
        get_mock_ip, port=24, username=ADMIN_USER, password=ADMIN_PASS
    )
    assert not ssh.is_hmac_used(
        NON_EXISTANT_SERVER, username=ADMIN_USER, password=ADMIN_PASS
    )


@pytest.mark.parametrize("get_mock_ip", ["os_hard"], indirect=True)
def test_is_is_cbc_used_close(get_mock_ip):
    """Server SSH uses CBC?."""
    assert not ssh.is_cbc_used(
        get_mock_ip, username=ADMIN_USER, password=ADMIN_PASS
    )
    assert not ssh.is_cbc_used(
        get_mock_ip, port=24, username=ADMIN_USER, password=ADMIN_PASS
    )
    assert not ssh.is_cbc_used(
        NON_EXISTANT_SERVER, username=ADMIN_USER, password=ADMIN_PASS
    )


@pytest.mark.parametrize("get_mock_ip", ["ssh_hard"], indirect=True)
def test_has_user_enumeration_close(get_mock_ip):
    """Server SSH has user enumeration?."""
    assert not ssh.has_user_enumeration(
        get_mock_ip, user_list=USER_LIST, fake_users=FAKE_USERS
    )
