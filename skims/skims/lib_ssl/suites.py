# pylint: disable=too-many-lines
from enum import (
    Enum,
)
from lib_ssl.types import (
    SSLVersionId,
)
from typing import (
    NamedTuple,
    Optional,
    Tuple,
)


class SSLSuiteVuln(Enum):
    PFS: int = 1
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


class SSLAuthentication(Enum):
    NONE: int = 1
    NULL: int = 2
    RSA: int = 3
    DSS: int = 4
    ANON: int = 5
    PSK: int = 6
    KRB_5: int = 7


class SSLEncryption(Enum):
    NULL: int = 1
    RC4_40: int = 2
    RC4_128: int = 3
    RC2_40_CBC: int = 4
    IDEA_CBC: int = 5
    DES_40_CBC: int = 6
    DES_56_CBC: int = 7
    DES3_EDE_CBC: int = 8
    AES_128_CBC: int = 9
    AES_256_CBC: int = 10
    CAMELLIA_128_CBC: int = 11
    CAMELLIA_256_CBC: int = 12
    SEED_CBC: int = 13
    AES_128_GCM: int = 14
    AES_256_GCM: int = 15
    SM_4_GCM: int = 16
    SM_4_CCM: int = 17


class SSLHash(Enum):
    NULL: int = 1
    MD5: int = 2
    SHA: int = 3
    SHA256: int = 4
    SHA384: int = 5
    SM3: int = 6


class SSLSuiteInfo(NamedTuple):
    rfc: int
    iana_name: str
    openssl_name: Optional[str]
    gnutls_name: Optional[str]
    code: Tuple[int, int]
    key_exchange: SSLKeyExchange
    authentication: SSLAuthentication
    encryption: SSLEncryption
    ssl_hash: SSLHash
    tls_versions: Tuple[SSLVersionId, ...]
    vulnerabilities: Tuple[SSLSuiteVuln, ...]


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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
            SSLSuiteVuln.CBC,
            SSLSuiteVuln.DES,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
        vulnerabilities=(SSLSuiteVuln.PFS,),
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
        vulnerabilities=(SSLSuiteVuln.PFS,),
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
        vulnerabilities=(SSLSuiteVuln.PFS,),
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
        vulnerabilities=(SSLSuiteVuln.PFS,),
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
        vulnerabilities=(SSLSuiteVuln.PFS,),
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
        vulnerabilities=(SSLSuiteVuln.PFS,),
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
        vulnerabilities=(SSLSuiteVuln.PFS,),
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
        vulnerabilities=(SSLSuiteVuln.PFS,),
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
        vulnerabilities=(SSLSuiteVuln.PFS,),
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
        vulnerabilities=(SSLSuiteVuln.PFS,),
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
            SSLSuiteVuln.PFS,
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
