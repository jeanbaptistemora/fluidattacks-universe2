import contextlib
from lib_ssl.suites import (
    get_suite_by_code,
    SSLCipherSuite,
    SSLSuiteInfo,
    SSLVersionId,
)
from lib_ssl.types import (
    SSLAlert,
    SSLAlertDescription,
    SSLAlertLevel,
    SSLHandshakeRecord,
    SSLRecord,
    SSLServerHandshake,
    SSLServerResponse,
    SSLSettings,
    TLSVersionId,
)
from model.core_model import (
    LocalesEnum,
)
from os import (
    urandom,
)
import socket
import ssl
from struct import (
    unpack,
)
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


def ssl_id2tls_id(ssl_id: SSLVersionId) -> ssl.TLSVersion:
    return getattr(TLSVersionId, ssl_id.name).value


@contextlib.contextmanager
def ssl_connect(
    ssl_settings: SSLSettings,
) -> Generator[Optional[ssl.SSLSocket], None, None]:
    host: str = ssl_settings.context.host
    port: int = ssl_settings.context.port
    intention: str = ssl_settings.intention[LocalesEnum.EN]

    try:
        sock: Optional[socket.socket] = tcp_connect(host, port, intention)

        if sock is None:
            yield None
        else:
            ssl_ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)  # NOSONAR
            ssl_ctx.minimum_version = ssl_id2tls_id(ssl_settings.tls_version)
            ssl_ctx.maximum_version = ssl_id2tls_id(ssl_settings.tls_version)

            ssl_sock = ssl_ctx.wrap_socket(sock, do_handshake_on_connect=False)
            ssl_sock.do_handshake()
            yield ssl_sock

    except ssl.SSLError as error:
        log_blocking(
            "warning",
            "%s:%s occured with %s:%d while %s",
            error.library,
            error.reason,
            host,
            port,
            intention,
        )
        yield None
    finally:
        if sock is not None:
            ssl_sock.shutdown(socket.SHUT_RDWR)
            ssl_sock.close()


def num_to_bytes(num: int, n_bytes: int, encoding: str = "big") -> List[int]:
    b_num: bytes = num.to_bytes(n_bytes, encoding)
    return list(b_num)


def bytes_to_num(data: bytes, encoding: str = "big") -> int:
    return int.from_bytes(data, byteorder=encoding)


def rand_bytes(length: int) -> List[int]:
    return list(urandom(length))


def get_suites_package(suites: List[SSLSuiteInfo], n_bytes: int) -> List[int]:
    package: List[int] = []
    for suite in suites:
        if suite.code:
            first_byte, second_byte = suite.code
            package.append(first_byte)
            package.append(second_byte)
    return num_to_bytes(len(package), n_bytes) + package


def get_ec_point_formats_ext() -> List[int]:
    extension_id: List[int] = [0, 11]
    point_formats: List[int] = [0, 1, 2]

    package: List[int] = num_to_bytes(len(point_formats), 1) + point_formats
    return extension_id + num_to_bytes(len(package), 2) + package


def get_elliptic_curves_ext() -> List[int]:
    extension_id: List[int] = [0, 10]

    suites: List[SSLSuiteInfo] = [
        SSLCipherSuite.DH_RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DH_anon_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_RC4_128_MD5.value,
        SSLCipherSuite.DH_anon_EXPORT_WITH_RC4_40_MD5.value,
        SSLCipherSuite.RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5.value,
        SSLCipherSuite.RSA_WITH_IDEA_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_RC4_128_MD5.value,
        SSLCipherSuite.RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_NULL_MD5.value,
        SSLCipherSuite.RSA_WITH_NULL_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC4_40_MD5.value,
        SSLCipherSuite.DH_RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA.value,
    ]

    package: List[int] = get_suites_package(suites, n_bytes=2)
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


def get_malicious_heartbeat(v_id: SSLVersionId, n_payload: int) -> List[int]:
    content_type: List[int] = [24]
    version: List[int] = [3, v_id]

    package_type: List[int] = [1]

    package: List[int] = package_type + num_to_bytes(n_payload, 2)
    return content_type + version + num_to_bytes(len(package), 2) + package


def get_heartbeat(v_id: SSLVersionId, payload: List[int]) -> List[int]:
    content_type: List[int] = [24]
    version: List[int] = [3, v_id.value]

    package_type: List[int] = [1]
    padding: List[int] = rand_bytes(16)

    payload_length: List[int] = num_to_bytes(len(payload), 2)

    package: List[int] = package_type + payload_length + payload + padding
    return content_type + version + num_to_bytes(len(package), 2) + package


def get_client_hello_head(v_id: SSLVersionId, package: List[int]) -> List[int]:
    content_type: List[int] = [SSLRecord.HANDSHAKE.value]
    handshake: List[int] = [SSLHandshakeRecord.CLIENT_HELLO.value]
    version: List[int] = [3, v_id.value]

    header: List[int] = handshake + num_to_bytes(len(package) + 2, 3) + version
    return content_type + version + num_to_bytes(len(package) + 6, 2) + header


def get_client_hello_package(
    v_id: SSLVersionId,
    cipher_suites: List[SSLSuiteInfo],
    extensions: Optional[List[int]] = None,
) -> List[int]:
    session_id: List[int] = [0]
    no_compression: List[int] = [1, 0]

    package: List[int] = []

    if extensions is not None:
        package = num_to_bytes(len(extensions), 2) + extensions

    suites = get_suites_package(cipher_suites, n_bytes=2)
    package = rand_bytes(32) + session_id + suites + no_compression + package
    return get_client_hello_head(v_id, package) + package


def read_ssl_record(sock: socket.socket) -> Optional[Tuple[int, int, int]]:
    header = tcp_read(sock, 5)

    if header is None or len(header) < 5:
        return None

    packet_type, _, version_id, length = unpack(">BBBH", header)
    return packet_type, version_id, length


def read_handshake_header(
    sock: socket.socket,
) -> Optional[Tuple[int, int, int]]:
    header = tcp_read(sock, 6)

    if header is None or len(header) < 6:
        return None

    packet_type, b_length, _, version_id = unpack(">B3sBB", header)
    return packet_type, version_id, bytes_to_num(b_length)


def read_random_val(sock: socket.socket) -> Optional[bytes]:
    return tcp_read(sock, 32)


def read_session_id(sock: socket.socket) -> Optional[bytes]:
    if b_session_id_length := tcp_read(sock, 1):
        [session_id_length] = unpack(">B", b_session_id_length)
        return tcp_read(sock, session_id_length)
    return None


def read_cipher_suite(sock: socket.socket) -> Optional[SSLSuiteInfo]:
    if b_cipher_suite := tcp_read(sock, 2):
        first_byte, second_byte = unpack(">BB", b_cipher_suite)
        return get_suite_by_code(code=(first_byte, second_byte))
    return None


def parse_server_alert(
    sock: socket.socket, record: SSLRecord
) -> Optional[SSLAlert]:
    if record == SSLRecord.ALERT:
        data = tcp_read(sock, 2)

        if data is not None:
            level, description = unpack(">BB", data)

            return SSLAlert(
                level=SSLAlertLevel(level),
                description=SSLAlertDescription(description),
            )

    return None


def parse_server_handshake(
    sock: socket.socket, record: SSLRecord
) -> Optional[SSLServerHandshake]:
    if record == SSLRecord.HANDSHAKE:
        handshake_header = read_handshake_header(sock)

        if handshake_header is None:
            return None

        handshake_type, version_id, _ = handshake_header
        handshake_record = SSLHandshakeRecord(handshake_type)

        if handshake_record == SSLHandshakeRecord.SERVER_HELLO:
            read_random_val(sock)
            read_session_id(sock)
            return SSLServerHandshake(
                record=handshake_record,
                version_id=SSLVersionId(version_id),
                cipher_suite=read_cipher_suite(sock),
            )

    return None


def parse_server_response(sock: socket.socket) -> Optional[SSLServerResponse]:
    header = read_ssl_record(sock)

    if header is None:
        return None

    package_type, version_id, _ = header
    record: SSLRecord = SSLRecord(package_type)

    return SSLServerResponse(
        record=record,
        version_id=SSLVersionId(version_id),
        alert=parse_server_alert(sock, record),
        handshake=parse_server_handshake(sock, record),
    )
