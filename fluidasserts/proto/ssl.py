# -*- coding: utf-8 -*-

"""
This modulle allows to check SSL vulnerabilities.

Heartbleed code inspired from original PoC by
Jared Stafford (jspenguin@jspenguin.org)
"""

# standard imports
from __future__ import absolute_import
import copy
import socket
import struct
from typing import Tuple, Optional, List
from contextlib import suppress

# 3rd party imports
import tlslite

# local imports
from fluidasserts import DAST, LOW, OPEN, CLOSED, Unit
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import http
from fluidasserts.helper.ssl import connect
from fluidasserts.utils.decorators import track, level, notify, api, unknown_if

PORT = 443
TYPRECEIVE = Tuple[Optional[str], Optional[int], Optional[int]]

# pylint: disable=protected-access


def _my_send_finished(self, master_secret, cipher_suite=None, next_proto=None,
                      settings=None):
    """Duck-tapped TLSConnection._sendFinished function."""
    self.sock.buffer_writes = True
    # Send ChangeCipherSpec
    for result in self._sendMsg(tlslite.messages.ChangeCipherSpec()):
        yield result

    # Switch to pending write state
    self._changeWriteState()

    if self._peer_record_size_limit:
        self._send_record_limit = self._peer_record_size_limit
        # this is TLS 1.2 and earlier method, so the real limit may be
        # lower that what's in the settings
        self._recv_record_limit = min(2**14, settings.record_size_limit)

    if next_proto is not None:
        next_proto_msg = tlslite.messages.NextProtocol().create(next_proto)
        for result in self._sendMsg(next_proto_msg):
            yield result

    # Calculate verification data
    verify_data = tlslite.mathtls.calcFinished(self.version,
                                               master_secret,
                                               cipher_suite,
                                               self._handshake_hash,
                                               self._client)
    if self.fault == tlslite.constants.Fault.badFinished:
        verify_data[0] = (verify_data[0] + 1) % 256

    if self.macTweak:
        tweak_len = min(len(verify_data), len(self.macTweak))
        for i in range(0, tweak_len):
            verify_data[i] ^= self.macTweak[i]

    # Send Finished message under new state
    finished = tlslite.messages.Finished(self.version).create(verify_data)
    for result in self._sendMsg(finished):
        yield result
    self.sock.flush()
    self.sock.buffer_writes = False


def _rcv_tls_record(sock: socket.socket) -> TYPRECEIVE:
    """
    Receive TLS record.

    :param sock: Socket to connect to.
    :return: A triplet containing type, version and received message,
             or (None, None, None) if something went wrong during connection.
    """
    try:
        tls_header = sock.recv(5)
        if not tls_header:
            return None, None, None
        if len(tls_header) < 5:
            return None, None, None
        typ, ver, length = struct.unpack('>BHH', tls_header)
        if typ > 24:
            return None, None, None
        message = ''
        while len(message) != length:
            message += sock.recv(length - len(message)).decode('ISO-8859-1')
        if not message:
            return None, None, None
        return typ, ver, message
    except socket.error:
        return None, None, None


def _build_client_hello(tls_ver: str) -> List:
    """
    Build CLIENTHELLO TLS message.

    :param tls_ver: TLS version.
    :return: A List with the corresponding hex codes.
    """
    ssl_version_mapping = {
        'SSLv3':   0x00,
        'TLSv1.0': 0x01,
        'TLSv1.1': 0x02,
        'TLSv1.2': 0x03
    }
    client_hello = [
        # TLS header ( 5 bytes)
        0x16,               # Content type (0x16 for handshake)
        0x03, ssl_version_mapping[tls_ver],         # TLS Version
        0x00, 0xdc,         # Length
        # Handshake header
        0x01,               # Type (0x01 for ClientHello)
        0x00, 0x00, 0xd8,   # Length
        0x03, ssl_version_mapping[tls_ver],         # TLS Version
        # Random (32 byte)
        0x53, 0x43, 0x5b, 0x90, 0x9d, 0x9b, 0x72, 0x0b,
        0xbc, 0x0c, 0xbc, 0x2b, 0x92, 0xa8, 0x48, 0x97,
        0xcf, 0xbd, 0x39, 0x04, 0xcc, 0x16, 0x0a, 0x85,
        0x03, 0x90, 0x9f, 0x77, 0x04, 0x33, 0xd4, 0xde,
        0x00,               # Session ID length
        0x00, 0x66,         # Cipher suites length
        # Cipher suites (51 suites)
        0xc0, 0x14, 0xc0, 0x0a, 0xc0, 0x22, 0xc0, 0x21,
        0x00, 0x39, 0x00, 0x38, 0x00, 0x88, 0x00, 0x87,
        0xc0, 0x0f, 0xc0, 0x05, 0x00, 0x35, 0x00, 0x84,
        0xc0, 0x12, 0xc0, 0x08, 0xc0, 0x1c, 0xc0, 0x1b,
        0x00, 0x16, 0x00, 0x13, 0xc0, 0x0d, 0xc0, 0x03,
        0x00, 0x0a, 0xc0, 0x13, 0xc0, 0x09, 0xc0, 0x1f,
        0xc0, 0x1e, 0x00, 0x33, 0x00, 0x32, 0x00, 0x9a,
        0x00, 0x99, 0x00, 0x45, 0x00, 0x44, 0xc0, 0x0e,
        0xc0, 0x04, 0x00, 0x2f, 0x00, 0x96, 0x00, 0x41,
        0xc0, 0x11, 0xc0, 0x07, 0xc0, 0x0c, 0xc0, 0x02,
        0x00, 0x05, 0x00, 0x04, 0x00, 0x15, 0x00, 0x12,
        0x00, 0x09, 0x00, 0x14, 0x00, 0x11, 0x00, 0x08,
        0x00, 0x06, 0x00, 0x03, 0x00, 0xff,
        0x01,               # Compression methods length
        0x00,               # Compression method (0x00 for NULL)
        0x00, 0x49,         # Extensions length
        # Extension: ec_point_formats
        0x00, 0x0b, 0x00, 0x04, 0x03, 0x00, 0x01, 0x02,
        # Extension: elliptic_curves
        0x00, 0x0a, 0x00, 0x34, 0x00, 0x32, 0x00, 0x0e,
        0x00, 0x0d, 0x00, 0x19, 0x00, 0x0b, 0x00, 0x0c,
        0x00, 0x18, 0x00, 0x09, 0x00, 0x0a, 0x00, 0x16,
        0x00, 0x17, 0x00, 0x08, 0x00, 0x06, 0x00, 0x07,
        0x00, 0x14, 0x00, 0x15, 0x00, 0x04, 0x00, 0x05,
        0x00, 0x12, 0x00, 0x13, 0x00, 0x01, 0x00, 0x02,
        0x00, 0x03, 0x00, 0x0f, 0x00, 0x10, 0x00, 0x11,
        # Extension: SessionTicket TLS
        0x00, 0x23, 0x00, 0x00,
        # Extension: Heartbeat
        0x00, 0x0f, 0x00, 0x01, 0x01]
    return client_hello


def _build_heartbeat(tls_ver: str) -> List:
    """
    Build heartbeat message according to TLS version.

    :param tls_ver: TLS version.
    :return: A List with the corresponding hex codes.
    """
    ssl_version_mapping = {
        'SSLv3':   0x00,
        'TLSv1.0': 0x01,
        'TLSv1.1': 0x02,
        'TLSv1.2': 0x03
    }

    heartbeat = [
        0x18,       # Content Type (Heartbeat)
        0x03, ssl_version_mapping[tls_ver],  # TLS version
        0x00, 0x03,  # Length
        # Payload
        0x01,       # Type (Request)
        0x40, 0x00  # Payload length
    ]
    return heartbeat


@notify
@level('medium')
@track
def is_pfs_disabled(site: str, port: int = PORT) -> bool:
    """
    Check if PFS is enabled.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    try:
        with connect(site, port=port,
                     key_exchange_names=['dhe_rsa', 'ecdhe_rsa',
                                         'ecdh_anon', 'dh_anon']):
            show_close('Forward Secrecy enabled on site',
                       details=dict(site=site, port=port))
            result = False
    except (tlslite.errors.TLSRemoteAlert,
            tlslite.errors.TLSAbruptCloseError):
        show_open('Forward Secrecy not enabled on site',
                  details=dict(site=site, port=port))
        return True
    except (tlslite.errors.TLSLocalAlert, socket.error) as exc:
        show_unknown('Could not connect',
                     details=dict(site=site, port=port, error=str(exc)))
        result = False
    return result


@notify
@level('high')
@track
def is_sslv3_enabled(site: str, port: int = PORT) -> bool:
    """
    Check if SSLv3 suites are enabled.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    result = True
    try:
        with connect(site, port=port, min_version=(3, 0), max_version=(3, 0)):
            show_open('SSLv3 enabled on site',
                      details=dict(site=site, port=port))
            result = True
    except (tlslite.errors.TLSRemoteAlert, tlslite.errors.TLSAbruptCloseError):
        show_close('SSLv3 not enabled on site',
                   details=dict(site=site, port=port))
        result = False
    except (tlslite.errors.TLSLocalAlert):
        show_unknown('Port doesn\'t support SSL',
                     details=dict(site=site, port=port))
        result = False
    except socket.error as exc:
        result = False
        show_unknown('Could not connect',
                     details=dict(site=site, port=port, error=str(exc)))
    return result


@notify
@level('medium')
@track
def is_tlsv1_enabled(site: str, port: int = PORT) -> bool:
    """
    Check if TLSv1 suites are enabled.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    result = True
    try:
        with connect(site, port=port, min_version=(3, 1), max_version=(3, 1)):
            show_open('TLSv1 enabled on site',
                      details=dict(site=site, port=port))
            result = True
    except (tlslite.errors.TLSRemoteAlert, tlslite.errors.TLSAbruptCloseError):
        show_close('TLSv1 not enabled on site',
                   details=dict(site=site, port=port))
        result = False
    except (tlslite.errors.TLSLocalAlert):
        show_unknown('Port doesn\'t support SSL',
                     details=dict(site=site, port=port))
        result = False
    except socket.error as exc:
        result = False
        show_unknown('Could not connect',
                     details=dict(site=site, port=port, error=str(exc)))
    return result


@api(risk=LOW, kind=DAST)
@unknown_if(socket.error, tlslite.errors.TLSLocalAlert)
def is_tlsv11_enabled(site: str, port: int = PORT) -> tuple:
    """
    Check if TLSv1.1 suites are enabled.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    :returns: - ``OPEN`` if **TLS v1.1** is enabled on site.
              - ``UNKNOWN`` on errors,
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    is_enabled: bool = False

    with suppress(tlslite.errors.TLSRemoteAlert,
                  tlslite.errors.TLSAbruptCloseError):
        with connect(site, port=port, min_version=(3, 2), max_version=(3, 2)):
            is_enabled = True

    msg_open: str = 'TLS v1.1 is enabled'
    msg_closed: str = 'TLS v1.1 is disabled'

    units: List[Unit] = [
        Unit(where=f'{site}@{port}',
             specific=[msg_open if is_enabled else msg_closed])]

    if is_enabled:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@notify
@level('high')
@track
def has_poodle_tls(site: str, port: int = PORT) -> bool:
    """
    Check if POODLE TLS is present.

    See our `blog entry on POODLE
    <https://fluidattacks.com/web/blog/treacherous-poodle/>`_.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    result = False
    try:
        with connect(site, port=port, check='POODLE',
                     cipher_names=["aes256", "aes128", "3des"],
                     min_version=(3, 1)):
            show_open('Site vulnerable to POODLE TLS attack',
                      details=dict(site=site, port=port))
            result = True
    except (tlslite.errors.TLSRemoteAlert,
            tlslite.errors.TLSAbruptCloseError):
        show_close('Site not vulnerable to POODLE TLS attack',
                   details=dict(site=site, port=port))
        result = False
    except (tlslite.errors.TLSLocalAlert):
        show_unknown('Port doesn\'t support SSL',
                     details=dict(site=site, port=port))
        result = False
    except socket.error as exc:
        result = False
        show_unknown('Could not connect',
                     details=dict(site=site, port=port, error=str(exc)))
    return result


@notify
@level('high')
@track
def has_poodle_sslv3(site: str, port: int = PORT) -> bool:
    """
    Check if POODLE SSLv3 is present.

    See our `blog entry on POODLE
    <https://fluidattacks.com/web/blog/treacherous-poodle/>`_.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    result = False
    try:
        with connect(site, port=port, min_version=(3, 0),
                     cipher_names=["aes256", "aes128", "3des"],
                     max_version=(3, 0), check='POODLE'):
            show_open('Site vulnerable to POODLE SSLv3 attack',
                      details=dict(site=site, port=port))
            return True
    except (tlslite.errors.TLSRemoteAlert, tlslite.errors.TLSAbruptCloseError):
        show_close('Site not vulnerable to POODLE SSLv3 attack',
                   details=dict(site=site, port=port))
        result = False
    except (tlslite.errors.TLSLocalAlert):
        show_unknown('Port doesn\'t support SSL',
                     details=dict(site=site, port=port))
        result = False
    except socket.error as exc:
        result = False
        show_unknown('Could not connect',
                     details=dict(site=site, port=port, error=str(exc)))
    return result


@api(risk=LOW, kind=DAST)
@unknown_if(http.ConnError)
def has_breach(site: str, port: int = PORT) -> tuple:
    """
    Check if BREACH category of vulnerabilities is present.

    Remember that to be vulnerable, a web application must:

    - Be served from a server that uses HTTP-level compression.
    - Reflect user-input in HTTP response bodies.
    - Reflect a secret (such as a CSRF token) in HTTP response bodies.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    :returns: - ``OPEN`` if the page is served with HTTP compression enabled,
                requirements two and three are up to the human to be verified.
              - ``UNKNOWN`` on errors,
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    common_compressors = ['compress', 'exi', 'gzip',
                          'identity', 'pack200-gzip', 'br', 'bzip2',
                          'lzma', 'peerdist', 'sdch', 'xpress', 'xz']

    session = http.HTTPSession(
        url=f'https://{site}:{port}',
        request_at_instantiation=False)
    session._set_messages(
        source='HTTP/Request/Headers/Content-Encoding',
        msg_open='Site is vulnerable to BREACH attack',
        msg_closed='Site is not vulnerable to BREACH attack')

    for compression in common_compressors:
        session.headers = {'Accept-Encoding': f'{compression},deflate'}
        session.do_request()
        content_encoding = session.response.headers.get('Content-Encoding', '')
        session._add_unit(
            is_vulnerable=compression in content_encoding)

    return session._get_tuple_result()


@notify
@level('high')
@track
def allows_anon_ciphers(site: str, port: int = PORT) -> bool:
    """
    Check if site accepts anonymous cipher suites.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    result = True
    try:
        with connect(site, port=port, anon=True):
            show_open('Site allows anonymous cipher suites',
                      details=dict(site=site, port=port))
            result = True
    except (tlslite.errors.TLSRemoteAlert, tlslite.errors.TLSAbruptCloseError):
        show_close('Site not allows anonymous cipher suites',
                   details=dict(site=site, port=port))
        result = False
    except (tlslite.errors.TLSLocalAlert):
        show_unknown('Port doesn\'t support SSL',
                     details=dict(site=site, port=port))
        result = False
    except socket.error as exc:
        result = False
        show_unknown('Could not connect',
                     details=dict(site=site, port=port, error=str(exc)))
    return result


@notify
@level('high')
@track
def allows_weak_ciphers(site: str, port: int = PORT) -> bool:
    """
    Check if site accepts weak cipher suites.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    result = True
    try:
        with connect(site, port=port,
                     cipher_names=['rc4', '3des', 'null']):
            show_open('Site allows weak (RC4, 3DES and NULL) cipher \
suites', details=dict(site=site, port=port))
            result = True
    except (tlslite.errors.TLSRemoteAlert, tlslite.errors.TLSAbruptCloseError):
        show_close('Site not allows weak (RC4, 3DES and NULL) cipher \
suites', details=dict(site=site, port=port))
        result = False
    except (tlslite.errors.TLSLocalAlert):
        show_unknown('Port doesn\'t support SSL',
                     details=dict(site=site, port=port))
        result = False
    except socket.error as exc:
        result = False
        show_unknown('Could not connect',
                     details=dict(site=site, port=port, error=str(exc)))
    return result


@api(risk=LOW, kind=DAST)
@unknown_if(socket.error, tlslite.errors.TLSLocalAlert)
def has_beast(site: str, port: int = PORT) -> tuple:
    """
    Check if site allows BEAST attack.

    See our `blog entry on BEAST
    <https://fluidattacks.com/web/blog/release-the-beast/>`_.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    :returns: - ``OPEN`` if **CBC** mode is used together with **SSL**.
              - ``UNKNOWN`` on errors,
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    is_vulnerable: bool = False
    with suppress(tlslite.errors.TLSRemoteAlert,
                  tlslite.errors.TLSAbruptCloseError):
        with connect(site, port=port,
                     min_version=(3, 1), max_version=(3, 1)) as connection:
            if connection._recordLayer.isCBCMode():
                is_vulnerable = True

    msg_open: str = 'BEAST attack is possible'
    msg_closed: str = 'BEAST attack is not possible'

    units: List[Unit] = [
        Unit(where=f'{site}@{port}',
             specific=[msg_open if is_vulnerable else msg_closed])]

    if is_vulnerable:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@notify
@level('high')
@track
def has_heartbleed(site: str, port: int = PORT) -> bool:
    """
    Check if site allows Heartbleed attack.

    See our `blog entry on Heartbleed
    <https://fluidattacks.com/web/blog/my-heart-bleeds/>`_.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    # pylint: disable=too-many-nested-blocks
    try:
        versions = ['TLSv1.2', 'TLSv1.1', 'TLSv1.0', 'SSLv3']
        for vers in versions:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((site, port))
            sock.send(bytes(_build_client_hello(vers)))
            typ, _, _ = _rcv_tls_record(sock)
            if not typ:
                continue
            if typ == 22:
                # Received Server Hello
                sock.send(bytes(_build_heartbeat(vers)))
                while True:
                    typ, _, pay = _rcv_tls_record(sock)
                    if typ == 21 or typ is None:
                        break
                    if typ == 24:
                        # Received hearbeat response
                        if len(pay) > 3:
                            # Length is higher than sent
                            show_open('Site vulnerable to Heartbleed \
attack ({})'.format(vers), details=dict(site=site, port=port))
                            return True
            sock.close()
        show_close("Site doesn't support SSL/TLS heartbeats",
                   details=dict(site=site, port=port))
        return False
    except socket.error as exc:
        show_unknown('Could not connect',
                     details=dict(site=site, port=port, error=str(exc)))
        result = False
    return result


@notify
@level('high')
@track
def allows_modified_mac(site: str, port: int = PORT) -> bool:
    """
    Check if site allows messages with modified MAC.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    orig_method = \
        copy.deepcopy(tlslite.tlsconnection.TLSConnection._sendFinished)
    tlslite.tlsconnection.TLSConnection._sendFinished = _my_send_finished
    result = False
    failed_bits = list()
    for mask_bit in range(0, 96):
        mask = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        mask_index = int((mask_bit - (mask_bit % 8)) / 8)
        mask[mask_index] = (0x80 >> (mask_bit % 8))
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((site, port))
            tls = tlslite.TLSConnection(sock)
            tls.macTweak = bytearray(mask)
            tls.handshakeClientCert()
            tls.send(b"GET / HTTP/1.0\n\n\n")
            tls.read()
        except (tlslite.TLSRemoteAlert, tlslite.TLSAbruptCloseError,
                tlslite.errors.TLSLocalAlert, socket.error):
            continue
        else:
            result = True
            failed_bits.append(mask_bit)

    tlslite.tlsconnection.TLSConnection._sendFinished = orig_method

    if result:
        show_open('Server allowed messages with modified MAC',
                  details=dict(server=site, port=port,
                               failed_bits=", ".join([str(x)
                                                     for x in failed_bits])))
    else:
        show_close('Server rejected messages with modified MAC',
                   details=dict(server=site, port=port))
    return result


@notify
@level('medium')
@track
def not_tls13_enabled(site: str, port: int = PORT) -> bool:
    """
    Check if site has TLSv1.3 enabled.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    result = True
    try:
        with connect(site, port=port, min_version=(3, 4), max_version=(3, 4)):
            show_close('Site supports TLSv1.3',
                       details=dict(site=site, port=port))
            result = False
    except (tlslite.errors.TLSLocalAlert) as exc:
        if exc.message and 'Too old version' in exc.message:
            show_open('Site does not support TLSv1.3',
                      details=dict(site=site, port=port))
            return True
        show_unknown('Port doesn\'t support SSL',
                     details=dict(site=site, port=port))
        return False
    except socket.error as exc:
        result = False
        show_unknown('Could not connect',
                     details=dict(site=site, port=port, error=str(exc)))
    return result


@notify
@level('medium')
@track
def allows_insecure_downgrade(site: str, port: int = PORT) -> bool:
    """
    Check if site has support for TLS_FALLBACK_SCSV extension.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    supported = []
    for version in reversed(range(0, 5)):
        try:
            with connect(site, port=port, max_version=(3, version)):
                supported.append(version)
        except (tlslite.errors.TLSRemoteAlert, OSError):
            continue
        except tlslite.errors.TLSLocalAlert:
            show_unknown('Port does not support SSL/TLS',
                         details=dict(site=site, port=port))
            return False
    if not supported:
        show_unknown('Could not connect to server',
                     details=dict(site=site, port=port))
        return False

    result = True

    if len(supported) > 1 and any(x in (0, 1, 2) for x in supported):
        try:
            with connect(site, port=port, max_version=(3, min(supported)),
                         scsv=True):
                show_open('Site does not support TLS_FALLBACK_SCSV',
                          details=dict(site=site, port=port))
                result = True
        except tlslite.errors.TLSRemoteAlert as exc:
            if str(exc) in ('inappropriate_fallback', 'close_notify'):
                show_close('Site supports TLS_FALLBACK_SCSV',
                           details=dict(site=site, port=port))
            else:
                show_unknown('Could not connect to server',
                             details=dict(site=site, port=port,
                                          error=str(exc).replace(':', ',')))
            result = False
    else:
        show_close('Host does not support multiple TLS versions',
                   details=dict(site=site, port=port))
        result = False
    return result


@notify
@level('medium')
@track
def tls_uses_cbc(site: str, port: int = PORT) -> bool:
    """
    Check if TLS connection uses CBC.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    result = False
    try:
        with connect(site, port=port,
                     min_version=(3, 1),
                     max_version=(3, 3)) as conn:
            if conn._recordLayer.isCBCMode():  # noqa
                show_open('Site uses TLS CBC ciphers and may be vulnerable to \
to GOLDENDOODLE and Zombie POODLE attacks',
                          details=dict(site=site, port=port))
                result = True
            else:
                show_close('Site does not use TLS CBC ciphers',
                           details=dict(site=site, port=port))
                result = False
    except (tlslite.errors.TLSRemoteAlert,
            tlslite.errors.TLSAbruptCloseError, socket.error) as exc:
        result = False
        show_unknown('Could not connect',
                     details=dict(site=site, port=port, error=str(exc)))
    except (tlslite.errors.TLSLocalAlert):
        show_unknown('Port doesn\'t support SSL',
                     details=dict(site=site, port=port))
        result = False
    return result


@api(risk=LOW, kind=DAST)
@unknown_if(tlslite.errors.TLSLocalAlert)
def has_sweet32(site: str, port: int = PORT) -> tuple:
    """
    Check if server is vulnerable to **SWEET32**.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    :returns: - ``OPEN`` if server supports **Triple DES ciphers**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    is_vulnerable: bool = False
    with suppress(socket.error,
                  tlslite.errors.TLSRemoteAlert,
                  tlslite.errors.TLSAbruptCloseError):
        with connect(site, port=port,
                     cipher_names=["3des"],
                     min_version=(3, 1), max_version=(3, 3)):
            is_vulnerable = True

    msg_open: str = 'SWEET32 attack is possible'
    msg_closed: str = 'SWEET32 attack is not possible'

    units: List[Unit] = [
        Unit(where=f'{site}@{port}',
             specific=[msg_open if is_vulnerable else msg_closed])]

    if is_vulnerable:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@notify
@level('medium')
@track
def has_tls13_downgrade_vuln(site: str, port: int = PORT) -> bool:
    """
    Check if server is prone to TLSv1.3 downgrade attack.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    """
    supported = []
    for version in reversed(range(0, 5)):
        try:
            with connect(site, port=port,
                         min_version=(3, version),
                         max_version=(3, version)):
                supported.append(version)
        except (tlslite.errors.TLSRemoteAlert, tlslite.errors.TLSLocalAlert,
                OSError):
            continue
    if not supported:
        show_unknown('Could not connect to server',
                     details=dict(site=site, port=port))
        return False

    if 4 not in supported:
        show_unknown('Site does not support TLSv1.3',
                     details=dict(site=site, port=port))
        return False
    if len(supported) > 1:
        try:
            with connect(site, port=port, min_version=(3, min(supported)),
                         max_version=(3, min(supported)),
                         key_exchange_names=['rsa']):
                show_open('Site supports TLSv1.3 and older versions and \
supports RSA keys without (EC)DH(E) cipher suites',
                          details=dict(site=site, port=port,
                                       supported=supported))
                result = True
        except (tlslite.errors.TLSRemoteAlert,
                tlslite.errors.TLSAbruptCloseError):
            show_close('Site supports TLSv1.3 older versions but \
RSA keys require (EC)DH(E) cipher suites',
                       details=dict(site=site, port=port,
                                    supported=supported))
            result = False
        except (tlslite.errors.TLSLocalAlert, socket.error) as exc:
            show_unknown('Could not connect',
                         details=dict(site=site, port=port, error=str(exc)))
            result = False
    else:
        show_close('Site not vulnerable to TLSv1.3 downgrade attack',
                   details=dict(site=site, port=port,
                                supported=supported))
        result = False
    return result
