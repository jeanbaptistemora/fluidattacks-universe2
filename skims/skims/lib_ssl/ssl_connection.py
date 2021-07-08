import contextlib
from lib_ssl.types import (
    SSLSettings,
)
from socket import (
    socket,
)
import tlslite
from typing import (
    Generator,
    Optional,
    Tuple,
)
from utils.logs import (
    log_blocking,
)
from utils.sockets import (
    tcp_connect,
)


@contextlib.contextmanager
def connect(
    ssl_settings: SSLSettings,
    expected_exceptions: Tuple[tlslite.errors.BaseTLSException, ...] = (),
) -> Generator[Optional[tlslite.TLSConnection], None, None]:

    try:
        sock: Optional[socket] = tcp_connect(
            ssl_settings.host, ssl_settings.port, ssl_settings.intention
        )

        if sock is None:
            yield None
        else:
            connection = tlslite.TLSConnection(sock)

            settings = tlslite.HandshakeSettings()
            settings.sendFallbackSCSV = ssl_settings.scsv
            settings.minVersion = ssl_settings.min_version
            settings.maxVersion = ssl_settings.max_version
            settings.macNames = ssl_settings.mac_names
            settings.cipherNames = ssl_settings.cipher_names
            settings.keyExchangeNames = ssl_settings.key_exchange_names

            if ssl_settings.anonymous:
                connection.handshakeClientAnonymous(settings=settings)
            else:
                connection.handshakeClientCert(settings=settings)

            yield connection

    except tlslite.errors.BaseTLSException as error:
        if isinstance(error, expected_exceptions):
            yield connection
        else:
            log_blocking(
                "error",
                "%s %s occured with %s:%d while %s",
                type(error).__name__,
                error,
                ssl_settings.host,
                ssl_settings.port,
                ssl_settings.intention,
            )
            yield None
    finally:
        if sock is not None:
            connection.close()
