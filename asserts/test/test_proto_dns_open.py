# -*- coding: utf-8 -*-

"""Modulo para pruebas de DNS.

Este modulo contiene las funciones necesarias para probar si el modulo de
DNS se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('proto_dns')

# local imports
from fluidasserts.proto import dns


# Constants

TEST_ZONE = 'fluid.la'
WEAK_PORT = 53
HARD_PORT = 53


#
# Open tests
#

@pytest.mark.parametrize('get_mock_ip', ['dns_weak'], indirect=True)
def test_is_dynupdate_enabled_open(get_mock_ip):
    """Dynamic update enabled?."""
    assert dns.is_dynupdate_enabled(TEST_ZONE, get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['dns_weak'], indirect=True)
def test_is_xfr_enabled_open(get_mock_ip):
    """Transferencia de zonas habilitado en server?."""
    assert dns.is_xfr_enabled(TEST_ZONE, get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['dns_weak'], indirect=True)
def test_has_cache_poison_open(get_mock_ip):
    """Server vulnerable a cache poison?."""
    assert dns.has_cache_poison(TEST_ZONE, get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['dns_weak'], indirect=True)
def test_has_cache_snooping_open(get_mock_ip):
    """Server vulnerable a cache snooping?."""
    assert dns.has_cache_snooping(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['dns_weak'], indirect=True)
def test_has_recursion_open(get_mock_ip):
    """Server has recursion enabled?."""
    assert dns.has_recursion(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['dns_weak'], indirect=True)
def test_has_subdomain_takeover(get_mock_ip):
    """Test has_subdomain_takeover."""
    controlled_domains_1: list = [
        # An attacker is able to claim a subdomain here
        # Let's assume this is GitHub Pages IP
        '20.20.20.20',
    ]
    controlled_domains_2: list = [
        # An attacker is able to claim a subdomain here
        # because it points to 20.20.20.20 by CNAME
        'subdomaintakeover.fluid.la',
    ]
    controlled_domains_3: list = [
        # An attacker is able to claim a subdomain here
        # Let's assume this is GitHub Pages IPv6
        '2400:cb00:2049:1::a29f:1804',
    ]
    assert dns.has_subdomain_takeover(
        'engineering.fluid.la', get_mock_ip, controlled_domains_1).is_open()
    assert dns.has_subdomain_takeover(
        'engineering.fluid.la', get_mock_ip, controlled_domains_2).is_open()
    assert dns.has_subdomain_takeover(
        'engineering.fluid.la', get_mock_ip, controlled_domains_3).is_open()


@pytest.mark.parametrize('get_mock_ip', ['dns_weak'], indirect=True)
def test_can_amplify_open(get_mock_ip):
    """Server can perform DNS amplification attacks?."""
    assert dns.can_amplify(get_mock_ip)
