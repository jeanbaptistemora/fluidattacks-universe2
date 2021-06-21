import contextlib
import socket
import tlslite
from typing import (
    Tuple,
)


@contextlib.contextmanager
def connect(
    hostname: str,
    port: int,
    min_version: Tuple[int, int] = (3, 0),
    max_version: Tuple[int, int] = (3, 4),
) -> tlslite.TLSConnection:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))

    connection = tlslite.TLSConnection(sock)
    settings = tlslite.HandshakeSettings()

    settings.minVersion = min_version
    settings.maxVersion = max_version

    try:
        connection.handshakeClientCert(settings=settings)
        yield connection
    finally:
        connection.close()
