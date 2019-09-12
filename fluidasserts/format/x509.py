# -*- coding: utf-8 -*-
"""This module allows to check ``X509`` certificates' vulnerabilities."""

# standard imports
import datetime
import socket
import ssl
from typing import List

# 3rd party imports
import tlslite
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID

# local imports
from fluidasserts import Unit, DAST, MEDIUM, OPEN, CLOSED
from fluidasserts.helper.ssl import connect
from fluidasserts.helper.ssl import connect_legacy
from fluidasserts.utils.decorators import api, unknown_if

PORT = 443


@unknown_if(socket.error,
            tlslite.errors.TLSLocalAlert,
            tlslite.errors.TLSRemoteAlert)
def _uses_sign_alg(site: str, alg: str, port: int) -> tuple:
    """
    Check if the given hashing method was used in signing the site certificate.

    :param site: Address to connect to.
    :param alg: Hashing method to test.
    :param port: Port to connect to.
    """
    with connect(site, port=port) as connection:
        __cert = connection.session.serverCertChain.x509List[0].bytes
        cert = ssl.DER_cert_to_PEM_cert(__cert)

    cert_obj = load_pem_x509_certificate(cert.encode('utf-8'),
                                         default_backend())

    sign_algo: str = cert_obj.signature_hash_algorithm.name

    return _get_result_as_tuple(
        site=site,
        port=port,
        msg_open=f'Certificate has {sign_algo} as signature algorithm',
        msg_closed=f'Certificate has not {sign_algo} as signature algorithm',
        open_if=alg in sign_algo)


def _get_result_as_tuple(*,
                         site: str, port: int,
                         msg_open: str, msg_closed: str,
                         open_if: bool) -> tuple:
    """Return the tuple version of the Result object."""
    units: List[Unit] = [
        Unit(where=f'{site}:{port}',
             specific=[msg_open if open_if else msg_closed])]

    if open_if:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.error,
            tlslite.errors.TLSLocalAlert,
            tlslite.errors.TLSRemoteAlert)
def is_cert_cn_not_equal_to_site(site: str, port: int = PORT) -> tuple:
    """
    Check if certificate Common Name (CN) is different from given sitename.

    Name in certificate should be coherent with organization name, see
    `REQ. 093 <https://fluidattacks.com/web/rules/093/>`_

    :param site: Site address.
    :param port: Port to connect to.
    :returns: - ``OPEN`` if the parameter **site** does not equal the
                certificate's **Common Name** (CN).
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    with connect(site, port=port) as conn:
        __cert = conn.session.serverCertChain.x509List[0].bytes
        cert = ssl.DER_cert_to_PEM_cert(__cert)

    cert_obj = load_pem_x509_certificate(cert.encode('utf-8'),
                                         default_backend())
    cert_cn = \
        cert_obj.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[
            0].value.lower()

    wc_cert = '*.' + site.lower()

    domain = 'NONE'
    if cert_cn.startswith('*.'):
        domain = '.' + cert_cn.split('*.')[1].lower()

    return _get_result_as_tuple(
        site=site,
        port=port,
        msg_open=f'{cert_cn} CN is not equal to site {site}',
        msg_closed=f'{cert_cn} CN is equal to site {site}',
        open_if=(site.lower() != cert_cn
                 and wc_cert != cert_cn
                 and not site.endswith(domain)))


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.error,
            tlslite.errors.TLSLocalAlert,
            tlslite.errors.TLSRemoteAlert)
def is_cert_inactive(site: str, port: int = PORT) -> tuple:
    """
    Check if certificate is no longer valid.

    Fails if end of validity date obtained from certificate
    is beyond the time of execution.

    :param site: Site address.
    :param port: Port to connect to.
    :returns: - ``OPEN`` if certificate's **not valid after** date is
                less than or equal the current time.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    with connect(site, port=port) as conn:
        __cert = conn.session.serverCertChain.x509List[0].bytes
        cert = ssl.DER_cert_to_PEM_cert(__cert)

    cert_obj = load_pem_x509_certificate(cert.encode('utf-8'),
                                         default_backend())

    now = datetime.datetime.now()
    cert_time = cert_obj.not_valid_after

    now_str: str = now.isoformat()
    cert_time_str: str = cert_time.isoformat()

    return _get_result_as_tuple(
        site=site,
        port=port,
        msg_open=f'Certificate is expired {now_str} > {cert_time_str}',
        msg_closed=f'Certificate is still valid {now_str} <= {cert_time_str}',
        open_if=now > cert_time)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.error)
def is_cert_untrusted(site: str, port: int = PORT) -> tuple:
    """
    Check if certificate is trusted (signed by recognized CA).

    :param site: Site address.
    :param port: Port to connect to.
    :returns: - ``OPEN`` if certificate's is **signed** by a recognized
                **Certificate Authority**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    is_trusted: bool = False
    try:
        with connect_legacy(site, port, validate_cert=True):
            is_trusted = True
    except socket.error as exc:
        if not (exc.errno == 1 and 'verify failed' in str(exc.strerror)):
            raise exc
    return _get_result_as_tuple(
        site=site,
        port=port,
        msg_open='Cert is not trusted',
        msg_closed='Cert is trusted',
        open_if=not is_trusted)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.error,
            tlslite.errors.TLSLocalAlert,
            tlslite.errors.TLSRemoteAlert)
def is_cert_validity_lifespan_unsafe(site: str, port: int = PORT) -> tuple:
    """
    Check if certificate lifespan is larger than two years which is insecure.

    :param site: Site address.
    :param port: Port to connect to.
    :returns: - ``OPEN`` if certificate's lifespan (**not_valid_after** -
                **not_valid_before**) is more than two 730 days.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    max_validity_days = 730

    with connect(site, port=port) as conn:
        __cert = conn.session.serverCertChain.x509List[0].bytes
        cert = ssl.DER_cert_to_PEM_cert(__cert)

    cert_obj = load_pem_x509_certificate(cert.encode('utf-8'),
                                         default_backend())

    not_after = cert_obj.not_valid_after
    not_before = cert_obj.not_valid_before
    lifespan = (not_after - not_before).days

    return _get_result_as_tuple(
        site=site,
        port=port,
        msg_open=f'Certificate lifespan of {lifespan} days is insecure',
        msg_closed=f'Certificate lifespan of {lifespan} days is safe',
        open_if=lifespan > max_validity_days)


@api(risk=MEDIUM, kind=DAST)
def is_sha1_used(site: str, port: int = PORT) -> tuple:
    """
    Check if certificate was signed using the ``SHA1`` algorithm.

    Use of this algorithm is not recommended.
    See `Storing passwords safely`__.

    __ https://fluidattacks.com/web/blog/storing-password-safely/

    :param site: Site address.
    :param port: Port to connect to.
    :returns: - ``OPEN`` if certificate's signing algorithm is **SHA1**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_sign_alg(site, 'sha1', port)


@api(risk=MEDIUM, kind=DAST)
def is_md5_used(site: str, port: int = PORT) -> tuple:
    """
    Check if certificate was signed using the ``MD5`` algorithm.

    Use of this algorithm is not recommended.
    See `Storing passwords safely`__.

    __ https://fluidattacks.com/web/blog/storing-password-safely/

    :param site: Site address.
    :param port: Port to connect to.
    :returns: - ``OPEN`` if certificate's signing algorithm is **MD5**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _uses_sign_alg(site, 'md5', port)
