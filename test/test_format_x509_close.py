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
from fluidasserts.format import x509


# Constants

SSL_PORT = 443
NON_EXISTANT = '0.0.0.0'

#
# Closing tests
#


@pytest.mark.parametrize('get_mock_ip', ['ssl_hard'], indirect=True)
def test_cn_equal_to_site_close(get_mock_ip):
    """CN del cert concuerda con el nombre del sitio?."""
    assert not x509.is_cert_cn_not_equal_to_site(get_mock_ip, 80)
    assert not x509.is_cert_cn_not_equal_to_site('0.0.0.0')


@pytest.mark.parametrize('get_mock_ip', ['ssl_hard'], indirect=True)
def test_cn_wildcard_close(get_mock_ip):
    """CN del cert concuerda con el nombre del sitio?."""
    assert not x509.is_cert_cn_using_wildcard(get_mock_ip, 80)
    assert not x509.is_cert_cn_using_wildcard('0.0.0.0')


@pytest.mark.parametrize('get_mock_ip', ['ssl_hard'], indirect=True)
def test_cert_active_close(get_mock_ip):
    """Certificado aun esta vigente?."""
    assert not x509.is_cert_inactive(get_mock_ip)
    assert not x509.is_cert_inactive(get_mock_ip, 80)
    assert not x509.is_cert_inactive(NON_EXISTANT)


@pytest.mark.parametrize('get_mock_ip', ['ssl_hard'], indirect=True)
def test_cert_lifespan_safe_close(get_mock_ip):
    """Vigencia del certificado es segura?."""
    assert not x509.is_cert_validity_lifespan_unsafe(get_mock_ip)
    assert not x509.is_cert_validity_lifespan_unsafe(get_mock_ip, 80)
    assert not x509.is_cert_validity_lifespan_unsafe(NON_EXISTANT)


@pytest.mark.parametrize('get_mock_ip', ['ssl_hard'], indirect=True)
def test_is_sha1_used_close(get_mock_ip):
    """Presencia de SHA1 en los algoritmos de cifrado?."""
    assert not x509.is_sha1_used(get_mock_ip, SSL_PORT)
    assert not x509.is_sha1_used(get_mock_ip, 80)
    assert not x509.is_sha1_used(NON_EXISTANT, SSL_PORT)


@pytest.mark.parametrize('get_mock_ip', ['ssl_hard'], indirect=True)
def test_is_md5_used_close(get_mock_ip):
    """Presencia de MD5 en los algoritmos de cifrado?."""
    assert not x509.is_md5_used(get_mock_ip, SSL_PORT)
    assert not x509.is_md5_used(get_mock_ip, 80)
    assert not x509.is_md5_used(NON_EXISTANT, SSL_PORT)


@pytest.mark.parametrize('get_mock_ip', ['ssl_hard'], indirect=True)
def test_is_cert_trusted_close(get_mock_ip):
    """Check if cert is trusted."""
    assert not x509.is_cert_untrusted('google.com', SSL_PORT)
    assert not x509.is_cert_untrusted(get_mock_ip, 80)
    assert not x509.is_cert_untrusted(NON_EXISTANT, SSL_PORT)
