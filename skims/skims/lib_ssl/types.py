from enum import (
    Enum,
)
from model.core_model import (
    FindingEnum,
    LocalesEnum,
    SkimsSslTarget,
)
from typing import (
    Dict,
    List,
    NamedTuple,
    Tuple,
)


class SSLContext(NamedTuple):
    target: SkimsSslTarget

    def __str__(self) -> str:
        return f"{self.target.host}:{self.target.port}"


class SSLSettings(NamedTuple):
    host: str = "localhost"
    port: int = 443
    scsv: bool = False
    anonymous: bool = False
    min_version: Tuple[int, int] = (3, 0)
    max_version: Tuple[int, int] = (3, 4)
    intention: Dict[LocalesEnum, str] = {
        LocalesEnum.EN: "establish SSL connection",
        LocalesEnum.ES: "establecer conexión SSL",
    }
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
    finding: FindingEnum

    def get_line(self) -> int:
        return self.line.value


ssl_suites: Dict["str", List[int]] = {
    "ECDH_ECDSA_WITH_RC4_128_SHA": [0xC0, 0x02],
    "ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA": [0xC0, 0x03],
    "ECDH_ECDSA_WITH_AES_128_CBC_SHA": [0xC0, 0x04],
    "ECDH_ECDSA_WITH_AES_256_CBC_SHA": [0xC0, 0x05],
    "ECDHE_ECDSA_WITH_RC4_128_SHA": [0xC0, 0x07],
    "ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA": [0xC0, 0x08],
    "ECDHE_ECDSA_WITH_AES_128_CBC_SHA": [0xC0, 0x09],
    "ECDHE_ECDSA_WITH_AES_256_CBC_SHA": [0xC0, 0x0A],
    "ECDH_RSA_WITH_RC4_128_SHA": [0xC0, 0x0C],
    "ECDH_RSA_WITH_3DES_EDE_CBC_SHA": [0xC0, 0x0D],
    "ECDH_RSA_WITH_AES_128_CBC_SHA": [0xC0, 0x0E],
    "ECDH_RSA_WITH_AES_256_CBC_SHA": [0xC0, 0x0F],
    "ECDHE_RSA_WITH_RC4_128_SHA": [0xC0, 0x11],
    "ECDHE_RSA_WITH_3DES_EDE_CBC_SHA": [0xC0, 0x12],
    "ECDHE_RSA_WITH_AES_128_CBC_SHA": [0xC0, 0x13],
    "ECDHE_RSA_WITH_AES_256_CBC_SHA": [0xC0, 0x14],
    "SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA": [0xC0, 0x1B],
    "SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA": [0xC0, 0x1C],
    "SRP_SHA_RSA_WITH_AES_128_CBC_SHA": [0xC0, 0x1E],
    "SRP_SHA_DSS_WITH_AES_128_CBC_SHA": [0xC0, 0x1F],
    "SRP_SHA_RSA_WITH_AES_256_CBC_SHA": [0xC0, 0x21],
    "SRP_SHA_DSS_WITH_AES_256_CBC_SHA": [0xC0, 0x22],
    "RSA_WITH_NULL_MD5": [0x00, 0x01],
    "RSA_WITH_NULL_SHA": [0x00, 0x02],
    "RSA_EXPORT_WITH_RC4_40_MD5": [0x00, 0x03],
    "RSA_WITH_RC4_128_MD5": [0x00, 0x04],
    "RSA_WITH_RC4_128_SHA": [0x00, 0x05],
    "RSA_EXPORT_WITH_RC2_CBC_40_MD5": [0x00, 0x06],
    "RSA_WITH_IDEA_CBC_SHA": [0x00, 0x07],
    "RSA_EXPORT_WITH_DES40_CBC_SHA": [0x00, 0x08],
    "RSA_WITH_DES_CBC_SHA": [0x00, 0x09],
    "RSA_WITH_3DES_EDE_CBC_SHA": [0x00, 0x0A],
    "DH_DSS_EXPORT_WITH_DES40_CBC_SHA": [0x00, 0x0B],
    "DH_DSS_WITH_DES_CBC_SHA": [0x00, 0x0C],
    "DH_DSS_WITH_3DES_EDE_CBC_SHA": [0x00, 0x0D],
    "DH_RSA_EXPORT_WITH_DES40_CBC_SHA": [0x00, 0x0E],
    "DH_RSA_WITH_DES_CBC_SHA": [0x00, 0x0F],
    "DH_RSA_WITH_3DES_EDE_CBC_SHA": [0x00, 0x10],
    "DHE_DSS_EXPORT_WITH_DES40_CBC_SHA": [0x00, 0x11],
    "DHE_DSS_WITH_DES_CBC_SHA": [0x00, 0x12],
    "DHE_DSS_WITH_3DES_EDE_CBC_SHA": [0x00, 0x13],
    "DHE_RSA_EXPORT_WITH_DES40_CBC_SHA": [0x00, 0x14],
    "DHE_RSA_WITH_DES_CBC_SHA": [0x00, 0x15],
    "DHE_RSA_WITH_3DES_EDE_CBC_SHA": [0x00, 0x16],
    "DH_anon_EXPORT_WITH_RC4_40_MD5": [0x00, 0x17],
    "DH_anon_WITH_RC4_128_MD5": [0x00, 0x18],
    "DH_anon_EXPORT_WITH_DES40_CBC_SHA": [0x00, 0x19],
    "RSA_WITH_AES_128_CBC_SHA": [0x00, 0x2F],
    "DHE_DSS_WITH_AES_128_CBC_SHA": [0x00, 0x32],
    "DHE_RSA_WITH_AES_128_CBC_SHA": [0x00, 0x33],
    "RSA_WITH_AES_256_CBC_SHA": [0x00, 0x35],
    "DHE_DSS_WITH_AES_256_CBC_SHA": [0x00, 0x38],
    "DHE_RSA_WITH_AES_256_CBC_SHA": [0x00, 0x39],
    "RSA_WITH_CAMELLIA_128_CBC_SHA": [0x00, 0x41],
    "DHE_DSS_WITH_CAMELLIA_128_CBC_SHA": [0x00, 0x44],
    "DHE_RSA_WITH_CAMELLIA_128_CBC_SHA": [0x00, 0x45],
    "RSA_WITH_CAMELLIA_256_CBC_SHA": [0x00, 0x84],
    "DHE_DSS_WITH_CAMELLIA_256_CBC_SHA": [0x00, 0x87],
    "DHE_RSA_WITH_CAMELLIA_256_CBC_SHA": [0x00, 0x88],
    "RSA_WITH_SEED_CBC_SHA": [0x00, 0x96],
    "DHE_DSS_WITH_SEED_CBC_SHA": [0x00, 0x99],
    "DHE_RSA_WITH_SEED_CBC_SHA": [0x00, 0x9A],
    "EMPTY_RENEGOTIATION_INFO_SCSV": [0x00, 0xFF],
}
