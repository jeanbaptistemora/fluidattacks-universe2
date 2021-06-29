from enum import (
    Enum,
)
from lib_ssl.types import (
    SSLSettings,
)
from typing import (
    Dict,
    Tuple,
)
from utils.string import (
    make_snippet,
    SNIPPETS_COLUMNS,
    SnippetViewport,
)

ssl_versions: Dict[Tuple[int, int], str] = {
    (3, 0): "SSLv3.0",
    (3, 1): "TLSv1.0",
    (3, 2): "TLSv1.1",
    (3, 3): "TLSv1.2",
    (3, 4): "TLSv1.3",
}


class SSLSnippetLine(Enum):
    min_version: int = 2
    max_version: int = 3
    ciphers: int = 4
    mac: int = 5
    key_exchange: int = 6


# pylint: disable=too-many-arguments
def snippet(
    host: str,
    port: int,
    conn_established: bool,
    line: SSLSnippetLine,
    ssl_settings: SSLSettings,
    columns_per_line: int = SNIPPETS_COLUMNS,
) -> str:

    min_version: str = ssl_versions[ssl_settings.min_version]
    max_version: str = ssl_versions[ssl_settings.max_version]
    chiphers: str = ", ".join(ssl_settings.cipher_names)
    mac: str = ", ".join(ssl_settings.mac_names)
    key_exchange: str = ", ".join(ssl_settings.key_exchange_names)

    content: str = f"SSL connection request to {host}:{port}\n"
    content += f"min version: {min_version}\n"
    content += f"max version: {max_version}\n"
    content += f"chiphers: {chiphers}\n"
    content += f"mac: {mac}\n"
    content += f"key exchange: {key_exchange}\n"
    content += f"connection established: {conn_established}\n"

    return make_snippet(
        content=content,
        viewport=SnippetViewport(
            columns_per_line=columns_per_line,
            column=0,
            line=line.value,
            wrap=True,
        ),
    )
