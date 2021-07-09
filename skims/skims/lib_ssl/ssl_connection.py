import contextlib
from lib_ssl.types import (
    SSLEllipticCurves,
    SSLSettings,
    SSLSuites,
)
from os import (
    urandom,
)
from socket import (
    socket,
)
from struct import (
    unpack,
)
import tlslite
from typing import (
    Generator,
    List,
    Optional,
    Tuple,
)
from utils.logs import (
    log_blocking,
)
from utils.sockets import (
    tcp_connect,
    tcp_read,
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


def num_to_bytes(num: int, n_bytes: int, encoding: str = "big") -> List[int]:
    b_num: bytes = num.to_bytes(n_bytes, encoding)
    return list(b_num)


def rand_bytes(length: int) -> List[int]:
    return list(urandom(length))


def get_ec_point_formats_ext() -> List[int]:
    extension_id: List[int] = [0, 11]
    point_formats: List[int] = [0, 1, 2]

    package: List[int] = num_to_bytes(len(point_formats), 1) + point_formats
    return extension_id + num_to_bytes(len(package), 2) + package


def get_elliptic_curves_ext() -> List[int]:
    extension_id: List[int] = [0, 10]
    ellip_curves: List[int] = SSLEllipticCurves().get_all()

    package: List[int] = num_to_bytes(len(ellip_curves), 2) + ellip_curves
    return extension_id + num_to_bytes(len(package), 2) + package


def get_session_ticket_ext() -> List[int]:
    extension_id: List[int] = [0, 35]

    package: List[int] = []
    return extension_id + num_to_bytes(len(package), 2) + package


def get_heartbeat_ext() -> List[int]:
    extension_id: List[int] = [0, 15]
    mode: List[int] = [1]

    package: List[int] = mode
    return extension_id + num_to_bytes(len(package), 2) + package


def get_malicious_heartbeat(version_id: int, n_payload: int) -> List[int]:
    content_type: List[int] = [24]
    version: List[int] = [3, version_id]

    package_type: List[int] = [1]

    package: List[int] = package_type + num_to_bytes(n_payload, 2)
    return content_type + version + num_to_bytes(len(package), 2) + package


def get_heartbeat(version_id: int, payload: List[int]) -> List[int]:
    content_type: List[int] = [24]
    version: List[int] = [3, version_id]

    package_type: List[int] = [1]
    padding: List[int] = rand_bytes(16)

    payload_length: List[int] = num_to_bytes(len(payload), 2)

    package: List[int] = package_type + payload_length + payload + padding
    return content_type + version + num_to_bytes(len(package), 2) + package


def get_client_hello_header(version_id: int, package: List[int]) -> List[int]:
    content_type: List[int] = [22]
    handshake: List[int] = [1]
    version: List[int] = [3, version_id]

    header: List[int] = handshake + num_to_bytes(len(package) + 2, 3) + version
    return content_type + version + num_to_bytes(len(package) + 6, 2) + header


def get_client_hello_package(
    version_id: int, extensions: Optional[List[int]] = None
) -> List[int]:

    session_id: List[int] = [0]
    no_compression: List[int] = [1, 0]

    cipher_suites: List[int] = SSLSuites().get_all()
    suites: List[int] = num_to_bytes(len(cipher_suites), 2) + cipher_suites

    package: List[int] = []

    if extensions is not None:
        package = num_to_bytes(len(extensions), 2) + extensions

    package = rand_bytes(32) + session_id + suites + no_compression + package
    return get_client_hello_header(version_id, package) + package


def read_ssl_record(sock: socket) -> Optional[Tuple[int, int, int]]:
    header = tcp_read(sock, 5)

    if header is None or len(header) < 5:
        return None

    packet_type, _, version_id, length = unpack(">BBBH", header)
    return packet_type, version_id, length
