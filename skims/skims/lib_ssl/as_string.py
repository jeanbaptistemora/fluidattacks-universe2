from lib_ssl.types import (
    SSLVulnerability,
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


def snippet(
    ssl_vulnerability: SSLVulnerability,
    columns_per_line: int = SNIPPETS_COLUMNS,
) -> str:
    ssl_settings = ssl_vulnerability.ssl_settings

    host: str = ssl_settings.host
    port: int = ssl_settings.port
    min_version: str = ssl_versions[ssl_settings.min_version]
    max_version: str = ssl_versions[ssl_settings.max_version]
    ciphers: str = ", ".join(ssl_settings.cipher_names)
    mac: str = ", ".join(ssl_settings.mac_names)
    key_exchange: str = ", ".join(ssl_settings.get_key_exchange_names())

    content: str = f"intention: {ssl_settings.intention}\n"
    content += f"SSL request made to {host}:{port} with following parameters\n"
    content += f"   fallback scsv: {ssl_settings.scsv}\n"
    content += f"   min version: {min_version}\n"
    content += f"   max version: {max_version}\n"
    content += f"   ciphers: {ciphers}\n"
    content += f"   mac: {mac}\n"
    content += f"   key exchange: {key_exchange}\n"
    content += f"result: {ssl_vulnerability.description}\n"

    return make_snippet(
        content=content,
        viewport=SnippetViewport(
            column=0,
            wrap=True,
            columns_per_line=columns_per_line,
            line=ssl_vulnerability.get_line(),
        ),
    )
