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


class SSLEllipticCurves(NamedTuple):
    DH_RSA_EXPORT_WITH_DES40_CBC_SHA: List[int] = [0x00, 0x0E]
    DH_DSS_WITH_3DES_EDE_CBC_SHA: List[int] = [0x00, 0x0D]
    DH_anon_EXPORT_WITH_DES40_CBC_SHA: List[int] = [0x00, 0x19]
    DH_DSS_EXPORT_WITH_DES40_CBC_SHA: List[int] = [0x00, 0x0B]
    DH_DSS_WITH_DES_CBC_SHA: List[int] = [0x00, 0x0C]
    DH_anon_WITH_RC4_128_MD5: List[int] = [0x00, 0x18]
    RSA_WITH_DES_CBC_SHA: List[int] = [0x00, 0x09]
    RSA_WITH_3DES_EDE_CBC_SHA: List[int] = [0x00, 0x0A]
    DHE_RSA_WITH_3DES_EDE_CBC_SHA: List[int] = [0x00, 0x16]
    DH_anon_EXPORT_WITH_RC4_40_MD5: List[int] = [0x00, 0x17]
    RSA_EXPORT_WITH_DES40_CBC_SHA: List[int] = [0x00, 0x08]
    RSA_EXPORT_WITH_RC2_CBC_40_MD5: List[int] = [0x00, 0x06]
    RSA_WITH_IDEA_CBC_SHA: List[int] = [0x00, 0x07]
    DHE_RSA_EXPORT_WITH_DES40_CBC_SHA: List[int] = [0x00, 0x14]
    DHE_RSA_WITH_DES_CBC_SHA: List[int] = [0x00, 0x15]
    RSA_WITH_RC4_128_MD5: List[int] = [0x00, 0x04]
    RSA_WITH_RC4_128_SHA: List[int] = [0x00, 0x05]
    DHE_DSS_WITH_DES_CBC_SHA: List[int] = [0x00, 0x12]
    DHE_DSS_WITH_3DES_EDE_CBC_SHA: List[int] = [0x00, 0x13]
    RSA_WITH_NULL_MD5: List[int] = [0x00, 0x01]
    RSA_WITH_NULL_SHA: List[int] = [0x00, 0x02]
    RSA_EXPORT_WITH_RC4_40_MD5: List[int] = [0x00, 0x03]
    DH_RSA_WITH_DES_CBC_SHA: List[int] = [0x00, 0x0F]
    DH_RSA_WITH_3DES_EDE_CBC_SHA: List[int] = [0x00, 0x10]
    DHE_DSS_EXPORT_WITH_DES40_CBC_SHA: List[int] = [0x00, 0x11]

    def get_all(self) -> List[int]:
        return sum(list(self), [])


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


class SSLSuites(NamedTuple):
    ECDHE_RSA_WITH_AES_256_CBC_SHA: List[int] = [0xC0, 0x14]
    ECDHE_ECDSA_WITH_AES_256_CBC_SHA: List[int] = [0xC0, 0x0A]
    SRP_SHA_DSS_WITH_AES_256_CBC_SHA: List[int] = [0xC0, 0x22]
    SRP_SHA_RSA_WITH_AES_256_CBC_SHA: List[int] = [0xC0, 0x21]
    DHE_RSA_WITH_AES_256_CBC_SHA: List[int] = [0x00, 0x39]
    DHE_DSS_WITH_AES_256_CBC_SHA: List[int] = [0x00, 0x38]
    DHE_RSA_WITH_CAMELLIA_256_CBC_SHA: List[int] = [0x00, 0x88]
    DHE_DSS_WITH_CAMELLIA_256_CBC_SHA: List[int] = [0x00, 0x87]
    ECDH_RSA_WITH_AES_256_CBC_SHA: List[int] = [0xC0, 0x0F]
    ECDH_ECDSA_WITH_AES_256_CBC_SHA: List[int] = [0xC0, 0x05]
    RSA_WITH_AES_256_CBC_SHA: List[int] = [0x00, 0x35]
    RSA_WITH_CAMELLIA_256_CBC_SHA: List[int] = [0x00, 0x84]
    ECDHE_RSA_WITH_3DES_EDE_CBC_SHA: List[int] = [0xC0, 0x12]
    ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA: List[int] = [0xC0, 0x08]
    SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA: List[int] = [0xC0, 0x1C]
    SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA: List[int] = [0xC0, 0x1B]
    DHE_RSA_WITH_3DES_EDE_CBC_SHA: List[int] = [0x00, 0x16]
    DHE_DSS_WITH_3DES_EDE_CBC_SHA: List[int] = [0x00, 0x13]
    ECDH_RSA_WITH_3DES_EDE_CBC_SHA: List[int] = [0xC0, 0x0D]
    ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA: List[int] = [0xC0, 0x03]
    RSA_WITH_3DES_EDE_CBC_SHA: List[int] = [0x00, 0x0A]
    ECDHE_RSA_WITH_AES_128_CBC_SHA: List[int] = [0xC0, 0x13]
    ECDHE_ECDSA_WITH_AES_128_CBC_SHA: List[int] = [0xC0, 0x09]
    SRP_SHA_DSS_WITH_AES_128_CBC_SHA: List[int] = [0xC0, 0x1F]
    SRP_SHA_RSA_WITH_AES_128_CBC_SHA: List[int] = [0xC0, 0x1E]
    DHE_RSA_WITH_AES_128_CBC_SHA: List[int] = [0x00, 0x33]
    DHE_DSS_WITH_AES_128_CBC_SHA: List[int] = [0x00, 0x32]
    DHE_RSA_WITH_SEED_CBC_SHA: List[int] = [0x00, 0x9A]
    DHE_DSS_WITH_SEED_CBC_SHA: List[int] = [0x00, 0x99]
    DHE_RSA_WITH_CAMELLIA_128_CBC_SHA: List[int] = [0x00, 0x45]
    DHE_DSS_WITH_CAMELLIA_128_CBC_SHA: List[int] = [0x00, 0x44]
    ECDH_RSA_WITH_AES_128_CBC_SHA: List[int] = [0xC0, 0x0E]
    ECDH_ECDSA_WITH_AES_128_CBC_SHA: List[int] = [0xC0, 0x04]
    RSA_WITH_AES_128_CBC_SHA: List[int] = [0x00, 0x2F]
    RSA_WITH_SEED_CBC_SHA: List[int] = [0x00, 0x96]
    RSA_WITH_CAMELLIA_128_CBC_SHA: List[int] = [0x00, 0x41]
    ECDHE_RSA_WITH_RC4_128_SHA: List[int] = [0xC0, 0x11]
    ECDHE_ECDSA_WITH_RC4_128_SHA: List[int] = [0xC0, 0x07]
    ECDH_RSA_WITH_RC4_128_SHA: List[int] = [0xC0, 0x0C]
    ECDH_ECDSA_WITH_RC4_128_SHA: List[int] = [0xC0, 0x02]
    RSA_WITH_RC4_128_SHA: List[int] = [0x00, 0x05]
    RSA_WITH_RC4_128_MD5: List[int] = [0x00, 0x04]
    DHE_RSA_WITH_DES_CBC_SHA: List[int] = [0x00, 0x15]
    DHE_DSS_WITH_DES_CBC_SHA: List[int] = [0x00, 0x12]
    RSA_WITH_DES_CBC_SHA: List[int] = [0x00, 0x09]
    DHE_RSA_EXPORT_WITH_DES40_CBC_SHA: List[int] = [0x00, 0x14]
    DHE_DSS_EXPORT_WITH_DES40_CBC_SHA: List[int] = [0x00, 0x11]
    RSA_EXPORT_WITH_DES40_CBC_SHA: List[int] = [0x00, 0x08]
    RSA_EXPORT_WITH_RC2_CBC_40_MD5: List[int] = [0x00, 0x06]
    RSA_EXPORT_WITH_RC4_40_MD5: List[int] = [0x00, 0x03]
    EMPTY_RENEGOTIATION_INFO_SCSV: List[int] = [0x00, 0xFF]

    def get_all(self) -> List[int]:
        return sum(list(self), [])


class SSLVulnerability(NamedTuple):
    description: str
    line: SSLSnippetLine
    ssl_settings: SSLSettings
    finding: FindingEnum

    def get_line(self) -> int:
        return self.line.value
