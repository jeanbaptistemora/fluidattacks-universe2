# -*- coding: utf-8 -*-
"""Modulo SSL."""

# standard imports
from __future__ import absolute_import
import logging
import socket

# 3rd party imports
import certifi
import datetime
import ssl
import tlslite
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import banner_helper

PORT = 443

logger = logging.getLogger('FLUIDAsserts')


def is_cert_cn_not_equal_to_site(site, port=PORT):
    """Function to check whether cert cn is equal to site."""
    result = True
    has_sni = False
    try:
        cert = ssl.get_server_certificate((site, port))
    except:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            wrapped_socket = ssl.SSLSocket(sock=sock,
                                           ca_certs=certifi.where(),
                                           cert_reqs=ssl.CERT_REQUIRED,
                                           server_hostname=site)
            wrapped_socket.connect((site, port))
            __cert = wrapped_socket.getpeercert(True)
            cert = ssl.DER_cert_to_PEM_cert(__cert)
            has_sni = True
        except socket.error:
            logger.info('%s: Port closed, Details=%s:%s',
                         show_unknown(), site, port)
            return False

    cert_obj = load_pem_x509_certificate(cert.encode('utf-8'),
                                         default_backend())
    cert_cn = \
        cert_obj.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[
            0].value

    wildcard_site = '*.' + site

    main_domain = 'NONE'
    if cert_cn.startswith('*.'):
        main_domain = '.' + cert_cn.split('*.')[1]

    if site != cert_cn and wildcard_site != cert_cn and not site.endswith(main_domain):
        if has_sni:
            logger.info('%s: %s CN not equals to site. However server \
supports SNI, Details=%s:%s', show_close(), cert_cn, site, port)
            result = False
        else:
            logger.info('%s: %s CN not equals to site, Details=%s:%s',
                        show_open(), cert_cn, site, port)
            result = True
    else:
        logger.info('%s: %s CN equals to site, Details=%s:%s',
                    show_close(), cert_cn, site, port)
        result = False
    return result


def is_cert_inactive(site, port=PORT):
    """Function to check whether cert is still valid."""
    result = True
    try:
        cert = ssl.get_server_certificate((site, port))
    except:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            wrapped_socket = ssl.SSLSocket(sock=sock,
                                           ca_certs=certifi.where(),
                                           cert_reqs=ssl.CERT_REQUIRED,
                                           server_hostname=site)
            wrapped_socket.connect((site, port))
            __cert = wrapped_socket.getpeercert(True)
            cert = ssl.DER_cert_to_PEM_cert(__cert)
        except socket.error:
            logger.info('%s: Port closed, Details=%s:%s',
                        show_unknown(), site, port)
            return False

    cert_obj = load_pem_x509_certificate(cert.encode('utf-8'),
                                         default_backend())

    if cert_obj.not_valid_after > datetime.datetime.now():
        logger.info('%s: Certificate is still valid, Details=Not valid \
after: %s, Current time: %s',
                    show_close(), cert_obj.not_valid_after.isoformat(),
                    datetime.datetime.now().isoformat())
        result = False
    else:
        logger.info('%s: Certificate is not valid, Details=Not valid \
after: %s, Current time: %s',
                    show_open(), cert_obj.not_valid_after.isoformat(),
                    datetime.datetime.now().isoformat())
        result = True
    return result


def is_cert_validity_lifespan_unsafe(site, port=PORT):
    """Function to check whether cert lifespan is safe."""
    max_validity_days = 365

    result = True
    try:
        cert = ssl.get_server_certificate((site, port))
    except:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            wrapped_socket = ssl.SSLSocket(sock=sock,
                                           ca_certs=certifi.where(),
                                           cert_reqs=ssl.CERT_REQUIRED,
                                           server_hostname=site)
            wrapped_socket.connect((site, port))
            __cert = wrapped_socket.getpeercert(True)
            cert = ssl.DER_cert_to_PEM_cert(__cert)
        except socket.error:
            logger.info('%s: Port closed, Details=%s:%s',
                        show_unknown(), site, port)
            return False

    cert_obj = load_pem_x509_certificate(cert.encode('utf-8'),
                                         default_backend())

    cert_validity = \
        cert_obj.not_valid_after - cert_obj.not_valid_before

    if cert_validity.days <= max_validity_days:
        logger.info('%s: Certificate has a secure lifespan, Details=Not \
valid before: %s, Not valid after: %s',
                    show_close(), cert_obj.not_valid_before.isoformat(),
                    cert_obj.not_valid_after.isoformat())
        result = False
    else:
        logger.info('%s: Certificate has an insecure lifespan, Details=Not \
valid before: %s, Not valid after: %s',
                    show_open(), cert_obj.not_valid_before.isoformat(),
                    cert_obj.not_valid_after.isoformat())
        result = True
    return result


def is_pfs_disabled(site, port=PORT):
    """Function to check whether PFS is enabled."""
    packet = '<packet>SOME_DATA</packet>'

    ciphers = 'ECDHE-RSA-AES256-GCM-SHA384:\
               ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:\
               ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:\
               ECDHE-ECDSA-AES256-SHA:DHE-DSS-AES256-GCM-SHA384:\
               DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-SHA256:\
               DHE-DSS-AES256-SHA256:DHE-RSA-AES256-SHA:\
               DHE-DSS-AES256-SHA:DHE-RSA-CAMELLIA256-SHA:\
               DHE-DSS-CAMELLIA256-SHA:ECDHE-RSA-AES128-GCM-SHA256:\
               ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:\
               ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:\
               ECDHE-ECDSA-AES128-SHA:DHE-DSS-AES128-GCM-SHA256:\
               DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-SHA256:\
               DHE-DSS-AES128-SHA256:DHE-RSA-AES128-SHA:\
               DHE-DSS-AES128-SHA:DHE-RSA-SEED-SHA:DHE-DSS-SEED-SHA:\
               DHE-RSA-CAMELLIA128-SHA:DHE-DSS-CAMELLIA128-SHA:\
               ECDHE-RSA-RC4-SHA:ECDHE-ECDSA-RC4-SHA:\
               ECDHE-RSA-DES-CBC3-SHA:ECDHE-ECDSA-DES-CBC3-SHA'

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        wrapped_socket = ssl.SSLSocket(sock, ciphers=ciphers)
        wrapped_socket.connect((site, port))
        wrapped_socket.send(packet.encode('utf-8'))
        logger.info('%s: PFS enabled on site, Details=%s:%s',
                    show_close(), site, port)
        result = False
    except ssl.SSLError:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            wrapped_socket = ssl.SSLSocket(sock=sock,
                                           ca_certs=certifi.where(),
                                           cert_reqs=ssl.CERT_REQUIRED,
                                           server_hostname=site,
                                           ciphers=ciphers)
            wrapped_socket.connect((site, port))
            wrapped_socket.send(packet.encode('utf-8'))
            logger.info('%s: PFS enabled on site, Details=%s:%s',
                        show_close(), site, port)
            result = False
        except ssl.SSLError:
            logger.info('%s: PFS not enabled on site, Details=%s:%s',
                        show_open(), site, port)
            return True

    except socket.error:
        logger.info('%s: Port is closed for PFS check, Details=%s:%s',
                    show_unknown(), site, port)
        result = False
    finally:
        wrapped_socket.close()
    return result


def is_sslv3_enabled(site, port=PORT):
    """Function to check whether SSLv3 suites are enabled."""
    result = True
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((site, port))

        tls_conn = tlslite.TLSConnection(sock)
        settings = tlslite.HandshakeSettings()

        settings.minVersion = (3, 0)
        settings.maxVersion = (3, 0)
        new_settings = settings.validate()

        tls_conn.handshakeClientCert(settings=new_settings)

        logger.info('%s: SSLv3 enabled on site, Details=%s:%s',
                    show_open(), site, port)
        result = True
    except tlslite.errors.TLSRemoteAlert:
        logger.info('%s: SSLv3 not enabled on site, Details=%s:%s',
                    show_close(), site, port)
        result = False
    except tlslite.errors.TLSAbruptCloseError:
        logger.info('%s: SSLv3 not enabled on site, Details=%s:%s',
                    show_close(), site, port)
        result = False
    except tlslite.errors.TLSLocalAlert:
        logger.info('%s: SSLv3 not enabled on site, Details=%s:%s',
                    show_close(), site, port)
        result = False
    except socket.error:
        logger.info('%s: Port is closed for SSLv3 check, Details=%s:%s',
                    show_unknown(), site, port)
        result = False
    finally:
        sock.close()
    return result


def is_tlsv1_enabled(site, port=PORT):
    """Function to check whether TLSv1 suites are enabled."""
    result = True
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((site, port))

        tls_conn = tlslite.TLSConnection(sock)
        settings = tlslite.HandshakeSettings()

        settings.minVersion = (3, 1)
        settings.maxVersion = (3, 1)
        new_settings = settings.validate()

        tls_conn.handshakeClientCert(settings=new_settings)

        logger.info('%s: TLSv1 enabled on site, Details=%s:%s',
                    show_open(), site, port)
        result = True
    except tlslite.errors.TLSRemoteAlert:
        logger.info('%s: TLSv1 not enabled on site, Details=%s:%s',
                    show_close(), site, port)
        result = False
    except tlslite.errors.TLSAbruptCloseError:
        logger.info('%s: TLSv1 not enabled on site, Details=%s:%s',
                    show_close(), site, port)
        result = False
    except tlslite.errors.TLSLocalAlert:
        logger.info('%s: TLSv1 not enabled on site, Details=%s:%s',
                    show_close(), site, port)
        result = False
    except socket.error:
        logger.info('%s: Port is closed for TLSv1 check, Details=%s:%s',
                    show_unknown(), site, port)
        result = False
    finally:
        sock.close()
    return result
