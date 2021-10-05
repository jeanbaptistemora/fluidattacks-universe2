# pylint: disable=invalid-name
# pylint: disable=too-many-lines
from enum import (
    Enum,
    IntEnum,
)
from typing import (
    Iterator,
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


class SSLSuiteVuln(Enum):
    NO_PFS: int = 1
    MD5: int = 2
    SHA: int = 3
    RC4: int = 4
    RC2: int = 5
    CBC: int = 6
    DES: int = 7
    DES3: int = 8
    SM3: int = 9
    SM4: int = 10
    EXPORT_GRADE: int = 11
    ANON_KEY_EXCHANGE: int = 12
    NULL_AUTHENTICATION: int = 13
    NULL_ENCRYPTION: int = 14


class SSLKeyExchange(Enum):
    NONE: int = 1
    NULL: int = 2
    RSA: int = 3
    DH: int = 4
    DHE: int = 5
    KRB_5: int = 6
    PSK: int = 7
    ECDH: int = 8
    ECDHE: int = 9
    ECCPWD: int = 10
    SRP: int = 11
    UNKNOWN: int = 12


class SSLAuthentication(Enum):
    NONE: int = 1
    NULL: int = 2
    RSA: int = 3
    DSS: int = 4
    ANON: int = 5
    PSK: int = 6
    KRB_5: int = 7
    ECDSA: int = 8
    SHA_RSA: int = 9
    SHA_DSS: int = 10
    ECCPWD: int = 11
    SHA: int = 12
    DHE: int = 13
    UNKNOWN: int = 14


class SSLEncryption(Enum):
    NONE: int = 1
    NULL: int = 2
    RC4_40: int = 3
    RC4_56: int = 4
    RC4_128: int = 5
    RC2_40_CBC: int = 6
    RC2_56_CBC: int = 7
    IDEA_CBC: int = 8
    DES_40_CBC: int = 9
    DES_56_CBC: int = 10
    DES3_EDE_CBC: int = 11
    AES_128_CBC: int = 12
    AES_256_CBC: int = 13
    CAMELLIA_128_CBC: int = 14
    CAMELLIA_256_CBC: int = 15
    CAMELLIA_128_GCM: int = 16
    CAMELLIA_256_GCM: int = 17
    SEED_CBC: int = 18
    AES_128_GCM: int = 19
    AES_256_GCM: int = 20
    AES_128_CCM: int = 21
    AES_128_CCM_8: int = 22
    AES_256_CCM: int = 23
    AES_256_CCM_8: int = 24
    SM_4_GCM: int = 25
    SM_4_CCM: int = 26
    CHACHA_20_POLY_1305: int = 27
    ARIA_128_CBC: int = 28
    ARIA_256_CBC: int = 29
    ARIA_128_GCM: int = 30
    ARIA_256_GCM: int = 31
    UNKNOWN: int = 32


class SSLHash(Enum):
    NONE: int = 1
    NULL: int = 2
    MD5: int = 3
    SHA: int = 4
    SHA256: int = 5
    SHA384: int = 6
    SM3: int = 7
    UNKNOWN: int = 8


class SSLSuiteInfo(NamedTuple):
    rfc: int
    iana_name: str
    openssl_name: Optional[str]
    gnutls_name: Optional[str]
    code: Optional[Tuple[int, int]]
    key_exchange: SSLKeyExchange
    authentication: SSLAuthentication
    encryption: SSLEncryption
    ssl_hash: SSLHash
    tls_versions: Tuple[SSLVersionId, ...]
    vulnerabilities: Tuple[SSLSuiteVuln, ...]

    def get_openssl_name(self) -> str:
        if not self.openssl_name:
            return "---"
        return self.openssl_name

    def get_gnutls_name(self) -> str:
        if not self.gnutls_name:
            return "---"
        return self.gnutls_name

    def get_code_str(self) -> str:
        if not self.code:
            return "---"
        return " ".join([hex(byte) for byte in self.code])

    def get_vuln_str(self) -> str:
        if not self.vulnerabilities:
            return "---"
        return ", ".join([vuln.name for vuln in self.vulnerabilities])


#  Information taken from ciphersuite.info and
#  https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml
class SSLCipherSuite(Enum):
    NULL_WITH_NULL_NULL: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_NULL_WITH_NULL_NULL",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x00),
        key_exchange=SSLKeyExchange.NULL,
        authentication=SSLAuthentication.NULL,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.NULL,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_AUTHENTICATION,
            SSLSuiteVuln.NULL_ENCRYPTION,
        ),
    )
    RSA_WITH_NULL_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_RSA_WITH_NULL_MD5",
        openssl_name="NULL-MD5",
        gnutls_name="TLS_RSA_NULL_MD5",
        code=(0x00, 0x01),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.MD5,
        ),
    )
    RSA_WITH_NULL_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_RSA_WITH_NULL_SHA",
        openssl_name="NULL-SHA",
        gnutls_name="TLS_RSA_NULL_SHA1",
        code=(0x00, 0x02),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_EXPORT_WITH_RC4_40_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4346,
        iana_name="TLS_RSA_EXPORT_WITH_RC4_40_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x03),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.RC4_40,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.MD5,
        ),
    )
    RSA_WITH_RC4_128_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_RSA_WITH_RC4_128_MD5",
        openssl_name=None,
        gnutls_name="TLS_RSA_ARCFOUR_128_MD5",
        code=(0x00, 0x04),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.MD5,
        ),
    )
    RSA_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_RSA_WITH_RC4_128_SHA",
        openssl_name="",
        gnutls_name="TLS_RSA_ARCFOUR_128_SHA1",
        code=(0x00, 0x05),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_EXPORT_WITH_RC2_CBC_40_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4346,
        iana_name="TLS_RSA_EXPORT_WITH_RC2_CBC_40_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x06),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.RC2_40_CBC,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.RC2,
            SSLSuiteVuln.MD5,
        ),
    )
    RSA_WITH_IDEA_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5469,
        iana_name="TLS_RSA_WITH_IDEA_CBC_SHA",
        openssl_name="IDEA-CBC-SHA",
        gnutls_name=None,
        code=(0x00, 0x07),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.IDEA_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_EXPORT_WITH_DES40_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4346,
        iana_name="TLS_RSA_EXPORT_WITH_DES40_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x08),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES_40_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_WITH_DES_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5469,
        iana_name="TLS_RSA_WITH_DES_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x09),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES_56_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_RSA_WITH_3DES_EDE_CBC_SHA",
        openssl_name="DES-CBC3-SHA",
        gnutls_name="TLS_RSA_3DES_EDE_CBC_SHA1",
        code=(0x00, 0x0A),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_DSS_EXPORT_WITH_DES40_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4346,
        iana_name="TLS_DH_DSS_EXPORT_WITH_DES40_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x0B),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.DES_40_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_DSS_WITH_DES_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5469,
        iana_name="TLS_DH_DSS_WITH_DES_CBC_SHA",
        openssl_name="",
        gnutls_name="",
        code=(0x00, 0x0C),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.DES_56_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_DSS_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x0D),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_RSA_EXPORT_WITH_DES40_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4346,
        iana_name="TLS_DH_RSA_EXPORT_WITH_DES40_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x0E),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES_40_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_RSA_WITH_DES_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5469,
        iana_name="TLS_DH_RSA_WITH_DES_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x0F),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES_56_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_RSA_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x10),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_DSS_EXPORT_WITH_DES40_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4346,
        iana_name="TLS_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x11),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.DES_40_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_DSS_WITH_DES_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5469,
        iana_name="TLS_DHE_DSS_WITH_DES_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x12),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.DES_56_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_DSS_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA",
        openssl_name="DHE-DSS-DES-CBC3-SHA",
        gnutls_name="TLS_DHE_DSS_3DES_EDE_CBC_SHA1",
        code=(0x00, 0x13),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_RSA_EXPORT_WITH_DES40_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4346,
        iana_name="TLS_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x14),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES_40_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_RSA_WITH_DES_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5469,
        iana_name="TLS_DHE_RSA_WITH_DES_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x15),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES_56_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_RSA_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA",
        openssl_name="DHE-RSA-DES-CBC3-SHA",
        gnutls_name="TLS_DHE_RSA_3DES_EDE_CBC_SHA1",
        code=(0x00, 0x16),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_anon_EXPORT_WITH_RC4_40_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4346,
        iana_name="TLS_DH_anon_EXPORT_WITH_RC4_40_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x17),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.RC4_40,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.MD5,
        ),
    )
    DH_anon_WITH_RC4_128_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_anon_WITH_RC4_128_MD5",
        openssl_name=None,
        gnutls_name="TLS_DH_ANON_ARCFOUR_128_MD5",
        code=(0x00, 0x18),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.MD5,
        ),
    )
    DH_anon_EXPORT_WITH_DES40_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4346,
        iana_name="TLS_DH_anon_EXPORT_WITH_DES40_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x19),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.DES_40_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_anon_WITH_DES_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5469,
        iana_name="TLS_DH_anon_WITH_DES_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x1A),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.DES_56_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_anon_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_anon_WITH_3DES_EDE_CBC_SHA",
        openssl_name="ADH-DES-CBC3-SHA",
        gnutls_name="TLS_DH_ANON_3DES_EDE_CBC_SHA1",
        code=(0x00, 0x1B),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    KRB5_WITH_DES_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_WITH_DES_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x1E),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.DES_56_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    KRB5_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_WITH_3DES_EDE_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x1F),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    KRB5_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x20),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    KRB5_WITH_IDEA_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_WITH_IDEA_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x21),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.IDEA_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    KRB5_WITH_DES_CBC_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_WITH_DES_CBC_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x22),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.DES_56_CBC,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.MD5,
        ),
    )
    KRB5_WITH_3DES_EDE_CBC_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_WITH_3DES_EDE_CBC_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x23),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.MD5,
        ),
    )
    KRB5_WITH_RC4_128_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_WITH_RC4_128_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x24),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.MD5,
        ),
    )
    KRB5_WITH_IDEA_CBC_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_WITH_IDEA_CBC_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x25),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.IDEA_CBC,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.MD5,
        ),
    )
    KRB5_EXPORT_WITH_DES_CBC_40_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_EXPORT_WITH_DES_CBC_40_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x26),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.DES_40_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.SHA,
        ),
    )
    KRB5_EXPORT_WITH_RC2_CBC_40_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_EXPORT_WITH_RC2_CBC_40_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x27),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.RC2_40_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.RC2,
            SSLSuiteVuln.SHA,
        ),
    )
    KRB5_EXPORT_WITH_RC4_40_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_EXPORT_WITH_RC4_40_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x28),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.RC4_40,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    KRB5_EXPORT_WITH_DES_CBC_40_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_EXPORT_WITH_DES_CBC_40_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x29),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.DES_40_CBC,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.MD5,
        ),
    )
    KRB5_EXPORT_WITH_RC2_CBC_40_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_EXPORT_WITH_RC2_CBC_40_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x2A),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.RC2_40_CBC,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.RC2,
            SSLSuiteVuln.MD5,
        ),
    )
    KRB5_EXPORT_WITH_RC4_40_MD5: SSLSuiteInfo = SSLSuiteInfo(
        rfc=2712,
        iana_name="TLS_KRB5_EXPORT_WITH_RC4_40_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x2B),
        key_exchange=SSLKeyExchange.KRB_5,
        authentication=SSLAuthentication.KRB_5,
        encryption=SSLEncryption.RC4_40,
        ssl_hash=SSLHash.MD5,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.MD5,
        ),
    )
    PSK_WITH_NULL_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4785,
        iana_name="TLS_PSK_WITH_NULL_SHA",
        openssl_name="PSK-NULL-SHA",
        gnutls_name="TLS_PSK_NULL_SHA1",
        code=(0x00, 0x2C),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_PSK_WITH_NULL_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4785,
        iana_name="TLS_DHE_PSK_WITH_NULL_SHA",
        openssl_name="DHE-PSK-NULL-SHA",
        gnutls_name="TLS_DHE_PSK_NULL_SHA1",
        code=(0x00, 0x2D),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_PSK_WITH_NULL_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4785,
        iana_name="TLS_RSA_PSK_WITH_NULL_SHA",
        openssl_name="RSA-PSK-NULL-SHA",
        gnutls_name="TLS_RSA_PSK_NULL_SHA1",
        code=(0x00, 0x2E),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_RSA_WITH_AES_128_CBC_SHA",
        openssl_name="AES128-SHA",
        gnutls_name="TLS_RSA_AES_128_CBC_SHA1",
        code=(0x00, 0x2F),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_DSS_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_DSS_WITH_AES_128_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x30),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_RSA_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_RSA_WITH_AES_128_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x31),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_DSS_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DHE_DSS_WITH_AES_128_CBC_SHA",
        openssl_name="DHE-DSS-AES128-SHA",
        gnutls_name="TLS_DHE_DSS_AES_128_CBC_SHA1",
        code=(0x00, 0x32),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_RSA_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DHE_RSA_WITH_AES_128_CBC_SHA",
        openssl_name="DHE-RSA-AES128-SHA",
        gnutls_name="TLS_DHE_RSA_AES_128_CBC_SHA1",
        code=(0x00, 0x33),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_anon_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_anon_WITH_AES_128_CBC_SHA",
        openssl_name="ADH-AES128-SHA",
        gnutls_name="TLS_DH_ANON_AES_128_CBC_SHA1",
        code=(0x00, 0x34),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_RSA_WITH_AES_256_CBC_SHA",
        openssl_name="AES256-SHA",
        gnutls_name="TLS_RSA_AES_256_CBC_SHA1",
        code=(0x00, 0x35),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_DSS_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_DSS_WITH_AES_256_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x36),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_RSA_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_RSA_WITH_AES_256_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x37),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_DSS_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DHE_DSS_WITH_AES_256_CBC_SHA",
        openssl_name="DHE-DSS-AES256-SHA",
        gnutls_name="TLS_DHE_DSS_AES_256_CBC_SHA1",
        code=(0x00, 0x38),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_RSA_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DHE_RSA_WITH_AES_256_CBC_SHA",
        openssl_name="DHE-RSA-AES256-SHA",
        gnutls_name="TLS_DHE_RSA_AES_256_CBC_SHA1",
        code=(0x00, 0x39),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_anon_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_anon_WITH_AES_256_CBC_SHA",
        openssl_name="ADH-AES256-SHA",
        gnutls_name="TLS_DH_ANON_AES_256_CBC_SHA1",
        code=(0x00, 0x3A),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_WITH_NULL_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_RSA_WITH_NULL_SHA256",
        openssl_name="NULL-SHA256",
        gnutls_name="TLS_RSA_NULL_SHA256",
        code=(0x00, 0x3B),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
        ),
    )
    RSA_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_RSA_WITH_AES_128_CBC_SHA256",
        openssl_name="AES128-SHA256",
        gnutls_name="TLS_RSA_AES_128_CBC_SHA256",
        code=(0x00, 0x3C),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    RSA_WITH_AES_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_RSA_WITH_AES_256_CBC_SHA256",
        openssl_name="AES256-SHA256",
        gnutls_name="TLS_RSA_AES_256_CBC_SHA256",
        code=(0x00, 0x3D),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_DSS_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_DSS_WITH_AES_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x3E),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_RSA_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_RSA_WITH_AES_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x3F),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DHE_DSS_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DHE_DSS_WITH_AES_128_CBC_SHA256",
        openssl_name="DHE-DSS-AES128-SHA256",
        gnutls_name="TLS_DHE_DSS_AES_128_CBC_SHA256",
        code=(0x00, 0x40),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    RSA_WITH_CAMELLIA_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_RSA_WITH_CAMELLIA_128_CBC_SHA",
        openssl_name="CAMELLIA128-SHA",
        gnutls_name="TLS_RSA_CAMELLIA_128_CBC_SHA1",
        code=(0x00, 0x41),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_DSS_WITH_CAMELLIA_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x42),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_RSA_WITH_CAMELLIA_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x43),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_DSS_WITH_CAMELLIA_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA",
        openssl_name="DHE-DSS-CAMELLIA128-SHA",
        gnutls_name="TLS_DHE_DSS_CAMELLIA_128_CBC_SHA1",
        code=(0x00, 0x44),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_RSA_WITH_CAMELLIA_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA",
        openssl_name="DHE-RSA-CAMELLIA128-SHA",
        gnutls_name="TLS_DHE_RSA_CAMELLIA_128_CBC_SHA1",
        code=(0x00, 0x45),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_anon_WITH_CAMELLIA_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA",
        openssl_name="ADH-CAMELLIA128-SHA",
        gnutls_name="TLS_DH_ANON_CAMELLIA_128_CBC_SHA1",
        code=(0x00, 0x46),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_RSA_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DHE_RSA_WITH_AES_128_CBC_SHA256",
        openssl_name="DHE-RSA-AES128-SHA256",
        gnutls_name="TLS_DHE_RSA_AES_128_CBC_SHA256",
        code=(0x00, 0x67),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DH_DSS_WITH_AES_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_DSS_WITH_AES_256_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x68),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_RSA_WITH_AES_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_RSA_WITH_AES_256_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x69),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DHE_DSS_WITH_AES_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DHE_DSS_WITH_AES_256_CBC_SHA256",
        openssl_name="DHE-DSS-AES256-SHA256",
        gnutls_name="TLS_DHE_DSS_AES_256_CBC_SHA256",
        code=(0x00, 0x6A),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DHE_RSA_WITH_AES_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DHE_RSA_WITH_AES_256_CBC_SHA256",
        openssl_name="DHE-RSA-AES256-SHA256",
        gnutls_name="TLS_DHE_RSA_AES_256_CBC_SHA256",
        code=(0x00, 0x6B),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DH_anon_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_anon_WITH_AES_128_CBC_SHA256",
        openssl_name="ADH-AES128-SHA256",
        gnutls_name="TLS_DH_ANON_AES_128_CBC_SHA256",
        code=(0x00, 0x6C),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_anon_WITH_AES_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5246,
        iana_name="TLS_DH_anon_WITH_AES_256_CBC_SHA256",
        openssl_name="ADH-AES256-SHA256",
        gnutls_name="TLS_DH_ANON_AES_256_CBC_SHA256",
        code=(0x00, 0x6D),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
        ),
    )
    RSA_WITH_CAMELLIA_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_RSA_WITH_CAMELLIA_256_CBC_SHA",
        openssl_name="CAMELLIA256-SHA",
        gnutls_name="TLS_RSA_CAMELLIA_256_CBC_SHA1",
        code=(0x00, 0x84),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_DSS_WITH_CAMELLIA_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x85),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_RSA_WITH_CAMELLIA_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x86),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_DSS_WITH_CAMELLIA_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA",
        openssl_name="DHE-DSS-CAMELLIA256-SHA",
        gnutls_name="TLS_DHE_DSS_CAMELLIA_256_CBC_SHA1",
        code=(0x00, 0x87),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_RSA_WITH_CAMELLIA_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA",
        openssl_name="DHE-RSA-CAMELLIA256-SHA",
        gnutls_name="TLS_DHE_RSA_CAMELLIA_256_CBC_SHA1",
        code=(0x00, 0x88),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_anon_WITH_CAMELLIA_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA",
        openssl_name="ADH-CAMELLIA256-SHA",
        gnutls_name="TLS_DH_ANON_CAMELLIA_256_CBC_SHA1",
        code=(0x00, 0x89),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    PSK_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_PSK_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name="TLS_PSK_ARCFOUR_128_SHA1",
        code=(0x00, 0x8A),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    PSK_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_PSK_WITH_3DES_EDE_CBC_SHA",
        openssl_name="PSK-3DES-EDE-CBC-SHA",
        gnutls_name="TLS_PSK_3DES_EDE_CBC_SHA1",
        code=(0x00, 0x8B),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    PSK_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_PSK_WITH_AES_128_CBC_SHA",
        openssl_name="PSK-AES128-CBC-SHA",
        gnutls_name="TLS_PSK_AES_128_CBC_SHA1",
        code=(0x00, 0x8C),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    PSK_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_PSK_WITH_AES_256_CBC_SHA",
        openssl_name="PSK-AES256-CBC-SHA",
        gnutls_name="TLS_PSK_AES_256_CBC_SHA1",
        code=(0x00, 0x8D),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_PSK_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_DHE_PSK_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name="TLS_DHE_PSK_ARCFOUR_128_SHA1",
        code=(0x00, 0x8E),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_PSK_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_DHE_PSK_WITH_3DES_EDE_CBC_SHA",
        openssl_name="DHE-PSK-3DES-EDE-CBC-SHA",
        gnutls_name="TLS_DHE_PSK_3DES_EDE_CBC_SHA1",
        code=(0x00, 0x8F),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_PSK_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_DHE_PSK_WITH_AES_128_CBC_SHA",
        openssl_name="DHE-PSK-AES128-CBC-SHA",
        gnutls_name="TLS_DHE_PSK_AES_128_CBC_SHA1",
        code=(0x00, 0x90),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_PSK_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_DHE_PSK_WITH_AES_256_CBC_SHA",
        openssl_name="DHE-PSK-AES256-CBC-SHA",
        gnutls_name="TLS_DHE_PSK_AES_256_CBC_SHA1",
        code=(0x00, 0x91),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_PSK_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_RSA_PSK_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name="TLS_RSA_PSK_ARCFOUR_128_SHA1",
        code=(0x00, 0x92),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_PSK_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_RSA_PSK_WITH_3DES_EDE_CBC_SHA",
        openssl_name="RSA-PSK-3DES-EDE-CBC-SHA",
        gnutls_name="TLS_RSA_PSK_3DES_EDE_CBC_SHA1",
        code=(0x00, 0x93),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_PSK_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_RSA_PSK_WITH_AES_128_CBC_SHA",
        openssl_name="RSA-PSK-AES128-CBC-SHA",
        gnutls_name="TLS_RSA_PSK_AES_128_CBC_SHA1",
        code=(0x00, 0x94),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_PSK_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4279,
        iana_name="TLS_RSA_PSK_WITH_AES_256_CBC_SHA",
        openssl_name="RSA-PSK-AES256-CBC-SHA",
        gnutls_name="TLS_RSA_PSK_AES_256_CBC_SHA1",
        code=(0x00, 0x95),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_WITH_SEED_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4162,
        iana_name="TLS_RSA_WITH_SEED_CBC_SHA",
        openssl_name="SEED-SHA",
        gnutls_name=None,
        code=(0x00, 0x96),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.SEED_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_DSS_WITH_SEED_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4162,
        iana_name="TLS_DH_DSS_WITH_SEED_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x97),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.SEED_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_RSA_WITH_SEED_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4162,
        iana_name="TLS_DH_RSA_WITH_SEED_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x98),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.SEED_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_DSS_WITH_SEED_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4162,
        iana_name="TLS_DHE_DSS_WITH_SEED_CBC_SHA",
        openssl_name="DHE-DSS-SEED-SHA",
        gnutls_name=None,
        code=(0x00, 0x99),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.SEED_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DHE_RSA_WITH_SEED_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4162,
        iana_name="TLS_DHE_RSA_WITH_SEED_CBC_SHA",
        openssl_name="DHE-RSA-SEED-SHA",
        gnutls_name=None,
        code=(0x00, 0x9A),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.SEED_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    DH_anon_WITH_SEED_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=4162,
        iana_name="TLS_DH_anon_WITH_SEED_CBC_SHA",
        openssl_name="ADH-SEED-SHA",
        gnutls_name=None,
        code=(0x00, 0x9B),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.SEED_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    RSA_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_RSA_WITH_AES_128_GCM_SHA256",
        openssl_name="AES128-GCM-SHA256",
        gnutls_name="TLS_RSA_AES_128_GCM_SHA256",
        code=(0x00, 0x9C),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    RSA_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_RSA_WITH_AES_256_GCM_SHA384",
        openssl_name="AES256-GCM-SHA384",
        gnutls_name="TLS_RSA_AES_256_GCM_SHA384",
        code=(0x00, 0x9D),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_RSA_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
        openssl_name="DHE-RSA-AES128-GCM-SHA256",
        gnutls_name="TLS_DHE_RSA_AES_128_GCM_SHA256",
        code=(0x00, 0x9E),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_RSA_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
        openssl_name="DHE-RSA-AES256-GCM-SHA384",
        gnutls_name="TLS_DHE_RSA_AES_256_GCM_SHA384",
        code=(0x00, 0x9F),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DH_RSA_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_DH_RSA_WITH_AES_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xA0),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DH_RSA_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_DH_RSA_WITH_AES_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xA1),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_DSS_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_DHE_DSS_WITH_AES_128_GCM_SHA256",
        openssl_name="DHE-DSS-AES128-GCM-SHA256",
        gnutls_name="TLS_DHE_DSS_AES_128_GCM_SHA256",
        code=(0x00, 0xA2),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_DSS_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_DHE_DSS_WITH_AES_256_GCM_SHA384",
        openssl_name="DHE-DSS-AES256-GCM-SHA384",
        gnutls_name="TLS_DHE_DSS_AES_256_GCM_SHA384",
        code=(0x00, 0xA3),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DH_DSS_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_DH_DSS_WITH_AES_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xA4),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DH_DSS_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_DH_DSS_WITH_AES_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xA5),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DH_anon_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_DH_anon_WITH_AES_128_GCM_SHA256",
        openssl_name="ADH-AES128-GCM-SHA256",
        gnutls_name="TLS_DH_ANON_AES_128_GCM_SHA256",
        code=(0x00, 0xA6),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
        ),
    )
    DH_anon_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5288,
        iana_name="TLS_DH_anon_WITH_AES_256_GCM_SHA384",
        openssl_name="ADH-AES256-GCM-SHA384",
        gnutls_name="TLS_DH_ANON_AES_256_GCM_SHA384",
        code=(0x00, 0xA7),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
        ),
    )
    PSK_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_PSK_WITH_AES_128_GCM_SHA256",
        openssl_name="PSK-AES128-GCM-SHA256",
        gnutls_name="TLS_PSK_AES_128_GCM_SHA256",
        code=(0x00, 0xA8),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_PSK_WITH_AES_256_GCM_SHA384",
        openssl_name="PSK-AES256-GCM-SHA384",
        gnutls_name="TLS_PSK_AES_256_GCM_SHA384",
        code=(0x00, 0xA9),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_PSK_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_DHE_PSK_WITH_AES_128_GCM_SHA256",
        openssl_name="DHE-PSK-AES128-GCM-SHA256",
        gnutls_name="TLS_DHE_PSK_AES_128_GCM_SHA256",
        code=(0x00, 0xAA),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_PSK_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_DHE_PSK_WITH_AES_256_GCM_SHA384",
        openssl_name="DHE-PSK-AES256-GCM-SHA384",
        gnutls_name="TLS_DHE_PSK_AES_256_GCM_SHA384",
        code=(0x00, 0xAB),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    RSA_PSK_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_RSA_PSK_WITH_AES_128_GCM_SHA256",
        openssl_name="RSA-PSK-AES128-GCM-SHA256",
        gnutls_name="TLS_RSA_PSK_AES_128_GCM_SHA256",
        code=(0x00, 0xAC),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    RSA_PSK_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_RSA_PSK_WITH_AES_256_GCM_SHA384",
        openssl_name="RSA-PSK-AES256-GCM-SHA384",
        gnutls_name="TLS_RSA_PSK_AES_256_GCM_SHA384",
        code=(0x00, 0xAD),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_PSK_WITH_AES_128_CBC_SHA256",
        openssl_name="PSK-AES128-CBC-SHA256",
        gnutls_name="TLS_PSK_AES_128_CBC_SHA256",
        code=(0x00, 0xAE),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    PSK_WITH_AES_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_PSK_WITH_AES_256_CBC_SHA384",
        openssl_name="PSK-AES256-CBC-SHA384",
        gnutls_name="TLS_PSK_AES_256_CBC_SHA384",
        code=(0x00, 0xAF),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    PSK_WITH_NULL_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_PSK_WITH_NULL_SHA256",
        openssl_name="PSK-NULL-SHA256",
        gnutls_name="TLS_PSK_NULL_SHA256",
        code=(0x00, 0xB0),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
        ),
    )
    PSK_WITH_NULL_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_PSK_WITH_NULL_SHA384",
        openssl_name="PSK-NULL-SHA384",
        gnutls_name="TLS_PSK_NULL_SHA384",
        code=(0x00, 0xB1),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
        ),
    )
    DHE_PSK_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_DHE_PSK_WITH_AES_128_CBC_SHA256",
        openssl_name="DHE-PSK-AES128-CBC-SHA256",
        gnutls_name="TLS_DHE_PSK_AES_128_CBC_SHA256",
        code=(0x00, 0xB2),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DHE_PSK_WITH_AES_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_DHE_PSK_WITH_AES_256_CBC_SHA384",
        openssl_name="DHE-PSK-AES256-CBC-SHA384",
        gnutls_name="TLS_DHE_PSK_AES_256_CBC_SHA384",
        code=(0x00, 0xB3),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DHE_PSK_WITH_NULL_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_DHE_PSK_WITH_NULL_SHA256",
        openssl_name="DHE-PSK-NULL-SHA256",
        gnutls_name="TLS_DHE_PSK_NULL_SHA256",
        code=(0x00, 0xB4),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.NULL_ENCRYPTION,),
    )
    DHE_PSK_WITH_NULL_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_DHE_PSK_WITH_NULL_SHA384",
        openssl_name="DHE-PSK-NULL-SHA384",
        gnutls_name="TLS_DHE_PSK_NULL_SHA384",
        code=(0x00, 0xB5),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.NULL_ENCRYPTION,),
    )
    RSA_PSK_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_RSA_PSK_WITH_AES_128_CBC_SHA256",
        openssl_name="RSA-PSK-AES128-CBC-SHA256",
        gnutls_name="TLS_RSA_PSK_AES_128_CBC_SHA256",
        code=(0x00, 0xB6),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    RSA_PSK_WITH_AES_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_RSA_PSK_WITH_AES_256_CBC_SHA384",
        openssl_name="RSA-PSK-AES256-CBC-SHA384",
        gnutls_name="TLS_RSA_PSK_AES_256_CBC_SHA384",
        code=(0x00, 0xB7),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    RSA_PSK_WITH_NULL_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_RSA_PSK_WITH_NULL_SHA256",
        openssl_name="RSA-PSK-NULL-SHA256",
        gnutls_name="TLS_RSA_PSK_NULL_SHA256",
        code=(0x00, 0xB8),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
        ),
    )
    RSA_PSK_WITH_NULL_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5487,
        iana_name="TLS_RSA_PSK_WITH_NULL_SHA384",
        openssl_name="RSA-PSK-NULL-SHA384",
        gnutls_name="TLS_RSA_PSK_NULL_SHA384",
        code=(0x00, 0xB9),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
        ),
    )
    RSA_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name="CAMELLIA128-SHA256",
        gnutls_name="TLS_RSA_CAMELLIA_128_CBC_SHA256",
        code=(0x00, 0xBA),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_DSS_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xBB),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_RSA_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xBC),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name="DHE-DSS-CAMELLIA128-SHA256",
        gnutls_name="TLS_DHE_DSS_CAMELLIA_128_CBC_SHA256",
        code=(0x00, 0xBD),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name="DHE-RSA-CAMELLIA128-SHA256",
        gnutls_name="TLS_DHE_RSA_CAMELLIA_128_CBC_SHA256",
        code=(0x00, 0xBE),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DH_anon_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name="ADH-CAMELLIA128-SHA256",
        gnutls_name="TLS_DH_ANON_CAMELLIA_128_CBC_SHA256",
        code=(0x00, 0xBF),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
        ),
    )
    RSA_WITH_CAMELLIA_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256",
        openssl_name="CAMELLIA256-SHA256",
        gnutls_name="TLS_RSA_CAMELLIA_256_CBC_SHA256",
        code=(0x00, 0xC0),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_DSS_WITH_CAMELLIA_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xC1),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_RSA_WITH_CAMELLIA_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xC2),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256",
        openssl_name="DHE-DSS-CAMELLIA256-SHA256",
        gnutls_name="TLS_DHE_DSS_CAMELLIA_256_CBC_SHA256",
        code=(0x00, 0xC3),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256",
        openssl_name="DHE-RSA-CAMELLIA256-SHA256",
        gnutls_name="TLS_DHE_RSA_CAMELLIA_256_CBC_SHA256",
        code=(0x00, 0xC4),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DH_anon_WITH_CAMELLIA_256_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5932,
        iana_name="TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA256",
        openssl_name="ADH-CAMELLIA256-SHA256",
        gnutls_name="TLS_DH_ANON_CAMELLIA_256_CBC_SHA256",
        code=(0x00, 0xC5),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
        ),
    )
    SM4_GCM_SM3: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8998,
        iana_name="TLS_SM4_GCM_SM3",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xC6),
        key_exchange=SSLKeyExchange.NONE,
        authentication=SSLAuthentication.NONE,
        encryption=SSLEncryption.SM_4_GCM,
        ssl_hash=SSLHash.SM3,
        tls_versions=(SSLVersionId.tlsv1_3,),
        vulnerabilities=(
            SSLSuiteVuln.SM4,
            SSLSuiteVuln.SM3,
        ),
    )
    SM4_CCM_SM3: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8998,
        iana_name="TLS_SM4_CCM_SM3",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xC7),
        key_exchange=SSLKeyExchange.NONE,
        authentication=SSLAuthentication.NONE,
        encryption=SSLEncryption.SM_4_CCM,
        ssl_hash=SSLHash.SM3,
        tls_versions=(SSLVersionId.tlsv1_3,),
        vulnerabilities=(
            SSLSuiteVuln.SM4,
            SSLSuiteVuln.SM3,
        ),
    )
    AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8446,
        iana_name="TLS_AES_128_GCM_SHA256",
        openssl_name="TLS_AES_128_GCM_SHA256",
        gnutls_name=None,
        code=(0x13, 0x01),
        key_exchange=SSLKeyExchange.NONE,
        authentication=SSLAuthentication.NONE,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_3,),
        vulnerabilities=(),
    )
    AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8446,
        iana_name="TLS_AES_256_GCM_SHA384",
        openssl_name="TLS_AES_256_GCM_SHA384",
        gnutls_name=None,
        code=(0x13, 0x02),
        key_exchange=SSLKeyExchange.NONE,
        authentication=SSLAuthentication.NONE,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_3,),
        vulnerabilities=(),
    )
    CHACHA20_POLY1305_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8446,
        iana_name="TLS_CHACHA20_POLY1305_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x13, 0x03),
        key_exchange=SSLKeyExchange.NONE,
        authentication=SSLAuthentication.NONE,
        encryption=SSLEncryption.CHACHA_20_POLY_1305,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_3,),
        vulnerabilities=(),
    )
    AES_128_CCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8446,
        iana_name="TLS_AES_128_CCM_SHA256",
        openssl_name="TLS_AES_128_CCM_SHA256",
        gnutls_name=None,
        code=(0x13, 0x04),
        key_exchange=SSLKeyExchange.NONE,
        authentication=SSLAuthentication.NONE,
        encryption=SSLEncryption.AES_128_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_3,),
        vulnerabilities=(),
    )
    AES_128_CCM_8_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8446,
        iana_name="TLS_AES_128_CCM_8_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0x13, 0x05),
        key_exchange=SSLKeyExchange.NONE,
        authentication=SSLAuthentication.NONE,
        encryption=SSLEncryption.AES_128_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_3,),
        vulnerabilities=(),
    )
    ECDH_ECDSA_WITH_NULL_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_ECDSA_WITH_NULL_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x01),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_ECDSA_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_ECDSA_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x02),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x03),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_ECDSA_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x04),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_ECDSA_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x05),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_ECDSA_WITH_NULL_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDHE_ECDSA_WITH_NULL_SHA",
        openssl_name="ECDHE-ECDSA-NULL-SHA",
        gnutls_name="TLS_ECDHE_ECDSA_NULL_SHA1",
        code=(0xC0, 0x06),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_ECDSA_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDHE_ECDSA_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name="TLS_ECDHE_ECDSA_ARCFOUR_128_SHA1",
        code=(0xC0, 0x07),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA",
        openssl_name="ECDHE-ECDSA-DES-CBC3-SHA",
        gnutls_name="TLS_ECDHE_ECDSA_3DES_EDE_CBC_SHA1",
        code=(0xC0, 0x08),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_ECDSA_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
        openssl_name="ECDHE-ECDSA-AES128-SHA",
        gnutls_name="TLS_ECDHE_ECDSA_AES_128_CBC_SHA1",
        code=(0xC0, 0x09),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_ECDSA_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
        openssl_name="ECDHE-ECDSA-AES256-SHA",
        gnutls_name="TLS_ECDHE_ECDSA_AES_256_CBC_SHA1",
        code=(0xC0, 0x0A),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_RSA_WITH_NULL_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_RSA_WITH_NULL_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x0B),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_RSA_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_RSA_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x0C),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_RSA_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x0D),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_RSA_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_RSA_WITH_AES_128_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x0E),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_RSA_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_RSA_WITH_AES_256_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x0F),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_RSA_WITH_NULL_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDHE_RSA_WITH_NULL_SHA",
        openssl_name="ECDHE-RSA-NULL-SHA",
        gnutls_name="TLS_ECDHE_RSA_NULL_SHA1",
        code=(0xC0, 0x10),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_RSA_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDHE_RSA_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name="TLS_ECDHE_RSA_ARCFOUR_128_SHA1",
        code=(0xC0, 0x11),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_RSA_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA",
        openssl_name="ECDHE-RSA-DES-CBC3-SHA",
        gnutls_name="TLS_ECDHE_RSA_3DES_EDE_CBC_SHA1",
        code=(0xC0, 0x12),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_RSA_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",
        openssl_name="ECDHE-RSA-AES128-SHA",
        gnutls_name="TLS_ECDHE_RSA_AES_128_CBC_SHA1",
        code=(0xC0, 0x13),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_RSA_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
        openssl_name="ECDHE-RSA-AES256-SHA",
        gnutls_name="TLS_ECDHE_RSA_AES_256_CBC_SHA1",
        code=(0xC0, 0x14),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_anon_WITH_NULL_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_anon_WITH_NULL_SHA",
        openssl_name="AECDH-NULL-SHA",
        gnutls_name="TLS_ECDH_ANON_NULL_SHA1",
        code=(0xC0, 0x15),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_anon_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_anon_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name="TLS_ECDH_ANON_ARCFOUR_128_SHA1",
        code=(0xC0, 0x16),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_anon_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_anon_WITH_3DES_EDE_CBC_SHA",
        openssl_name="AECDH-DES-CBC3-SHA",
        gnutls_name="TLS_ECDH_ANON_3DES_EDE_CBC_SHA1",
        code=(0xC0, 0x17),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_anon_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_anon_WITH_AES_128_CBC_SHA",
        openssl_name="AECDH-AES128-SHA",
        gnutls_name="TLS_ECDH_ANON_AES_128_CBC_SHA1",
        code=(0xC0, 0x18),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDH_anon_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8422,
        iana_name="TLS_ECDH_anon_WITH_AES_256_CBC_SHA",
        openssl_name="AECDH-AES256-SHA",
        gnutls_name="TLS_ECDH_ANON_AES_256_CBC_SHA1",
        code=(0xC0, 0x19),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    SRP_SHA_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5054,
        iana_name="TLS_SRP_SHA_WITH_3DES_EDE_CBC_SHA",
        openssl_name="SRP-3DES-EDE-CBC-SHA",
        gnutls_name="TLS_SRP_SHA_3DES_EDE_CBC_SHA1",
        code=(0xC0, 0x1A),
        key_exchange=SSLKeyExchange.SRP,
        authentication=SSLAuthentication.SHA,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5054,
        iana_name="TLS_SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA",
        openssl_name="SRP-RSA-3DES-EDE-CBC-SHA",
        gnutls_name="TLS_SRP_SHA_RSA_3DES_EDE_CBC_SHA1",
        code=(0xC0, 0x1B),
        key_exchange=SSLKeyExchange.SRP,
        authentication=SSLAuthentication.SHA_RSA,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5054,
        iana_name="TLS_SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA",
        openssl_name="SRP-DSS-3DES-EDE-CBC-SHA",
        gnutls_name="TLS_SRP_SHA_DSS_3DES_EDE_CBC_SHA1",
        code=(0xC0, 0x1C),
        key_exchange=SSLKeyExchange.SRP,
        authentication=SSLAuthentication.SHA_DSS,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    SRP_SHA_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5054,
        iana_name="TLS_SRP_SHA_WITH_AES_128_CBC_SHA",
        openssl_name="SRP-AES-128-CBC-SHA",
        gnutls_name="TLS_SRP_SHA_AES_128_CBC_SHA1",
        code=(0xC0, 0x1D),
        key_exchange=SSLKeyExchange.SRP,
        authentication=SSLAuthentication.SHA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    SRP_SHA_RSA_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5054,
        iana_name="TLS_SRP_SHA_RSA_WITH_AES_128_CBC_SHA",
        openssl_name="SRP-RSA-AES-128-CBC-SHA",
        gnutls_name="TLS_SRP_SHA_RSA_AES_128_CBC_SHA1",
        code=(0xC0, 0x1E),
        key_exchange=SSLKeyExchange.SRP,
        authentication=SSLAuthentication.SHA_RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    SRP_SHA_DSS_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5054,
        iana_name="TLS_SRP_SHA_DSS_WITH_AES_128_CBC_SHA",
        openssl_name="SRP-DSS-AES-128-CBC-SHA",
        gnutls_name="TLS_SRP_SHA_DSS_AES_128_CBC_SHA1",
        code=(0xC0, 0x1F),
        key_exchange=SSLKeyExchange.SRP,
        authentication=SSLAuthentication.SHA_DSS,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    SRP_SHA_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5054,
        iana_name="TLS_SRP_SHA_WITH_AES_256_CBC_SHA",
        openssl_name="SRP-AES-256-CBC-SHA",
        gnutls_name="TLS_SRP_SHA_AES_256_CBC_SHA1",
        code=(0xC0, 0x20),
        key_exchange=SSLKeyExchange.SRP,
        authentication=SSLAuthentication.SHA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    SRP_SHA_RSA_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5054,
        iana_name="TLS_SRP_SHA_RSA_WITH_AES_256_CBC_SHA",
        openssl_name="SRP-RSA-AES-256-CBC-SHA",
        gnutls_name="TLS_SRP_SHA_RSA_AES_256_CBC_SHA1",
        code=(0xC0, 0x21),
        key_exchange=SSLKeyExchange.SRP,
        authentication=SSLAuthentication.SHA_RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    SRP_SHA_DSS_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5054,
        iana_name="TLS_SRP_SHA_DSS_WITH_AES_256_CBC_SHA",
        openssl_name="SRP-DSS-AES-256-CBC-SHA",
        gnutls_name="TLS_SRP_SHA_DSS_AES_256_CBC_SHA1",
        code=(0xC0, 0x22),
        key_exchange=SSLKeyExchange.SRP,
        authentication=SSLAuthentication.SHA_DSS,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_ECDSA_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
        openssl_name="ECDHE-ECDSA-AES128-SHA256",
        gnutls_name="TLS_ECDHE_ECDSA_AES_128_CBC_SHA256",
        code=(0xC0, 0x23),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_ECDSA_WITH_AES_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
        openssl_name="ECDHE-ECDSA-AES256-SHA384",
        gnutls_name="TLS_ECDHE_ECDSA_AES_256_CBC_SHA384",
        code=(0xC0, 0x24),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDH_ECDSA_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x25),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDH_ECDSA_WITH_AES_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x26),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDHE_RSA_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
        openssl_name="ECDHE-RSA-AES128-SHA256",
        gnutls_name="TLS_ECDHE_RSA_AES_128_CBC_SHA256",
        code=(0xC0, 0x27),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_RSA_WITH_AES_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
        openssl_name="ECDHE-RSA-AES256-SHA384",
        gnutls_name="TLS_ECDHE_RSA_AES_256_CBC_SHA384",
        code=(0xC0, 0x28),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDH_RSA_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x29),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDH_RSA_WITH_AES_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x2A),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDHE_ECDSA_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
        openssl_name="ECDHE-ECDSA-AES128-GCM-SHA256",
        gnutls_name="TLS_ECDHE_ECDSA_AES_128_GCM_SHA256",
        code=(0xC0, 0x2B),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_ECDSA_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
        openssl_name="ECDHE-ECDSA-AES256-GCM-SHA384",
        gnutls_name="TLS_ECDHE_ECDSA_AES_256_GCM_SHA384",
        code=(0xC0, 0x2C),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDH_ECDSA_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x2D),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDH_ECDSA_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x2E),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDHE_RSA_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        openssl_name="ECDHE-RSA-AES128-GCM-SHA256",
        gnutls_name="TLS_ECDHE_RSA_AES_128_GCM_SHA256",
        code=(0xC0, 0x2F),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_RSA_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
        openssl_name="ECDHE-RSA-AES256-GCM-SHA384",
        gnutls_name="TLS_ECDHE_RSA_AES_256_GCM_SHA384",
        code=(0xC0, 0x30),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDH_RSA_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x31),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDH_RSA_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5289,
        iana_name="TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x32),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDHE_PSK_WITH_RC4_128_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5489,
        iana_name="TLS_ECDHE_PSK_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name="TLS_ECDHE_PSK_ARCFOUR_128_SHA1",
        code=(0xC0, 0x33),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_PSK_WITH_3DES_EDE_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5489,
        iana_name="TLS_ECDHE_PSK_WITH_3DES_EDE_CBC_SHA",
        openssl_name="ECDHE-PSK-3DES-EDE-CBC-SHA",
        gnutls_name="TLS_ECDHE_PSK_3DES_EDE_CBC_SHA1",
        code=(0xC0, 0x34),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.DES3_EDE_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES3,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_PSK_WITH_AES_128_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5489,
        iana_name="TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA",
        openssl_name="ECDHE-PSK-AES128-CBC-SHA",
        gnutls_name="TLS_ECDHE_PSK_AES_128_CBC_SHA1",
        code=(0xC0, 0x35),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_PSK_WITH_AES_256_CBC_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5489,
        iana_name="TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA",
        openssl_name="ECDHE-PSK-AES256-CBC-SHA",
        gnutls_name="TLS_ECDHE_PSK_AES_256_CBC_SHA1",
        code=(0xC0, 0x36),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_PSK_WITH_AES_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5489,
        iana_name="TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA256",
        openssl_name="ECDHE-PSK-AES128-CBC-SHA256",
        gnutls_name="TLS_ECDHE_PSK_AES_128_CBC_SHA256",
        code=(0xC0, 0x37),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_PSK_WITH_AES_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5489,
        iana_name="TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA384",
        openssl_name="ECDHE-PSK-AES256-CBC-SHA384",
        gnutls_name="TLS_ECDHE_PSK_AES_256_CBC_SHA384",
        code=(0xC0, 0x38),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_PSK_WITH_NULL_SHA: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5489,
        iana_name="TLS_ECDHE_PSK_WITH_NULL_SHA",
        openssl_name="ECDHE-PSK-NULL-SHA",
        gnutls_name="TLS_ECDHE_PSK_NULL_SHA1",
        code=(0xC0, 0x39),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NULL_ENCRYPTION,
            SSLSuiteVuln.SHA,
        ),
    )
    ECDHE_PSK_WITH_NULL_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5489,
        iana_name="TLS_ECDHE_PSK_WITH_NULL_SHA256",
        openssl_name="ECDHE-PSK-NULL-SHA256",
        gnutls_name="TLS_ECDHE_PSK_NULL_SHA256",
        code=(0xC0, 0x3A),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.NULL_ENCRYPTION,),
    )
    ECDHE_PSK_WITH_NULL_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5489,
        iana_name="TLS_ECDHE_PSK_WITH_NULL_SHA384",
        openssl_name="ECDHE-PSK-NULL-SHA384",
        gnutls_name="TLS_ECDHE_PSK_NULL_SHA384",
        code=(0xC0, 0x3B),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.NULL,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.NULL_ENCRYPTION,),
    )
    RSA_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_RSA_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x3C),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    RSA_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_RSA_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x3D),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_DSS_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_DSS_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x3E),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_DSS_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_DSS_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x3F),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_RSA_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_RSA_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x40),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_RSA_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_RSA_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x41),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DHE_DSS_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_DSS_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x42),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DHE_DSS_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_DSS_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x43),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DHE_RSA_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_RSA_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x44),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DHE_RSA_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_RSA_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x45),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DH_anon_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_anon_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x46),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
        ),
    )
    DH_anon_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_anon_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x47),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDHE_ECDSA_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDHE_ECDSA_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x48),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_ECDSA_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDHE_ECDSA_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x49),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDH_ECDSA_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDH_ECDSA_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x4A),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDH_ECDSA_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDH_ECDSA_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x4B),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDHE_RSA_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6269,
        iana_name="TLS_ECDHE_RSA_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x4C),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_RSA_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDHE_RSA_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x4D),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDH_RSA_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDH_RSA_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x4E),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDH_RSA_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDH_RSA_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x4F),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    RSA_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_RSA_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x50),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    RSA_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_RSA_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x51),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_RSA_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_RSA_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x52),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_RSA_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_RSA_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x53),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DH_RSA_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_RSA_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x54),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DH_RSA_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_RSA_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x55),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_DSS_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_DSS_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x56),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_DSS_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_DSS_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x57),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DH_DSS_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_DSS_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x58),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DH_DSS_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_DSS_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x59),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DH_anon_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_anon_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x5A),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
        ),
    )
    DH_anon_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DH_anon_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x5B),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
        ),
    )
    ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x5C),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_ECDSA_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDHE_ECDSA_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x5D),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDH_ECDSA_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDH_ECDSA_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x5E),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDH_ECDSA_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDH_ECDSA_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x5F),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDHE_RSA_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDHE_RSA_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x60),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_RSA_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDHE_RSA_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x61),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDH_RSA_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDH_RSA_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x62),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDH_RSA_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDH_RSA_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x63),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_PSK_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x64),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    PSK_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_PSK_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x65),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DHE_PSK_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_PSK_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x66),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DHE_PSK_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_PSK_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x67),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    RSA_PSK_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_RSA_PSK_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x68),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    RSA_PSK_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_RSA_PSK_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x69),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    PSK_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_PSK_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x6A),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_PSK_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x6B),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_PSK_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_PSK_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x6C),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_PSK_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_DHE_PSK_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x6D),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    RSA_PSK_WITH_ARIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_RSA_PSK_WITH_ARIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x6E),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    RSA_PSK_WITH_ARIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_RSA_PSK_WITH_ARIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x6F),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDHE_PSK_WITH_ARIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDHE_PSK_WITH_ARIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x70),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_PSK_WITH_ARIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6209,
        iana_name="TLS_ECDHE_PSK_WITH_ARIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x71),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.ARIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name="ECDHE-ECDSA-CAMELLIA128-SHA256",
        gnutls_name="TLS_ECDHE_ECDSA_CAMELLIA_128_CBC_SHA256",
        code=(0xC0, 0x72),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384",
        openssl_name="ECDHE-ECDSA-CAMELLIA256-SHA384",
        gnutls_name="TLS_ECDHE_ECDSA_CAMELLIA_256_CBC_SHA384",
        code=(0xC0, 0x73),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDH_ECDSA_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDH_ECDSA_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x74),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDH_ECDSA_WITH_CAMELLIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDH_ECDSA_WITH_CAMELLIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x75),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name="ECDHE-RSA-CAMELLIA128-SHA256",
        gnutls_name="TLS_ECDHE_RSA_CAMELLIA_128_CBC_SHA256",
        code=(0xC0, 0x76),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384",
        openssl_name="ECDHE-RSA-CAMELLIA256-SHA384",
        gnutls_name="TLS_ECDHE_RSA_CAMELLIA_256_CBC_SHA384",
        code=(0xC0, 0x77),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDH_RSA_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDH_RSA_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x78),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDH_RSA_WITH_CAMELLIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDH_RSA_WITH_CAMELLIA_256_CBC_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x79),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    RSA_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_RSA_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name="TLS_RSA_CAMELLIA_128_GCM_SHA256",
        code=(0xC0, 0x7A),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    RSA_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_RSA_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name="TLS_RSA_CAMELLIA_256_GCM_SHA384",
        code=(0xC0, 0x7B),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_RSA_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DHE_RSA_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name="TLS_DHE_RSA_CAMELLIA_128_GCM_SHA256",
        code=(0xC0, 0x7C),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_RSA_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DHE_RSA_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name="TLS_DHE_RSA_CAMELLIA_256_GCM_SHA384",
        code=(0xC0, 0x7D),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DH_RSA_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DH_RSA_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x7E),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DH_RSA_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DH_RSA_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x7F),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_DSS_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DHE_DSS_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name="TLS_DHE_DSS_CAMELLIA_128_GCM_SHA256",
        code=(0xC0, 0x80),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_DSS_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DHE_DSS_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name="TLS_DHE_DSS_CAMELLIA_256_GCM_SHA384",
        code=(0xC0, 0x81),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DH_DSS_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DH_DSS_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x82),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DH_DSS_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DH_DSS_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x83),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DH_anon_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DH_anon_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name="TLS_DH_ANON_CAMELLIA_128_GCM_SHA256",
        code=(0xC0, 0x84),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
        ),
    )
    DH_anon_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DH_anon_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name="TLS_DH_ANON_CAMELLIA_256_GCM_SHA384",
        code=(0xC0, 0x85),
        key_exchange=SSLKeyExchange.DH,
        authentication=SSLAuthentication.ANON,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.ANON_KEY_EXCHANGE,
        ),
    )
    ECDHE_ECDSA_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDHE_ECDSA_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name="TLS_ECDHE_ECDSA_CAMELLIA_128_GCM_SHA256",
        code=(0xC0, 0x86),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_ECDSA_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDHE_ECDSA_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name="TLS_ECDHE_ECDSA_CAMELLIA_256_GCM_SHA384",
        code=(0xC0, 0x87),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDH_ECDSA_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDH_ECDSA_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x88),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDH_ECDSA_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDH_ECDSA_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x89),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDHE_RSA_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDHE_RSA_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name="TLS_ECDHE_RSA_CAMELLIA_128_GCM_SHA256",
        code=(0xC0, 0x8A),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_RSA_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDHE_RSA_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name="TLS_ECDHE_RSA_CAMELLIA_256_GCM_SHA384",
        code=(0xC0, 0x8B),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDH_RSA_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDH_RSA_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x8C),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDH_RSA_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDH_RSA_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0x8D),
        key_exchange=SSLKeyExchange.ECDH,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_PSK_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name="TLS_PSK_CAMELLIA_128_GCM_SHA256",
        code=(0xC0, 0x8E),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_PSK_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name="TLS_PSK_CAMELLIA_256_GCM_SHA384",
        code=(0xC0, 0x8F),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_PSK_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DHE_PSK_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name="TLS_DHE_PSK_CAMELLIA_128_GCM_SHA256",
        code=(0xC0, 0x90),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_PSK_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DHE_PSK_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name="TLS_DHE_PSK_CAMELLIA_256_GCM_SHA384",
        code=(0xC0, 0x91),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    RSA_PSK_WITH_CAMELLIA_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_RSA_PSK_WITH_CAMELLIA_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name="TLS_RSA_PSK_CAMELLIA_128_GCM_SHA256",
        code=(0xC0, 0x92),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    RSA_PSK_WITH_CAMELLIA_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_RSA_PSK_WITH_CAMELLIA_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name="TLS_RSA_PSK_CAMELLIA_256_GCM_SHA384",
        code=(0xC0, 0x93),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_PSK_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name="PSK-CAMELLIA128-SHA256",
        gnutls_name="TLS_PSK_CAMELLIA_128_CBC_SHA256",
        code=(0xC0, 0x94),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    PSK_WITH_CAMELLIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_PSK_WITH_CAMELLIA_256_CBC_SHA384",
        openssl_name="PSK-CAMELLIA256-SHA384",
        gnutls_name="TLS_PSK_CAMELLIA_256_CBC_SHA384",
        code=(0xC0, 0x95),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    DHE_PSK_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DHE_PSK_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name="DHE-PSK-CAMELLIA128-SHA256",
        gnutls_name="TLS_DHE_PSK_CAMELLIA_128_CBC_SHA256",
        code=(0xC0, 0x96),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    DHE_PSK_WITH_CAMELLIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_DHE_PSK_WITH_CAMELLIA_256_CBC_SHA384",
        openssl_name="DHE-PSK-CAMELLIA256-SHA384",
        gnutls_name="TLS_DHE_PSK_CAMELLIA_256_CBC_SHA384",
        code=(0xC0, 0x97),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    RSA_PSK_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_RSA_PSK_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name="RSA-PSK-CAMELLIA128-SHA256",
        gnutls_name="TLS_RSA_PSK_CAMELLIA_128_CBC_SHA256",
        code=(0xC0, 0x98),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    RSA_PSK_WITH_CAMELLIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_RSA_PSK_WITH_CAMELLIA_256_CBC_SHA384",
        openssl_name="RSA-PSK-CAMELLIA256-SHA384",
        gnutls_name="TLS_RSA_PSK_CAMELLIA_256_CBC_SHA384",
        code=(0xC0, 0x99),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.CBC,
        ),
    )
    ECDHE_PSK_WITH_CAMELLIA_128_CBC_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDHE_PSK_WITH_CAMELLIA_128_CBC_SHA256",
        openssl_name="ECDHE-PSK-CAMELLIA128-SHA256",
        gnutls_name="TLS_ECDHE_PSK_CAMELLIA_128_CBC_SHA256",
        code=(0xC0, 0x9A),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_128_CBC,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    ECDHE_PSK_WITH_CAMELLIA_256_CBC_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6367,
        iana_name="TLS_ECDHE_PSK_WITH_CAMELLIA_256_CBC_SHA384",
        openssl_name="ECDHE-PSK-CAMELLIA256-SHA384",
        gnutls_name="TLS_ECDHE_PSK_CAMELLIA_256_CBC_SHA384",
        code=(0xC0, 0x9B),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CAMELLIA_256_CBC,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
            SSLVersionId.tlsv1_2,
        ),
        vulnerabilities=(SSLSuiteVuln.CBC,),
    )
    RSA_WITH_AES_128_CCM: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_RSA_WITH_AES_128_CCM",
        openssl_name="AES128-CCM",
        gnutls_name="TLS_RSA_AES_128_CCM",
        code=(0xC0, 0x9C),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    RSA_WITH_AES_256_CCM: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_RSA_WITH_AES_256_CCM",
        openssl_name="AES256-CCM",
        gnutls_name="TLS_RSA_AES_256_CCM",
        code=(0xC0, 0x9D),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_RSA_WITH_AES_128_CCM: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_DHE_RSA_WITH_AES_128_CCM",
        openssl_name="DHE-RSA-AES128-CCM",
        gnutls_name="TLS_DHE_RSA_AES_128_CCM",
        code=(0xC0, 0x9E),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_RSA_WITH_AES_256_CCM: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_DHE_RSA_WITH_AES_256_CCM",
        openssl_name="DHE-RSA-AES256-CCM",
        gnutls_name="TLS_DHE_RSA_AES_256_CCM",
        code=(0xC0, 0x9F),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    RSA_WITH_AES_128_CCM_8: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_RSA_WITH_AES_128_CCM_8",
        openssl_name="AES128-CCM8",
        gnutls_name="TLS_RSA_AES_128_CCM_8",
        code=(0xC0, 0xA0),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    RSA_WITH_AES_256_CCM_8: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_RSA_WITH_AES_256_CCM_8",
        openssl_name="AES256-CCM8",
        gnutls_name="TLS_RSA_AES_256_CCM_8",
        code=(0xC0, 0xA1),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_RSA_WITH_AES_128_CCM_8: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_DHE_RSA_WITH_AES_128_CCM_8",
        openssl_name="DHE-RSA-AES128-CCM8",
        gnutls_name="TLS_DHE_RSA_AES_128_CCM_8",
        code=(0xC0, 0xA2),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_128_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_RSA_WITH_AES_256_CCM_8: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_DHE_RSA_WITH_AES_256_CCM_8",
        openssl_name="DHE-RSA-AES256-CCM8",
        gnutls_name="TLS_DHE_RSA_AES_256_CCM_8",
        code=(0xC0, 0xA3),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.AES_256_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    PSK_WITH_AES_128_CCM: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_PSK_WITH_AES_128_CCM",
        openssl_name="PSK-AES128-CCM",
        gnutls_name="TLS_PSK_AES_128_CCM",
        code=(0xC0, 0xA4),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_WITH_AES_256_CCM: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_PSK_WITH_AES_256_CCM",
        openssl_name="PSK-AES256-CCM",
        gnutls_name="TLS_PSK_AES_256_CCM",
        code=(0xC0, 0xA5),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    DHE_PSK_WITH_AES_128_CCM: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_DHE_PSK_WITH_AES_128_CCM",
        openssl_name="DHE-PSK-AES128-CCM",
        gnutls_name="TLS_DHE_PSK_AES_128_CCM",
        code=(0xC0, 0xA6),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_PSK_WITH_AES_256_CCM: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_DHE_PSK_WITH_AES_256_CCM",
        openssl_name="DHE-PSK-AES256-CCM",
        gnutls_name="TLS_DHE_PSK_AES_256_CCM",
        code=(0xC0, 0xA7),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    PSK_WITH_AES_128_CCM_8: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_PSK_WITH_AES_128_CCM_8",
        openssl_name="PSK-AES128-CCM8",
        gnutls_name="TLS_PSK_AES_128_CCM_8",
        code=(0xC0, 0xA8),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_WITH_AES_256_CCM_8: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_PSK_WITH_AES_256_CCM_8",
        openssl_name="PSK-AES256-CCM8",
        gnutls_name="TLS_PSK_AES_256_CCM_8",
        code=(0xC0, 0xA9),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_DHE_WITH_AES_128_CCM_8: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_PSK_DHE_WITH_AES_128_CCM_8",
        openssl_name="DHE-PSK-AES128-CCM8",
        gnutls_name="TLS_DHE_PSK_AES_128_CCM_8",
        code=(0xC0, 0xAA),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.DHE,
        encryption=SSLEncryption.AES_128_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    PSK_DHE_WITH_AES_256_CCM_8: SSLSuiteInfo = SSLSuiteInfo(
        rfc=6655,
        iana_name="TLS_PSK_DHE_WITH_AES_256_CCM_8",
        openssl_name="DHE-PSK-AES256-CCM8",
        gnutls_name="TLS_DHE_PSK_AES_256_CCM_8",
        code=(0xC0, 0xAB),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.DHE,
        encryption=SSLEncryption.AES_256_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDHE_ECDSA_WITH_AES_128_CCM: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7251,
        iana_name="TLS_ECDHE_ECDSA_WITH_AES_128_CCM",
        openssl_name="ECDHE-ECDSA-AES128-CCM",
        gnutls_name="TLS_ECDHE_ECDSA_AES_128_CCM",
        code=(0xC0, 0xAC),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_128_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_ECDSA_WITH_AES_256_CCM: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7251,
        iana_name="TLS_ECDHE_ECDSA_WITH_AES_256_CCM",
        openssl_name="ECDHE-ECDSA-AES256-CCM",
        gnutls_name="TLS_ECDHE_ECDSA_AES_256_CCM",
        code=(0xC0, 0xAD),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_256_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_ECDSA_WITH_AES_128_CCM_8: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7251,
        iana_name="TLS_ECDHE_ECDSA_WITH_AES_128_CCM_8",
        openssl_name="ECDHE-ECDSA-AES128-CCM8",
        gnutls_name="TLS_ECDHE_ECDSA_AES_128_CCM_8",
        code=(0xC0, 0xAE),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_128_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_ECDSA_WITH_AES_256_CCM_8: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7251,
        iana_name="TLS_ECDHE_ECDSA_WITH_AES_256_CCM_8",
        openssl_name="ECDHE-ECDSA-AES256-CCM8",
        gnutls_name="TLS_ECDHE_ECDSA_AES_256_CCM_8",
        code=(0xC0, 0xAF),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.AES_256_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECCPWD_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8492,
        iana_name="TLS_ECCPWD_WITH_AES_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0xB0),
        key_exchange=SSLKeyExchange.ECCPWD,
        authentication=SSLAuthentication.ECCPWD,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECCPWD_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8492,
        iana_name="TLS_ECCPWD_WITH_AES_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0xB1),
        key_exchange=SSLKeyExchange.ECCPWD,
        authentication=SSLAuthentication.ECCPWD,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECCPWD_WITH_AES_128_CCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8492,
        iana_name="TLS_ECCPWD_WITH_AES_128_CCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0xB2),
        key_exchange=SSLKeyExchange.ECCPWD,
        authentication=SSLAuthentication.ECCPWD,
        encryption=SSLEncryption.AES_128_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECCPWD_WITH_AES_256_CCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8492,
        iana_name="TLS_ECCPWD_WITH_AES_256_CCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xC0, 0xB3),
        key_exchange=SSLKeyExchange.ECCPWD,
        authentication=SSLAuthentication.ECCPWD,
        encryption=SSLEncryption.AES_256_CCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7905,
        iana_name="TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
        openssl_name="ECDHE-RSA-CHACHA20-POLY1305",
        gnutls_name="TLS_ECDHE_RSA_CHACHA20_POLY1305",
        code=(0xCC, 0xA8),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CHACHA_20_POLY_1305,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7905,
        iana_name="TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
        openssl_name="ECDHE-ECDSA-CHACHA20-POLY1305",
        gnutls_name="TLS_ECDHE_ECDSA_CHACHA20_POLY1305",
        code=(0xCC, 0xA9),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.ECDSA,
        encryption=SSLEncryption.CHACHA_20_POLY_1305,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_RSA_WITH_CHACHA20_POLY1305_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7905,
        iana_name="TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
        openssl_name="DHE-RSA-CHACHA20-POLY1305",
        gnutls_name="TLS_DHE_RSA_CHACHA20_POLY1305",
        code=(0xCC, 0xAA),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.CHACHA_20_POLY_1305,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    PSK_WITH_CHACHA20_POLY1305_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7905,
        iana_name="TLS_PSK_WITH_CHACHA20_POLY1305_SHA256",
        openssl_name="PSK-CHACHA20-POLY1305",
        gnutls_name="TLS_PSK_CHACHA20_POLY1305",
        code=(0xCC, 0xAB),
        key_exchange=SSLKeyExchange.PSK,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CHACHA_20_POLY_1305,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDHE_PSK_WITH_CHACHA20_POLY1305_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7905,
        iana_name="TLS_ECDHE_PSK_WITH_CHACHA20_POLY1305_SHA256",
        openssl_name="ECDHE-PSK-CHACHA20-POLY1305",
        gnutls_name="TLS_ECDHE_PSK_CHACHA20_POLY1305",
        code=(0xCC, 0xAC),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CHACHA_20_POLY_1305,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    DHE_PSK_WITH_CHACHA20_POLY1305_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7905,
        iana_name="TLS_DHE_PSK_WITH_CHACHA20_POLY1305_SHA256",
        openssl_name="DHE-PSK-CHACHA20-POLY1305",
        gnutls_name="TLS_DHE_PSK_CHACHA20_POLY1305",
        code=(0xCC, 0xAD),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CHACHA_20_POLY_1305,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    RSA_PSK_WITH_CHACHA20_POLY1305_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7905,
        iana_name="TLS_RSA_PSK_WITH_CHACHA20_POLY1305_SHA256",
        openssl_name="RSA-PSK-CHACHA20-POLY1305",
        gnutls_name="TLS_RSA_PSK_CHACHA20_POLY1305",
        code=(0xCC, 0xAE),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.CHACHA_20_POLY_1305,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(SSLSuiteVuln.NO_PFS,),
    )
    ECDHE_PSK_WITH_AES_128_GCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8442,
        iana_name="TLS_ECDHE_PSK_WITH_AES_128_GCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xD0, 0x01),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_GCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_PSK_WITH_AES_256_GCM_SHA384: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8442,
        iana_name="TLS_ECDHE_PSK_WITH_AES_256_GCM_SHA384",
        openssl_name=None,
        gnutls_name=None,
        code=(0xD0, 0x02),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_256_GCM,
        ssl_hash=SSLHash.SHA384,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_PSK_WITH_AES_128_CCM_8_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8442,
        iana_name="TLS_ECDHE_PSK_WITH_AES_128_CCM_8_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xD0, 0x03),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CCM_8,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )
    ECDHE_PSK_WITH_AES_128_CCM_SHA256: SSLSuiteInfo = SSLSuiteInfo(
        rfc=8442,
        iana_name="TLS_ECDHE_PSK_WITH_AES_128_CCM_SHA256",
        openssl_name=None,
        gnutls_name=None,
        code=(0xD0, 0x05),
        key_exchange=SSLKeyExchange.ECDHE,
        authentication=SSLAuthentication.PSK,
        encryption=SSLEncryption.AES_128_CCM,
        ssl_hash=SSLHash.SHA256,
        tls_versions=(SSLVersionId.tlsv1_2,),
        vulnerabilities=(),
    )


class SSLSpecialSuite(Enum):
    EMPTY_RENEGOTIATION_INFO_SCSV: SSLSuiteInfo = SSLSuiteInfo(
        rfc=5746,
        iana_name="TLS_EMPTY_RENEGOTIATION_INFO_SCSV",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0xFF),
        key_exchange=SSLKeyExchange.NONE,
        authentication=SSLAuthentication.NONE,
        encryption=SSLEncryption.NONE,
        ssl_hash=SSLHash.NONE,
        tls_versions=(
            SSLVersionId.tlsv1_0,
            SSLVersionId.tlsv1_1,
        ),
        vulnerabilities=(),
    )
    FALLBACK_SCSV: SSLSuiteInfo = SSLSuiteInfo(
        rfc=7507,
        iana_name="TLS_FALLBACK_SCSV",
        openssl_name="TLS_FALLBACK_SCSV",
        gnutls_name=None,
        code=(0x56, 0x00),
        key_exchange=SSLKeyExchange.NONE,
        authentication=SSLAuthentication.NONE,
        encryption=SSLEncryption.NONE,
        ssl_hash=SSLHash.NONE,
        tls_versions=(
            SSLVersionId.tlsv1_2,
            SSLVersionId.tlsv1_3,
        ),
        vulnerabilities=(),
    )
    RESERVED_SUITE_00_60: SSLSuiteInfo = SSLSuiteInfo(
        rfc=0,
        iana_name="TLS_RSA_EXPORT1024_WITH_RC4_56_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x60),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.RC4_56,
        ssl_hash=SSLHash.MD5,
        tls_versions=(),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.MD5,
        ),
    )
    RESERVED_SUITE_00_61: SSLSuiteInfo = SSLSuiteInfo(
        rfc=0,
        iana_name="TLS_RSA_EXPORT1024_WITH_RC2_CBC_56_MD5",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x61),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.RC2_56_CBC,
        ssl_hash=SSLHash.MD5,
        tls_versions=(),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.RC2,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.MD5,
        ),
    )
    RESERVED_SUITE_00_62: SSLSuiteInfo = SSLSuiteInfo(
        rfc=0,
        iana_name="TLS_RSA_EXPORT1024_WITH_DES_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x62),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.DES_40_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    RESERVED_SUITE_00_63: SSLSuiteInfo = SSLSuiteInfo(
        rfc=0,
        iana_name="TLS_DHE_DSS_EXPORT1024_WITH_DES_CBC_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x63),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.DES_40_CBC,
        ssl_hash=SSLHash.SHA,
        tls_versions=(),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.DES,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.SHA,
        ),
    )
    RESERVED_SUITE_00_64: SSLSuiteInfo = SSLSuiteInfo(
        rfc=0,
        iana_name="TLS_RSA_EXPORT1024_WITH_RC4_56_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x64),
        key_exchange=SSLKeyExchange.RSA,
        authentication=SSLAuthentication.RSA,
        encryption=SSLEncryption.RC4_56,
        ssl_hash=SSLHash.SHA,
        tls_versions=(),
        vulnerabilities=(
            SSLSuiteVuln.NO_PFS,
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    RESERVED_SUITE_00_65: SSLSuiteInfo = SSLSuiteInfo(
        rfc=0,
        iana_name="TLS_DHE_DSS_EXPORT1024_WITH_RC4_56_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x65),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.RC4_56,
        ssl_hash=SSLHash.SHA,
        tls_versions=(),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )
    RESERVED_SUITE_00_66: SSLSuiteInfo = SSLSuiteInfo(
        rfc=0,
        iana_name="TLS_DHE_DSS_WITH_RC4_128_SHA",
        openssl_name=None,
        gnutls_name=None,
        code=(0x00, 0x66),
        key_exchange=SSLKeyExchange.DHE,
        authentication=SSLAuthentication.DSS,
        encryption=SSLEncryption.RC4_128,
        ssl_hash=SSLHash.SHA,
        tls_versions=(),
        vulnerabilities=(
            SSLSuiteVuln.EXPORT_GRADE,
            SSLSuiteVuln.RC4,
            SSLSuiteVuln.SHA,
        ),
    )


def get_suite_by_openssl_name(name: str) -> SSLSuiteInfo:
    for normal_suite in SSLCipherSuite:
        if name == normal_suite.value.openssl_name:
            return normal_suite.value

    return SSLSuiteInfo(
        rfc=0,
        iana_name="UNKNOWN",
        openssl_name=name,
        gnutls_name=None,
        code=None,
        key_exchange=SSLKeyExchange.UNKNOWN,
        authentication=SSLAuthentication.UNKNOWN,
        encryption=SSLEncryption.UNKNOWN,
        ssl_hash=SSLHash.UNKNOWN,
        tls_versions=(),
        vulnerabilities=(),
    )


def get_suite_by_code(code: Tuple[int, int]) -> SSLSuiteInfo:
    for normal_suite in SSLCipherSuite:
        if code == normal_suite.value.code:
            return normal_suite.value

    for special_suite in SSLSpecialSuite:
        if code == special_suite.value.code:
            return special_suite.value

    return SSLSuiteInfo(
        rfc=0,
        iana_name="UNKNOWN",
        openssl_name=None,
        gnutls_name=None,
        code=code,
        key_exchange=SSLKeyExchange.UNKNOWN,
        authentication=SSLAuthentication.UNKNOWN,
        encryption=SSLEncryption.UNKNOWN,
        ssl_hash=SSLHash.UNKNOWN,
        tls_versions=(),
        vulnerabilities=(),
    )


def get_suites_with_pfs() -> Iterator[SSLSuiteInfo]:
    for suite in SSLCipherSuite:
        if SSLSuiteVuln.NO_PFS not in suite.value.vulnerabilities:
            yield suite.value


def get_suites_with_cbc() -> Iterator[SSLSuiteInfo]:
    for suite in SSLCipherSuite:
        if SSLSuiteVuln.CBC in suite.value.vulnerabilities:
            yield suite.value


def get_weak_suites() -> Iterator[SSLSuiteInfo]:
    for suite in SSLCipherSuite:
        weak_vuln = False
        for vuln in SSLSuiteVuln:
            if vuln in suite.value.vulnerabilities and vuln not in (
                SSLSuiteVuln.NO_PFS,
                SSLSuiteVuln.CBC,
            ):
                weak_vuln = True
                break
        if weak_vuln:
            yield suite.value
