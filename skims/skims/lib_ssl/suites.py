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
    EXPORT_GRADE: int = 9
    ANON_KEY_EXCHANGE: int = 10
    NULL_AUTHENTICATION: int = 11
    NULL_ENCRIPTION: int = 12


class SSLKeyExchange(Enum):
    NULL: int = 1
    RSA: int = 2


class SSLAuthentication(Enum):
    NULL: int = 1
    RSA: int = 2


class SSLEncryption(Enum):
    NULL: int = 1


class SSLHash(Enum):
    NULL: int = 1
    MD5: int = 2
    SHA: int = 3


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
            SSLSuiteVuln.NULL_ENCRIPTION,
        ),
    )
