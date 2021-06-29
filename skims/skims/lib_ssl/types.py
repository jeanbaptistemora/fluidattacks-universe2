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
    min_version: Tuple[int, int] = (3, 0)
    max_version: Tuple[int, int] = (3, 4)
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
