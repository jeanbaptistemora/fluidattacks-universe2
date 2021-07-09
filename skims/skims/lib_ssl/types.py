from enum import (
    Enum,
)
from model import (
    core_model,
)
from typing import (
    List,
    NamedTuple,
    Tuple,
)


class SSLContext(NamedTuple):
    target: core_model.SkimsSslTarget

    def __str__(self) -> str:
        return f"{self.target.host}:{self.target.port}"


class SSLSettings(NamedTuple):
    host: str = "localhost"
    port: int = 443
    scsv: bool = False
    anonymous: bool = False
    min_version: Tuple[int, int] = (3, 0)
    max_version: Tuple[int, int] = (3, 4)
    intention: str = "establish SSL connection"
    mac_names: List[str] = ["sha", "sha256", "sha384", "aead"]
    cipher_names: List[str] = [
        "chacha20-poly1305",
        "aes256gcm",
        "aes128gcm",
        "aes256ccm",
        "aes128ccm",
        "aes256",
        "aes128",
        "3des",
    ]
    anon_key_exchange_names: List[str] = [
        "ecdh_anon",
        "dh_anon",
    ]
    key_exchange_names: List[str] = [
        "rsa",
        "dhe_rsa",
        "ecdhe_rsa",
        "srp_sha",
        "srp_sha_rsa",
        "ecdh_anon",
        "dh_anon",
        "ecdhe_ecdsa",
        "dhe_dsa",
    ]

    def get_target(self) -> str:
        return f"{self.host}:{self.port}"

    def get_key_exchange_names(self) -> List[str]:
        if self.anonymous:
            return self.anon_key_exchange_names
        return self.key_exchange_names


class SSLSnippetLine(Enum):
    fallback_scsv: int = 3
    min_version: int = 4
    max_version: int = 5
    ciphers: int = 6
    mac: int = 7
    key_exchange: int = 8


class SSLVulnerability(NamedTuple):
    description: str
    line: SSLSnippetLine
    ssl_settings: SSLSettings
    finding: core_model.FindingEnum

    def get_line(self) -> int:
        return self.line.value
