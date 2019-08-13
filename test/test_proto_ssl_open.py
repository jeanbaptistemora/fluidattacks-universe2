# -*- coding: utf-8 -*-

"""Modulo para pruebas de SSL.

Este modulo contiene las funciones necesarias para probar si el modulo de
SSL se encuentra adecuadamente implementado.
"""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest

# local imports
from fluidasserts.proto import ssl


# Constants

SSL_PORT = 443

#
# Open tests
#


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_pfs_enabled_open(get_mock_ip):
    """PFS habilitado en sitio?."""
    assert ssl.is_pfs_disabled(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_sslv3_enabled_open(get_mock_ip):
    """SSLv3 habilitado en sitio?."""
    assert ssl.is_sslv3_enabled(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_tlsv1_enabled_open(get_mock_ip):
    """TLSv1 habilitado en sitio?."""
    assert ssl.is_tlsv1_enabled(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_tlsv11_enabled_open(get_mock_ip):
    """TLSv1.1 habilitado en sitio?."""
    assert ssl.is_tlsv11_enabled(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_has_poodle_sslv3_open(get_mock_ip):
    """Sitio vulnerable a POODLE?."""
    assert ssl.has_poodle_sslv3(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_has_beast_open(get_mock_ip):
    """Sitio vulnerable a BEAST?."""
    assert ssl.has_beast(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_hard'], indirect=True)
def test_has_breach_open(get_mock_ip):
    """Presencia de la vulnerabilidad Breach?."""
    assert ssl.has_breach('fluidattacks.com', SSL_PORT)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_allows_weak_alg_open(get_mock_ip):
    """Sitio permite algoritmos debiles?."""
    assert ssl.allows_weak_ciphers(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_allows_anon_alg_open(get_mock_ip):
    """Sitio permite algoritmos anonimos?."""
    assert ssl.allows_anon_ciphers(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_has_heartbleed_open(get_mock_ip):
    """Heartbleed enabled?."""
    assert ssl.has_heartbleed(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_allows_modified_mac_open(get_mock_ip):
    """Host allows messages with modified MAC?."""
    assert not ssl.allows_modified_mac(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_not_tls13_enabled_open(get_mock_ip):
    """TLSv1.3 enabled?."""
    assert ssl.not_tls13_enabled(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_scsv_open(get_mock_ip):
    """TLS_FALLBACK_SCSV enabled?."""
    assert ssl.allows_insecure_downgrade(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_tls_cbc_open(get_mock_ip):
    """TLS CBC ciphers enabled?."""
    assert ssl.tls_uses_cbc(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_weak'], indirect=True)
def test_sweet32_open(get_mock_ip):
    """Check SWEET32."""
    assert ssl.has_sweet32(get_mock_ip)


@pytest.mark.parametrize('get_mock_ip', ['ssl_hard'], indirect=True)
def test_tlsv13_downgrade_open(get_mock_ip):
    """Check TLSv1.3 downgrade attack."""
    assert ssl.has_tls13_downgrade_vuln(get_mock_ip)
