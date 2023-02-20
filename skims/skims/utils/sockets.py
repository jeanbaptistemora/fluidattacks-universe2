import socket
from utils.logs import (
    log_blocking,
)


def tcp_connect(
    hostname: str,
    port: int,
    intention: str = "establish tcp connection",
) -> socket.socket | None:
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
            "%s occured with %s:%d while %s",
            type(error).__name__,
            hostname,
            port,
            intention,
        )
        return None


def tcp_read(sock: socket.socket, size: int) -> bytes | None:
    try:
        return sock.recv(size)
    except (
        socket.error,
        socket.herror,
        socket.gaierror,
        socket.timeout,
    ) as error:
        log_blocking(
            "error",
            "%s occured reading socket",
            type(error).__name__,
        )
        return None
