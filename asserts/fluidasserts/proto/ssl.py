# -*- coding: utf-8 -*-

"""
This module allows to check SSL vulnerabilities.

Heartbleed code inspired from original PoC by
Jared Stafford (jspenguin@jspenguin.org)
"""

# pylint: disable=too-many-lines

from __future__ import (
    absolute_import,
)

from contextlib import (
    suppress,
)
import copy
from fluidasserts import (
    CLOSED,
    DAST,
    HIGH,
    LOW,
    MEDIUM,
    OPEN,
    Unit,
    UNKNOWN,
)
from fluidasserts.helper import (
    http,
)
from fluidasserts.helper.ssl import (
    connect,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
import socket
import struct
import tlslite
from typing import (
    List,
    Optional,
    Tuple,
)

PORT = 443
TYPRECEIVE = Tuple[Optional[str], Optional[int], Optional[int]]


# pylint: disable=protected-access


def _my_send_finished(
    self, master_secret, cipher_suite=None, next_proto=None, settings=None
):
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
        self._recv_record_limit = min(2 ** 14, settings.record_size_limit)

    if next_proto is not None:
        next_proto_msg = tlslite.messages.NextProtocol().create(next_proto)
        for result in self._sendMsg(next_proto_msg):
            yield result

    # Calculate verification data
    verify_data = tlslite.mathtls.calcFinished(
        self.version,
        master_secret,
        cipher_suite,
        self._handshake_hash,
        self._client,
    )
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


def _get_result_as_tuple(
    *, site: str, port: int, msg_open: str, msg_closed: str, open_if: bool
) -> tuple:
    """Return the tuple version of the Result object."""
    units: List[Unit] = [
        Unit(
            where=f"{site}@{port}",
            specific=[msg_open if open_if else msg_closed],
        )
    ]

    if open_if:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@api(risk=HIGH, kind=DAST)
@unknown_if(socket.error, tlslite.errors.TLSLocalAlert)
def has_poodle_tls(site: str, port: int = PORT) -> tuple:
    """
    Check if POODLE TLS is present.

    See our `blog entry on POODLE
    <https://fluidattacks.com/blog/treacherous-poodle/>`_.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    :returns: - ``OPEN`` if the server is vulnerable to POODLE TLS Attack.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    is_vulnerable: bool = False
    with suppress(
        tlslite.errors.TLSRemoteAlert, tlslite.errors.TLSAbruptCloseError
    ):
        with connect(
            site,
            port=port,
            check="POODLE",
            cipher_names=["aes256", "aes128", "3des"],
            min_version=(3, 1),
        ):
            is_vulnerable = True

    return _get_result_as_tuple(
        site=site,
        port=port,
        msg_open="Site is vulnerable to POODLE TLS attack",
        msg_closed="Site is not vulnerable to POODLE TLS attack",
        open_if=is_vulnerable,
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(socket.error, tlslite.errors.TLSLocalAlert)
def has_poodle_sslv3(site: str, port: int = PORT) -> tuple:
    """
    Check if POODLE SSLv3 is present.

    See our `blog entry on POODLE
    <https://fluidattacks.com/blog/treacherous-poodle/>`_.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    :returns: - ``OPEN`` if the server is vulnerable to POODLE SSL v3 Attack.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    is_vulnerable: bool = False
    with suppress(
        tlslite.errors.TLSRemoteAlert, tlslite.errors.TLSAbruptCloseError
    ):
        with connect(
            site,
            port=port,
            check="POODLE",
            min_version=(3, 0),
            max_version=(3, 0),
            cipher_names=["aes256", "aes128", "3des"],
        ):
            is_vulnerable = True

    return _get_result_as_tuple(
        site=site,
        port=port,
        msg_open="Site is vulnerable to POODLE SSLv3 attack",
        msg_closed="Site is not vulnerable to POODLE SSLv3 attack",
        open_if=is_vulnerable,
    )


@api(risk=HIGH, kind=DAST)
def allows_modified_mac(site: str, port: int = PORT) -> tuple:
    """
    Check if site allows messages with modified MAC.

    :param site: Address to connect to.
    :param port: If necessary, specify port to connect to.
    :returns: - ``OPEN`` if the server accepts a socket with a modified MAC.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    is_vulnerable: bool = False
    orig_method = copy.deepcopy(
        tlslite.tlsconnection.TLSConnection._sendFinished
    )
    tlslite.tlsconnection.TLSConnection._sendFinished = _my_send_finished
    failed_bits = list()
    for mask_bit in range(0, 96):
        mask = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        mask_index = int((mask_bit - (mask_bit % 8)) / 8)
        mask[mask_index] = 0x80 >> (mask_bit % 8)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((site, port))
            tls = tlslite.TLSConnection(sock)
            tls.macTweak = bytearray(mask)
            tls.handshakeClientCert()
            tls.send(b"GET / HTTP/1.0\n\n\n")
            tls.read()
        except (
            tlslite.TLSRemoteAlert,
            tlslite.TLSAbruptCloseError,
            tlslite.errors.TLSLocalAlert,
            socket.error,
        ):
            continue
        else:
            failed_bits.append(mask_bit)
            is_vulnerable = True

    tlslite.tlsconnection.TLSConnection._sendFinished = orig_method

    return _get_result_as_tuple(
        site=site,
        port=port,
        msg_open="Server allows messages with modified MAC",
        msg_closed="Server rejects messages with modified MAC",
        open_if=is_vulnerable,
    )
