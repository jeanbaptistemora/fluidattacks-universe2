import contextlib
import socket
import tlslite
from typing import (
    Generator,
    Optional,
    Tuple,
)
from utils.logs import (
    log_blocking,
)


def _socket_connect(
    hostname: str,
    port: int,
) -> Optional[socket.socket]:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        return sock
    except (
        socket.error,
        socket.herror,
        socket.gaierror,
        socket.timeout,
    ) as error:
        log_blocking(
            "error",
            "%s occured with %s:%d",
            type(error).__name__,
            hostname,
            port,
        )
        return None


@contextlib.contextmanager
def connect(
    hostname: str,
    port: int,
    min_version: Tuple[int, int] = (3, 0),
    max_version: Tuple[int, int] = (3, 4),
    expected_exceptions: Tuple[tlslite.errors.BaseTLSException, ...] = (),
) -> Generator[Optional[tlslite.TLSConnection], None, None]:

    try:
        sock: Optional[socket.socket] = _socket_connect(hostname, port)
        if sock is None:
            yield None
        else:
            connection = tlslite.TLSConnection(sock)
            settings = tlslite.HandshakeSettings()

            settings.minVersion = min_version
            settings.maxVersion = max_version

            connection.handshakeClientCert(settings=settings)
            yield connection
    except tlslite.errors.BaseTLSException as error:
        if not any(
            isinstance(error, exception) for exception in expected_exceptions
        ):
            log_blocking(
                "warning",
                "%s %s occured with %s:%d",
                type(error).__name__,
                error,
                hostname,
                port,
            )
        yield None
    finally:
        if sock is not None:
            connection.close()
