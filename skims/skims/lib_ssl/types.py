# pylint: disable=invalid-name
from enum import (
    Enum,
)
from lib_ssl.suites import (
    SSLSuiteInfo,
    SSLVersionId,
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


class SSLSnippetLine(Enum):
    SERVER: int = 1
    INTENTION: int = 2
    VERSIONS: int = 3
    REQUEST: int = 5
    RESPONSE: int = 10


class TLSVersionId(Enum):
    tlsv1_0: TLSVersion = TLSVersion.TLSv1
    tlsv1_1: TLSVersion = TLSVersion.TLSv1_1
    tlsv1_2: TLSVersion = TLSVersion.TLSv1_2
    tlsv1_3: TLSVersion = TLSVersion.TLSv1_3


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
    cipher_suite: SSLSuiteInfo


class SSLServerResponse(NamedTuple):
    record: SSLRecord
    version_id: SSLVersionId
    alert: Optional[SSLAlert] = None
    handshake: Optional[SSLServerHandshake] = None


class SSLContext(NamedTuple):
    host: str = "localhost"
    port: int = 443
    tls_responses: Tuple[SSLServerResponse, ...] = ()

    def get_tls_response(
        self, v_id: SSLVersionId
    ) -> Optional[SSLServerResponse]:
        for tls_response in self.tls_responses:
            if (
                tls_response.handshake is not None
                and tls_response.handshake.version_id == v_id
            ):
                return tls_response
        return None

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
    tls_version: SSLVersionId = SSLVersionId.sslv3_0
    key_exchange_names: List[str] = ["ANY"]
    authentication_names: List[str] = ["ANY"]
    cipher_names: List[str] = ["ANY"]
    hash_names: List[str] = ["ANY"]
    intention: Dict[LocalesEnum, str] = {
        LocalesEnum.EN: "establish SSL/TLS connection",
        LocalesEnum.ES: "establecer conexión SSL/TLS",
    }

    def __str__(self) -> str:
        return str(self.context)


class SSLVulnerability(NamedTuple):
    description: str
    ssl_settings: SSLSettings
    server_response: Optional[SSLServerResponse]
    finding: FindingEnum

    def get_context(self) -> SSLContext:
        return self.ssl_settings.context

    def get_intention(self, locale: LocalesEnum) -> str:
        return self.ssl_settings.intention[locale]

    def __str__(self) -> str:
        return str(self.ssl_settings)
