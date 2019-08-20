# -*- coding: utf-8 -*-

"""Modulo para pruebas de DNS.

Este modulo contiene las funciones necesarias para probar si el modulo de
DNS se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest

# local imports
from fluidasserts.proto import dns


# Constants

TEST_ZONE = 'fluid.la'
WEAK_PORT = 53
HARD_PORT = 53

#
# Closing tests
#


@pytest.mark.parametrize('get_mock_ip', ['dns_hard'], indirect=True)
def test_is_xfr_enabled_close(get_mock_ip):
    """Transferencia de zonas habilitado en server?."""
    assert not dns.is_xfr_enabled(TEST_ZONE, get_mock_ip)
    assert not dns.is_xfr_enabled(TEST_ZONE, '0.0.0.0')


@pytest.mark.parametrize('get_mock_ip', ['dns_hard'], indirect=True)
def test_is_dynupdates_enabled_close(get_mock_ip):
    """Actualizacion de zonas habilitado en server?."""
    assert not dns.is_dynupdate_enabled(TEST_ZONE, get_mock_ip)
    assert not dns.is_dynupdate_enabled(TEST_ZONE, '200.200.200.200')


@pytest.mark.parametrize('get_mock_ip', ['dns_hard'], indirect=True)
def test_has_cache_poison_close(get_mock_ip):
    """Server vulnerable a cache poison?."""
    assert not dns.has_cache_poison(TEST_ZONE, get_mock_ip)
    assert not dns.has_cache_poison(TEST_ZONE, '200.200.200.200')


@pytest.mark.parametrize('get_mock_ip', ['dns_hard'], indirect=True)
def test_has_cache_snooping_close(get_mock_ip):
    """Server vulnerable a cache snooping?."""
    assert not dns.has_cache_snooping(get_mock_ip)
    assert not dns.has_cache_snooping('200.200.200.200')


@pytest.mark.parametrize('get_mock_ip', ['dns_hard'], indirect=True)
def test_has_recursion_close(get_mock_ip):
    """Server vulnerable a cache snooping?."""
    assert not dns.has_recursion(get_mock_ip)
    assert not dns.has_recursion('0.0.0.0')


@pytest.mark.parametrize('get_mock_ip', ['dns_hard'], indirect=True)
def test_can_amplify_close(get_mock_ip):
    """Server can perform DNS amplification attacks?."""
    assert not dns.can_amplify(get_mock_ip)
    assert not dns.can_amplify('0.0.0.0')


@pytest.mark.parametrize('get_mock_ip', ['dns_hard'], indirect=True)
def test_has_subdomain_takeover(get_mock_ip):
    """Test has_subdomain_takeover."""
    controlled_domains: list = [
        # An attacker is not able to claim this site because it's already
        # taken
        'www.fluid.la',
    ]
    assert dns.has_subdomain_takeover(
        'fluid.la', get_mock_ip, controlled_domains).is_closed()
    assert dns.has_subdomain_takeover(
        get_mock_ip, get_mock_ip, controlled_domains).is_unknown()
    assert dns.has_subdomain_takeover(
        '0.0.0.0', get_mock_ip, controlled_domains).is_unknown()
