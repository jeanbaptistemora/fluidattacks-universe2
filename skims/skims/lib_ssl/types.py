from enum import (
    Enum,
    IntEnum,
)
from model.core_model import (
    FindingEnum,
    LocalesEnum,
)
from ssl import (
    TLSVersion,
)
from typing import (
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)


class SSLVersionId(IntEnum):
    sslv3_0: int = 0
    tlsv1_0: int = 1
    tlsv1_1: int = 2
    tlsv1_2: int = 3
    tlsv1_3: int = 4


class SSLVersionName(Enum):
    sslv3_0: str = "SSLv3.0"
    tlsv1_0: str = "TLSv1.0"
    tlsv1_1: str = "TLSv1.1"
    tlsv1_2: str = "TLSv1.2"
    tlsv1_3: str = "TLSv1.3"


class SSLSnippetLine(Enum):
    target_title: int = 1
    target: int = 2
    intention_title: int = 3
    intention: int = 4
    information_title: int = 5
    information_versions: int = 6
    request_title: int = 7
    fallback_scsv: int = 8
    min_version: int = 9
    max_version: int = 10
    response_title: int = 11
    handshake_cipher: int = 12
    alert_type: int = 12
    alert_level: int = 13
    alert_description: int = 14


class TLSVersionId(Enum):
    tlsv1_0: TLSVersion = TLSVersion.TLSv1
    tlsv1_1: TLSVersion = TLSVersion.TLSv1_1
    tlsv1_2: TLSVersion = TLSVersion.TLSv1_2
    tlsv1_3: TLSVersion = TLSVersion.TLSv1_3


class SSLSuite(Enum):
    NULL_WITH_NULL_NULL: Tuple[int, int] = (0x00, 0x00)
    RSA_WITH_NULL_MD5: Tuple[int, int] = (0x00, 0x01)
    RSA_WITH_NULL_SHA: Tuple[int, int] = (0x00, 0x02)
    RSA_EXPORT_WITH_RC4_40_MD5: Tuple[int, int] = (0x00, 0x03)
    RSA_WITH_RC4_128_MD5: Tuple[int, int] = (0x00, 0x04)
    RSA_WITH_RC4_128_SHA: Tuple[int, int] = (0x00, 0x05)
    RSA_EXPORT_WITH_RC2_CBC_40_MD5: Tuple[int, int] = (0x00, 0x06)
    RSA_WITH_IDEA_CBC_SHA: Tuple[int, int] = (0x00, 0x07)
    RSA_EXPORT_WITH_DES40_CBC_SHA: Tuple[int, int] = (0x00, 0x08)
    RSA_WITH_DES_CBC_SHA: Tuple[int, int] = (0x00, 0x09)
    RSA_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0x00, 0x0A)
    DH_DSS_EXPORT_WITH_DES40_CBC_SHA: Tuple[int, int] = (0x00, 0x0B)
    DH_DSS_WITH_DES_CBC_SHA: Tuple[int, int] = (0x00, 0x0C)
    DH_DSS_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0x00, 0x0D)
    DH_RSA_EXPORT_WITH_DES40_CBC_SHA: Tuple[int, int] = (0x00, 0x0E)
    DH_RSA_WITH_DES_CBC_SHA: Tuple[int, int] = (0x00, 0x0F)
    DH_RSA_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0x00, 0x10)
    DHE_DSS_EXPORT_WITH_DES40_CBC_SHA: Tuple[int, int] = (0x00, 0x11)
    DHE_DSS_WITH_DES_CBC_SHA: Tuple[int, int] = (0x00, 0x12)
    DHE_DSS_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0x00, 0x13)
    DHE_RSA_EXPORT_WITH_DES40_CBC_SHA: Tuple[int, int] = (0x00, 0x14)
    DHE_RSA_WITH_DES_CBC_SHA: Tuple[int, int] = (0x00, 0x15)
    DHE_RSA_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0x00, 0x16)
    DH_anon_EXPORT_WITH_RC4_40_MD5: Tuple[int, int] = (0x00, 0x17)
    DH_anon_WITH_RC4_128_MD5: Tuple[int, int] = (0x00, 0x18)
    DH_anon_EXPORT_WITH_DES40_CBC_SHA: Tuple[int, int] = (0x00, 0x19)
    DH_anon_WITH_DES_CBC_SHA: Tuple[int, int] = (0x00, 0x1A)
    DH_anon_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0x00, 0x1B)
    KRB5_WITH_DES_CBC_SHA: Tuple[int, int] = (0x00, 0x1E)
    KRB5_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0x00, 0x1F)
    KRB5_WITH_RC4_128_SHA: Tuple[int, int] = (0x00, 0x20)
    KRB5_WITH_IDEA_CBC_SHA: Tuple[int, int] = (0x00, 0x21)
    KRB5_WITH_DES_CBC_MD5: Tuple[int, int] = (0x00, 0x22)
    KRB5_WITH_3DES_EDE_CBC_MD5: Tuple[int, int] = (0x00, 0x23)
    KRB5_WITH_RC4_128_MD5: Tuple[int, int] = (0x00, 0x24)
    KRB5_WITH_IDEA_CBC_MD5: Tuple[int, int] = (0x00, 0x25)
    KRB5_EXPORT_WITH_DES_CBC_40_SHA: Tuple[int, int] = (0x00, 0x26)
    KRB5_EXPORT_WITH_RC2_CBC_40_SHA: Tuple[int, int] = (0x00, 0x27)
    KRB5_EXPORT_WITH_RC4_40_SHA: Tuple[int, int] = (0x00, 0x28)
    KRB5_EXPORT_WITH_DES_CBC_40_MD5: Tuple[int, int] = (0x00, 0x29)
    KRB5_EXPORT_WITH_RC2_CBC_40_MD5: Tuple[int, int] = (0x00, 0x2A)
    KRB5_EXPORT_WITH_RC4_40_MD5: Tuple[int, int] = (0x00, 0x2B)
    PSK_WITH_NULL_SHA: Tuple[int, int] = (0x00, 0x2C)
    DHE_PSK_WITH_NULL_SHA: Tuple[int, int] = (0x00, 0x2D)
    RSA_PSK_WITH_NULL_SHA: Tuple[int, int] = (0x00, 0x2E)
    RSA_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0x00, 0x2F)
    DH_DSS_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0x00, 0x30)
    DH_RSA_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0x00, 0x31)
    DHE_DSS_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0x00, 0x32)
    DHE_RSA_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0x00, 0x33)
    DH_anon_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0x00, 0x34)
    RSA_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0x00, 0x35)
    DH_DSS_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0x00, 0x36)
    DH_RSA_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0x00, 0x37)
    DHE_DSS_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0x00, 0x38)
    DHE_RSA_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0x00, 0x39)
    DH_anon_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0x00, 0x3A)
    RSA_WITH_NULL_SHA256: Tuple[int, int] = (0x00, 0x3B)
    RSA_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0x00, 0x3C)
    RSA_WITH_AES_256_CBC_SHA256: Tuple[int, int] = (0x00, 0x3D)
    DH_DSS_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0x00, 0x3E)
    DH_RSA_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0x00, 0x3F)
    DHE_DSS_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0x00, 0x40)
    RSA_WITH_CAMELLIA_128_CBC_SHA: Tuple[int, int] = (0x00, 0x41)
    DH_DSS_WITH_CAMELLIA_128_CBC_SHA: Tuple[int, int] = (0x00, 0x42)
    DH_RSA_WITH_CAMELLIA_128_CBC_SHA: Tuple[int, int] = (0x00, 0x43)
    DHE_DSS_WITH_CAMELLIA_128_CBC_SHA: Tuple[int, int] = (0x00, 0x44)
    DHE_RSA_WITH_CAMELLIA_128_CBC_SHA: Tuple[int, int] = (0x00, 0x45)
    DH_anon_WITH_CAMELLIA_128_CBC_SHA: Tuple[int, int] = (0x00, 0x46)
    RESERVED_SUITE_00_60: Tuple[int, int] = (0x00, 0x60)
    RESERVED_SUITE_00_61: Tuple[int, int] = (0x00, 0x61)
    RESERVED_SUITE_00_62: Tuple[int, int] = (0x00, 0x62)
    RESERVED_SUITE_00_63: Tuple[int, int] = (0x00, 0x63)
    RESERVED_SUITE_00_64: Tuple[int, int] = (0x00, 0x64)
    RESERVED_SUITE_00_65: Tuple[int, int] = (0x00, 0x65)
    RESERVED_SUITE_00_66: Tuple[int, int] = (0x00, 0x66)
    DHE_RSA_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0x00, 0x67)
    DH_DSS_WITH_AES_256_CBC_SHA256: Tuple[int, int] = (0x00, 0x68)
    DH_RSA_WITH_AES_256_CBC_SHA256: Tuple[int, int] = (0x00, 0x69)
    DHE_DSS_WITH_AES_256_CBC_SHA256: Tuple[int, int] = (0x00, 0x6A)
    DHE_RSA_WITH_AES_256_CBC_SHA256: Tuple[int, int] = (0x00, 0x6B)
    DH_anon_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0x00, 0x6C)
    DH_anon_WITH_AES_256_CBC_SHA256: Tuple[int, int] = (0x00, 0x6D)
    RSA_WITH_CAMELLIA_256_CBC_SHA: Tuple[int, int] = (0x00, 0x84)
    DH_DSS_WITH_CAMELLIA_256_CBC_SHA: Tuple[int, int] = (0x00, 0x85)
    DH_RSA_WITH_CAMELLIA_256_CBC_SHA: Tuple[int, int] = (0x00, 0x86)
    DHE_DSS_WITH_CAMELLIA_256_CBC_SHA: Tuple[int, int] = (0x00, 0x87)
    DHE_RSA_WITH_CAMELLIA_256_CBC_SHA: Tuple[int, int] = (0x00, 0x88)
    DH_anon_WITH_CAMELLIA_256_CBC_SHA: Tuple[int, int] = (0x00, 0x89)
    PSK_WITH_RC4_128_SHA: Tuple[int, int] = (0x00, 0x8A)
    PSK_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0x00, 0x8B)
    PSK_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0x00, 0x8C)
    PSK_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0x00, 0x8D)
    DHE_PSK_WITH_RC4_128_SHA: Tuple[int, int] = (0x00, 0x8E)
    DHE_PSK_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0x00, 0x8F)
    DHE_PSK_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0x00, 0x90)
    DHE_PSK_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0x00, 0x91)
    RSA_PSK_WITH_RC4_128_SHA: Tuple[int, int] = (0x00, 0x92)
    RSA_PSK_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0x00, 0x93)
    RSA_PSK_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0x00, 0x94)
    RSA_PSK_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0x00, 0x95)
    RSA_WITH_SEED_CBC_SHA: Tuple[int, int] = (0x00, 0x96)
    DH_DSS_WITH_SEED_CBC_SHA: Tuple[int, int] = (0x00, 0x97)
    DH_RSA_WITH_SEED_CBC_SHA: Tuple[int, int] = (0x00, 0x98)
    DHE_DSS_WITH_SEED_CBC_SHA: Tuple[int, int] = (0x00, 0x99)
    DHE_RSA_WITH_SEED_CBC_SHA: Tuple[int, int] = (0x00, 0x9A)
    DH_anon_WITH_SEED_CBC_SHA: Tuple[int, int] = (0x00, 0x9B)
    RSA_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0x00, 0x9C)
    RSA_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0x00, 0x9D)
    DHE_RSA_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0x00, 0x9E)
    DHE_RSA_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0x00, 0x9F)
    DH_RSA_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0x00, 0xA0)
    DH_RSA_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0x00, 0xA1)
    DHE_DSS_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0x00, 0xA2)
    DHE_DSS_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0x00, 0xA3)
    DH_DSS_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0x00, 0xA4)
    DH_DSS_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0x00, 0xA5)
    DH_anon_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0x00, 0xA6)
    DH_anon_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0x00, 0xA7)
    PSK_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0x00, 0xA8)
    PSK_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0x00, 0xA9)
    DHE_PSK_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0x00, 0xAA)
    DHE_PSK_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0x00, 0xAB)
    RSA_PSK_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0x00, 0xAC)
    RSA_PSK_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0x00, 0xAD)
    PSK_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0x00, 0xAE)
    PSK_WITH_AES_256_CBC_SHA384: Tuple[int, int] = (0x00, 0xAF)
    PSK_WITH_NULL_SHA256: Tuple[int, int] = (0x00, 0xB0)
    PSK_WITH_NULL_SHA384: Tuple[int, int] = (0x00, 0xB1)
    DHE_PSK_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0x00, 0xB2)
    DHE_PSK_WITH_AES_256_CBC_SHA384: Tuple[int, int] = (0x00, 0xB3)
    DHE_PSK_WITH_NULL_SHA256: Tuple[int, int] = (0x00, 0xB4)
    DHE_PSK_WITH_NULL_SHA384: Tuple[int, int] = (0x00, 0xB5)
    RSA_PSK_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0x00, 0xB6)
    RSA_PSK_WITH_AES_256_CBC_SHA384: Tuple[int, int] = (0x00, 0xB7)
    RSA_PSK_WITH_NULL_SHA256: Tuple[int, int] = (0x00, 0xB8)
    RSA_PSK_WITH_NULL_SHA384: Tuple[int, int] = (0x00, 0xB9)
    RSA_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0x00, 0xBA)
    DH_DSS_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0x00, 0xBB)
    DH_RSA_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0x00, 0xBC)
    DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0x00, 0xBD)
    DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0x00, 0xBE)
    DH_anon_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0x00, 0xBF)
    RSA_WITH_CAMELLIA_256_CBC_SHA256: Tuple[int, int] = (0x00, 0xC0)
    DH_DSS_WITH_CAMELLIA_256_CBC_SHA256: Tuple[int, int] = (0x00, 0xC1)
    DH_RSA_WITH_CAMELLIA_256_CBC_SHA256: Tuple[int, int] = (0x00, 0xC2)
    DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256: Tuple[int, int] = (0x00, 0xC3)
    DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256: Tuple[int, int] = (0x00, 0xC4)
    DH_anon_WITH_CAMELLIA_256_CBC_SHA256: Tuple[int, int] = (0x00, 0xC5)
    SM4_GCM_SM3: Tuple[int, int] = (0x00, 0xC6)
    SM4_CCM_SM3: Tuple[int, int] = (0x00, 0xC7)
    EMPTY_RENEGOTIATION_INFO_SCSV: Tuple[int, int] = (0x00, 0xFF)
    AES_128_GCM_SHA256: Tuple[int, int] = (0x13, 0x01)
    AES_256_GCM_SHA384: Tuple[int, int] = (0x13, 0x02)
    CHACHA20_POLY1305_SHA256: Tuple[int, int] = (0x13, 0x03)
    AES_128_CCM_SHA256: Tuple[int, int] = (0x13, 0x04)
    AES_128_CCM_8_SHA256: Tuple[int, int] = (0x13, 0x05)
    FALLBACK_SCSV: Tuple[int, int] = (0x56, 0x00)
    ECDH_ECDSA_WITH_NULL_SHA: Tuple[int, int] = (0xC0, 0x01)
    ECDH_ECDSA_WITH_RC4_128_SHA: Tuple[int, int] = (0xC0, 0x02)
    ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0xC0, 0x03)
    ECDH_ECDSA_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0xC0, 0x04)
    ECDH_ECDSA_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0xC0, 0x05)
    ECDHE_ECDSA_WITH_NULL_SHA: Tuple[int, int] = (0xC0, 0x06)
    ECDHE_ECDSA_WITH_RC4_128_SHA: Tuple[int, int] = (0xC0, 0x07)
    ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0xC0, 0x08)
    ECDHE_ECDSA_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0xC0, 0x09)
    ECDHE_ECDSA_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0xC0, 0x0A)
    ECDH_RSA_WITH_NULL_SHA: Tuple[int, int] = (0xC0, 0x0B)
    ECDH_RSA_WITH_RC4_128_SHA: Tuple[int, int] = (0xC0, 0x0C)
    ECDH_RSA_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0xC0, 0x0D)
    ECDH_RSA_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0xC0, 0x0E)
    ECDH_RSA_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0xC0, 0x0F)
    ECDHE_RSA_WITH_NULL_SHA: Tuple[int, int] = (0xC0, 0x10)
    ECDHE_RSA_WITH_RC4_128_SHA: Tuple[int, int] = (0xC0, 0x11)
    ECDHE_RSA_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0xC0, 0x12)
    ECDHE_RSA_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0xC0, 0x13)
    ECDHE_RSA_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0xC0, 0x14)
    ECDH_anon_WITH_NULL_SHA: Tuple[int, int] = (0xC0, 0x15)
    ECDH_anon_WITH_RC4_128_SHA: Tuple[int, int] = (0xC0, 0x16)
    ECDH_anon_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0xC0, 0x17)
    ECDH_anon_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0xC0, 0x18)
    ECDH_anon_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0xC0, 0x19)
    SRP_SHA_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0xC0, 0x1A)
    SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0xC0, 0x1B)
    SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0xC0, 0x1C)
    SRP_SHA_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0xC0, 0x1D)
    SRP_SHA_RSA_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0xC0, 0x1E)
    SRP_SHA_DSS_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0xC0, 0x1F)
    SRP_SHA_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0xC0, 0x20)
    SRP_SHA_RSA_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0xC0, 0x21)
    SRP_SHA_DSS_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0xC0, 0x22)
    ECDHE_ECDSA_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x23)
    ECDHE_ECDSA_WITH_AES_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x24)
    ECDH_ECDSA_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x25)
    ECDH_ECDSA_WITH_AES_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x26)
    ECDHE_RSA_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x27)
    ECDHE_RSA_WITH_AES_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x28)
    ECDH_RSA_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x29)
    ECDH_RSA_WITH_AES_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x2A)
    ECDHE_ECDSA_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x2B)
    ECDHE_ECDSA_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x2C)
    ECDH_ECDSA_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x2D)
    ECDH_ECDSA_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x2E)
    ECDHE_RSA_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x2F)
    ECDHE_RSA_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x30)
    ECDH_RSA_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x31)
    ECDH_RSA_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x32)
    ECDHE_PSK_WITH_RC4_128_SHA: Tuple[int, int] = (0xC0, 0x33)
    ECDHE_PSK_WITH_3DES_EDE_CBC_SHA: Tuple[int, int] = (0xC0, 0x34)
    ECDHE_PSK_WITH_AES_128_CBC_SHA: Tuple[int, int] = (0xC0, 0x35)
    ECDHE_PSK_WITH_AES_256_CBC_SHA: Tuple[int, int] = (0xC0, 0x36)
    ECDHE_PSK_WITH_AES_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x37)
    ECDHE_PSK_WITH_AES_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x38)
    ECDHE_PSK_WITH_NULL_SHA: Tuple[int, int] = (0xC0, 0x39)
    ECDHE_PSK_WITH_NULL_SHA256: Tuple[int, int] = (0xC0, 0x3A)
    ECDHE_PSK_WITH_NULL_SHA384: Tuple[int, int] = (0xC0, 0x3B)
    RSA_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x3C)
    RSA_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x3D)
    DH_DSS_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x3E)
    DH_DSS_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x3F)
    DH_RSA_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x40)
    DH_RSA_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x41)
    DHE_DSS_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x42)
    DHE_DSS_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x43)
    DHE_RSA_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x44)
    DHE_RSA_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x45)
    DH_anon_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x46)
    DH_anon_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x47)
    ECDHE_ECDSA_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x48)
    ECDHE_ECDSA_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x49)
    ECDH_ECDSA_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x4A)
    ECDH_ECDSA_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x4B)
    ECDHE_RSA_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x4C)
    ECDHE_RSA_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x4D)
    ECDH_RSA_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x4E)
    ECDH_RSA_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x4F)
    RSA_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x50)
    RSA_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x51)
    DHE_RSA_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x52)
    DHE_RSA_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x53)
    DH_RSA_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x54)
    DH_RSA_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x55)
    DHE_DSS_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x56)
    DHE_DSS_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x57)
    DH_DSS_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x58)
    DH_DSS_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x59)
    DH_anon_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x5A)
    DH_anon_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x5B)
    ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x5C)
    ECDHE_ECDSA_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x5D)
    ECDH_ECDSA_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x5E)
    ECDH_ECDSA_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x5F)
    ECDHE_RSA_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x60)
    ECDHE_RSA_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x61)
    ECDH_RSA_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x62)
    ECDH_RSA_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x63)
    PSK_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x64)
    PSK_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x65)
    DHE_PSK_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x66)
    DHE_PSK_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x67)
    RSA_PSK_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x68)
    RSA_PSK_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x69)
    PSK_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x6A)
    PSK_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x6B)
    DHE_PSK_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x6C)
    DHE_PSK_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x6D)
    RSA_PSK_WITH_ARIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x6E)
    RSA_PSK_WITH_ARIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x6F)
    ECDHE_PSK_WITH_ARIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x70)
    ECDHE_PSK_WITH_ARIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x71)
    ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x72)
    ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x73)
    ECDH_ECDSA_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x74)
    ECDH_ECDSA_WITH_CAMELLIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x75)
    ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x76)
    ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x77)
    ECDH_RSA_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x78)
    ECDH_RSA_WITH_CAMELLIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x79)
    RSA_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x7A)
    RSA_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x7B)
    DHE_RSA_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x7C)
    DHE_RSA_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x7D)
    DH_RSA_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x7E)
    DH_RSA_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x7F)
    DHE_DSS_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x80)
    DHE_DSS_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x81)
    DH_DSS_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x82)
    DH_DSS_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x83)
    DH_anon_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x84)
    DH_anon_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x85)
    ECDHE_ECDSA_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x86)
    ECDHE_ECDSA_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x87)
    ECDH_ECDSA_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x88)
    ECDH_ECDSA_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x89)
    ECDHE_RSA_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x8A)
    ECDHE_RSA_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x8B)
    ECDH_RSA_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x8C)
    ECDH_RSA_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x8D)
    PSK_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x8E)
    PSK_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x8F)
    DHE_PSK_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x90)
    DHE_PSK_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x91)
    RSA_PSK_WITH_CAMELLIA_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0x92)
    RSA_PSK_WITH_CAMELLIA_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0x93)
    PSK_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x94)
    PSK_WITH_CAMELLIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x95)
    DHE_PSK_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x96)
    DHE_PSK_WITH_CAMELLIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x97)
    RSA_PSK_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x98)
    RSA_PSK_WITH_CAMELLIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x99)
    ECDHE_PSK_WITH_CAMELLIA_128_CBC_SHA256: Tuple[int, int] = (0xC0, 0x9A)
    ECDHE_PSK_WITH_CAMELLIA_256_CBC_SHA384: Tuple[int, int] = (0xC0, 0x9B)
    RSA_WITH_AES_128_CCM: Tuple[int, int] = (0xC0, 0x9C)
    RSA_WITH_AES_256_CCM: Tuple[int, int] = (0xC0, 0x9D)
    DHE_RSA_WITH_AES_128_CCM: Tuple[int, int] = (0xC0, 0x9E)
    DHE_RSA_WITH_AES_256_CCM: Tuple[int, int] = (0xC0, 0x9F)
    RSA_WITH_AES_128_CCM_8: Tuple[int, int] = (0xC0, 0xA0)
    RSA_WITH_AES_256_CCM_8: Tuple[int, int] = (0xC0, 0xA1)
    DHE_RSA_WITH_AES_128_CCM_8: Tuple[int, int] = (0xC0, 0xA2)
    DHE_RSA_WITH_AES_256_CCM_8: Tuple[int, int] = (0xC0, 0xA3)
    PSK_WITH_AES_128_CCM: Tuple[int, int] = (0xC0, 0xA4)
    PSK_WITH_AES_256_CCM: Tuple[int, int] = (0xC0, 0xA5)
    DHE_PSK_WITH_AES_128_CCM: Tuple[int, int] = (0xC0, 0xA6)
    DHE_PSK_WITH_AES_256_CCM: Tuple[int, int] = (0xC0, 0xA7)
    PSK_WITH_AES_128_CCM_8: Tuple[int, int] = (0xC0, 0xA8)
    PSK_WITH_AES_256_CCM_8: Tuple[int, int] = (0xC0, 0xA9)
    PSK_DHE_WITH_AES_128_CCM_8: Tuple[int, int] = (0xC0, 0xAA)
    PSK_DHE_WITH_AES_256_CCM_8: Tuple[int, int] = (0xC0, 0xAB)
    ECDHE_ECDSA_WITH_AES_128_CCM: Tuple[int, int] = (0xC0, 0xAC)
    ECDHE_ECDSA_WITH_AES_256_CCM: Tuple[int, int] = (0xC0, 0xAD)
    ECDHE_ECDSA_WITH_AES_128_CCM_8: Tuple[int, int] = (0xC0, 0xAE)
    ECDHE_ECDSA_WITH_AES_256_CCM_8: Tuple[int, int] = (0xC0, 0xAF)
    ECCPWD_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0xC0, 0xB0)
    ECCPWD_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0xC0, 0xB1)
    ECCPWD_WITH_AES_128_CCM_SHA256: Tuple[int, int] = (0xC0, 0xB2)
    ECCPWD_WITH_AES_256_CCM_SHA384: Tuple[int, int] = (0xC0, 0xB3)
    SHA256_SHA256: Tuple[int, int] = (0xC0, 0xB4)
    SHA384_SHA384: Tuple[int, int] = (0xC0, 0xB5)
    GOSTR341112_256_WITH_KUZNYECHIK_CTR_OMAC: Tuple[int, int] = (0xC1, 0x00)
    GOSTR341112_256_WITH_MAGMA_CTR_OMAC: Tuple[int, int] = (0xC1, 0x01)
    GOSTR341112_256_WITH_28147_CNT_IMIT: Tuple[int, int] = (0xC1, 0x02)
    GOSTR341112_256_WITH_KUZNYECHIK_MGM_L: Tuple[int, int] = (0xC1, 0x03)
    GOSTR341112_256_WITH_MAGMA_MGM_L: Tuple[int, int] = (0xC1, 0x04)
    GOSTR341112_256_WITH_KUZNYECHIK_MGM_S: Tuple[int, int] = (0xC1, 0x05)
    GOSTR341112_256_WITH_MAGMA_MGM_S: Tuple[int, int] = (0xC1, 0x06)
    ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256: Tuple[int, int] = (0xCC, 0xA8)
    ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256: Tuple[int, int] = (0xCC, 0xA9)
    DHE_RSA_WITH_CHACHA20_POLY1305_SHA256: Tuple[int, int] = (0xCC, 0xAA)
    PSK_WITH_CHACHA20_POLY1305_SHA256: Tuple[int, int] = (0xCC, 0xAB)
    ECDHE_PSK_WITH_CHACHA20_POLY1305_SHA256: Tuple[int, int] = (0xCC, 0xAC)
    DHE_PSK_WITH_CHACHA20_POLY1305_SHA256: Tuple[int, int] = (0xCC, 0xAD)
    RSA_PSK_WITH_CHACHA20_POLY1305_SHA256: Tuple[int, int] = (0xCC, 0xAE)
    ECDHE_PSK_WITH_AES_128_GCM_SHA256: Tuple[int, int] = (0xD0, 0x01)
    ECDHE_PSK_WITH_AES_256_GCM_SHA384: Tuple[int, int] = (0xD0, 0x02)
    ECDHE_PSK_WITH_AES_128_CCM_8_SHA256: Tuple[int, int] = (0xD0, 0x03)
    ECDHE_PSK_WITH_AES_128_CCM_SHA256: Tuple[int, int] = (0xD0, 0x05)
    UNKNOWN: Tuple[int, int] = (-1, -1)


class SSLHandshakeRecord(Enum):
    CLIENT_HELLO: int = 1
    SERVER_HELLO: int = 2
    CERTIFICATE: int = 11
    SERVER_KEY_EXCHANGE: int = 12
    CERTIFICATE_REQUEST: int = 13
    SERVER_HELLO_DONE: int = 14
    CERTIFICATE_VERIFY: int = 15
    CLIENT_KEY_EXCHANGE: int = 16
    FINISHED: int = 20


class SSLRecord(Enum):
    CHANGE_CIPHER_SPEC: int = 20
    ALERT: int = 21
    HANDSHAKE: int = 22
    APPLICATION_DATA: int = 23


class SSLAlertLevel(Enum):
    WARNING: int = 1
    FATAL: int = 2
    unknown: int = 255


class SSLAlertDescription(Enum):
    close_notify: int = 0
    unexpected_message: int = 10
    bad_record_mac: int = 20
    decryption_failed_reserved: int = 21
    record_overflow: int = 22
    decompression_failure_reserved: int = 30
    handshake_failure: int = 40
    no_certificate_reserved: int = 41
    bad_certificate: int = 42
    unsupported_certificate: int = 43
    certificate_revoked: int = 44
    certificate_expired: int = 45
    certificate_unknown: int = 46
    illegal_parameter: int = 47
    unknown_ca: int = 48
    access_denied: int = 49
    decode_error: int = 50
    decrypt_error: int = 51
    export_restriction_reserved: int = 60
    protocol_version: int = 70
    insufficient_security: int = 71
    internal_error: int = 80
    inappropriate_fallback: int = 86
    user_canceled: int = 90
    no_renegotiation_reserved: int = 100
    missing_extension: int = 109
    unsupported_extension: int = 110
    certificate_unobtainable_reserved: int = 111
    unrecognized_name: int = 112
    bad_certificate_status_response: int = 113
    bad_certificate_hash_value_reserved: int = 114
    unknown_psk_identity: int = 115
    certificate_required: int = 116
    no_application_protocol: int = 120
    unknown: int = 255


class SSLAlert(NamedTuple):
    level: SSLAlertLevel
    description: SSLAlertDescription


class SSLServerHandshake(NamedTuple):
    record: SSLHandshakeRecord
    version_id: SSLVersionId
    cipher_suite: SSLSuite


class SSLServerResponse(NamedTuple):
    record: SSLRecord
    version_id: SSLVersionId
    alert: Optional[SSLAlert] = None
    handshake: Optional[SSLServerHandshake] = None


class SSLContext(NamedTuple):
    host: str = "localhost"
    port: int = 443
    tls_responses: Tuple[SSLServerResponse, ...] = ()

    def get_supported_tls_versions(self) -> Tuple[SSLVersionId, ...]:
        return tuple(
            tls_response.handshake.version_id
            for tls_response in self.tls_responses
            if tls_response.handshake is not None
        )

    def __str__(self) -> str:
        return f"{self.host}:{self.port}"


class SSLSettings(NamedTuple):
    context: SSLContext
    scsv: bool = False
    anonymous: bool = False
    min_version: SSLVersionId = SSLVersionId.sslv3_0
    max_version: SSLVersionId = SSLVersionId.tlsv1_3
    intention: Dict[LocalesEnum, str] = {
        LocalesEnum.EN: "establish SSL/TLS connection",
        LocalesEnum.ES: "establecer conexión SSL/TLS",
    }
    mac_names: List[str] = []
    cipher_names: List[str] = []
    anon_key_exchange_names: List[str] = []
    key_exchange_names: List[str] = []

    def __str__(self) -> str:
        return str(self.context)


class SSLVulnerability(NamedTuple):
    description: str
    line: SSLSnippetLine
    ssl_settings: SSLSettings
    server_response: Optional[SSLServerResponse]
    finding: FindingEnum

    def get_line(self) -> int:
        return self.line.value

    def __str__(self) -> str:
        return str(self.ssl_settings)
