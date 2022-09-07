# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.helper.asynchronous."""


import aiohttp
import asyncio
import pytest

pytestmark = pytest.mark.asserts_module("helper")


from fluidasserts.helper import (
    asynchronous,
)

#
# Tests
#


def test_is_timeout_error():
    """Test asynchronous.is_timeout_error."""
    assert asynchronous.is_timeout_error(asyncio.TimeoutError())


def test_is_connection_error():
    """Test asynchronous.is_connection_error."""
    assert asynchronous.is_connection_error(
        aiohttp.client_exceptions.ClientConnectionError()
    )


def test_is_parameter_error():
    """Test asynchronous.is_parameter_error."""
    assert asynchronous.is_parameter_error(
        aiohttp.client_exceptions.InvalidURL("localhost:8080")
    )
