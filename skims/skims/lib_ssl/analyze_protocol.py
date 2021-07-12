from lib_ssl.as_string import (
    snippet,
    ssl_versions,
)
from lib_ssl.ssl_connection import (
    connect,
    get_client_hello_package,
    get_ec_point_formats_ext,
    get_elliptic_curves_ext,
    get_heartbeat_ext,
    get_malicious_heartbeat,
    get_session_ticket_ext,
    read_ssl_record,
)
from lib_ssl.types import (
    SSLContext,
    SSLSettings,
    SSLSnippetLine,
    SSLVulnerability,
)
from model import (
    core_model,
)
import tlslite
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
)
from utils.ctx import (
    CTX,
)
from utils.sockets import (
    tcp_connect,
)
from zone import (
    t,
)


def _create_core_vulns(
    ssl_vulnerabilities: List[SSLVulnerability],
) -> core_model.Vulnerabilities:
    return tuple(
        core_model.Vulnerability(
            finding=ssl_vulnerability.finding,
            kind=core_model.VulnerabilityKindEnum.INPUTS,
            namespace=CTX.config.namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            stream="home,socket-send,socket-response",
            what=ssl_vulnerability.ssl_settings.get_target(),
            where=ssl_vulnerability.description,
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=(ssl_vulnerability.finding.value.cwe,),
                description=ssl_vulnerability.description,
                snippet=snippet(
                    locale=CTX.config.language,
                    ssl_vulnerability=ssl_vulnerability,
                ),
            ),
        )
        for ssl_vulnerability in ssl_vulnerabilities
    )


def _create_ssl_vuln(
    check: str,
    line: SSLSnippetLine,
    ssl_settings: SSLSettings,
    finding: core_model.FindingEnum,
    check_kwargs: Optional[Dict[str, str]] = None,
) -> SSLVulnerability:
    return SSLVulnerability(
        line=line,
        finding=finding,
        ssl_settings=ssl_settings,
        description=t(
            f"lib_ssl.analyze_protocol.{check}", **(check_kwargs or {})
        ),
    )


def _pfs_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    ssl_settings = SSLSettings(
        host=ctx.target.host,
        port=ctx.target.port,
        key_exchange_names=["dhe_rsa", "ecdhe_rsa", "ecdh_anon", "dh_anon"],
        intention={
            core_model.LocalesEnum.EN: (
                "check if server accepts key exchange with PFS support"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor acepta intercambio de llaves"
                "con soporte PFS"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and connection.closed:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="pfs_disabled",
                    ssl_settings=ssl_settings,
                    line=SSLSnippetLine.key_exchange,
                    finding=core_model.FindingEnum.F052_PFS,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


def _sslv3_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    ssl_settings = SSLSettings(
        host=ctx.target.host,
        port=ctx.target.port,
        max_version=(3, 0),
        intention={
            core_model.LocalesEnum.EN: (
                "check if server accepts connections with SSLv3"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor acepta conexiones con SSLv3"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="sslv3_enabled",
                    ssl_settings=ssl_settings,
                    line=SSLSnippetLine.max_version,
                    finding=core_model.FindingEnum.F052_SSLV3,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    ssl_settings = SSLSettings(
        host=ctx.target.host,
        port=ctx.target.port,
        min_version=(3, 1),
        max_version=(3, 1),
        intention={
            core_model.LocalesEnum.EN: (
                "check if server accepts connections with TLSv1.0"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor acepta conexiones con TLSv1.0"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="tlsv1_enabled",
                    ssl_settings=ssl_settings,
                    line=SSLSnippetLine.max_version,
                    finding=core_model.FindingEnum.F052_TLS,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_1_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    ssl_settings = SSLSettings(
        host=ctx.target.host,
        port=ctx.target.port,
        min_version=(3, 2),
        max_version=(3, 2),
        intention={
            core_model.LocalesEnum.EN: (
                "check if server accepts connections with TLSv1.1"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor acepta conexiones con TLSv1.1"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="tlsv1_1_enabled",
                    ssl_settings=ssl_settings,
                    line=SSLSnippetLine.max_version,
                    finding=core_model.FindingEnum.F052_TLS,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_3_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    ssl_settings = SSLSettings(
        ctx.target.host,
        ctx.target.port,
        min_version=(3, 4),
        max_version=(3, 4),
        intention={
            core_model.LocalesEnum.EN: (
                "check if server accepts connections with TLSv1.3"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor acepta conexiones con TLSv1.3"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSLocalAlert,),
    ) as connection:
        if connection is not None and connection.closed:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="tlsv1_3_disabled",
                    ssl_settings=ssl_settings,
                    line=SSLSnippetLine.max_version,
                    finding=core_model.FindingEnum.F052_TLS,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


def _anonymous_suits_allowed(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    ssl_settings = SSLSettings(
        ctx.target.host,
        ctx.target.port,
        anonymous=True,
        intention={
            core_model.LocalesEnum.EN: (
                "check if server accepts connections with anonymous"
                " cipher suits"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor acepta conexiones con suites"
                " de cifrado anónimo"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="anonymous_suits_allowed",
                    ssl_settings=ssl_settings,
                    line=SSLSnippetLine.key_exchange,
                    finding=core_model.FindingEnum.F052_ANON,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


def _weak_ciphers_allowed(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    ssl_settings = SSLSettings(
        ctx.target.host,
        ctx.target.port,
        cipher_names=["rc4", "3des", "null"],
        intention={
            core_model.LocalesEnum.EN: (
                "check if server accepts connections with weak ciphers"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor acepta conexiones con cifrado débil"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="weak_ciphers_allowed",
                    ssl_settings=ssl_settings,
                    line=SSLSnippetLine.ciphers,
                    finding=core_model.FindingEnum.F052,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


def _beast_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    ssl_settings = SSLSettings(
        ctx.target.host,
        ctx.target.port,
        min_version=(3, 1),
        max_version=(3, 1),
        intention={
            core_model.LocalesEnum.EN: (
                "check if server is vulnerable to BEAST attacks"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor es vulnerable a ataques BEAST"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            # pylint: disable=protected-access
            if connection._recordLayer.isCBCMode():
                ssl_vulnerabilities.append(
                    _create_ssl_vuln(
                        check="beast_possible",
                        ssl_settings=ssl_settings,
                        line=SSLSnippetLine.max_version,
                        finding=core_model.FindingEnum.F052_CBC,
                    )
                )

    return _create_core_vulns(ssl_vulnerabilities)


def _cbc_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    ssl_settings = SSLSettings(
        ctx.target.host,
        ctx.target.port,
        min_version=(3, 2),
        max_version=(3, 3),
        intention={
            core_model.LocalesEnum.EN: (
                "check if server accepts connections with ciphers that use CBC"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor acepta conexiones con cifrado"
                " que utiliza CBC"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            # pylint: disable=protected-access
            if connection._recordLayer.isCBCMode():
                ssl_vulnerabilities.append(
                    _create_ssl_vuln(
                        check="cbc_enabled",
                        ssl_settings=ssl_settings,
                        line=SSLSnippetLine.ciphers,
                        finding=core_model.FindingEnum.F052_CBC,
                    )
                )

    return _create_core_vulns(ssl_vulnerabilities)


def _sweet32_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    ssl_settings = SSLSettings(
        ctx.target.host,
        ctx.target.port,
        min_version=(3, 1),
        max_version=(3, 3),
        cipher_names=["3des"],
        intention={
            core_model.LocalesEnum.EN: (
                "check if server is vulnerable to SWEET32 attacks"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor es vulnerable a ataques SWEET32"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="sweet32_possible",
                    ssl_settings=ssl_settings,
                    line=SSLSnippetLine.ciphers,
                    finding=core_model.FindingEnum.F052_CBC,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


def _server_supports_tls(ctx: SSLContext, version: Tuple[int, int]) -> bool:
    ssl_settings = SSLSettings(
        ctx.target.host,
        ctx.target.port,
        min_version=version,
        max_version=version,
        intention={
            core_model.LocalesEnum.EN: (
                "check if server supports {version}".format(
                    version=ssl_versions[version],
                )
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor soporta {version}".format(
                    version=ssl_versions[version],
                )
            ),
        },
    )
    with connect(
        ssl_settings=ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            return True
    return False


def _fallback_scsv_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    min_version_id: int = -1

    for version_id in range(0, 3):
        if _server_supports_tls(ctx, version=(3, version_id)):
            min_version_id = version_id
            break

    if min_version_id == -1:
        return tuple()

    min_version: Tuple[int, int] = (3, min_version_id)

    ssl_settings = SSLSettings(
        ctx.target.host,
        ctx.target.port,
        scsv=True,
        min_version=min_version,
        max_version=min_version,
        intention={
            core_model.LocalesEnum.EN: (
                "check if server supports TLS_FALLBACK_SCSV"
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor soporta TLS_FALLBACK_SCSV"
            ),
        },
    )

    with connect(
        ssl_settings,
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="fallback_scsv_disabled",
                    ssl_settings=ssl_settings,
                    line=SSLSnippetLine.max_version,
                    finding=core_model.FindingEnum.F052_TLS,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_3_downgrade(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    if not _server_supports_tls(ctx, version=(3, 4)):
        return tuple()

    for version_id in range(0, 3):
        version: Tuple[int, int] = (3, version_id)
        ssl_settings = SSLSettings(
            ctx.target.host,
            ctx.target.port,
            min_version=version,
            max_version=version,
            intention={
                core_model.LocalesEnum.EN: (
                    "check if TLSv1.3 can be downgraded to {version}".format(
                        version=ssl_versions[version],
                    )
                ),
                core_model.LocalesEnum.ES: (
                    "verificar si TLSv1.3 puede degradarse a {version}".format(
                        version=ssl_versions[version],
                    )
                ),
            },
        )

        with connect(
            ssl_settings,
            expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
        ) as connection:
            if connection is not None and not connection.closed:
                ssl_vulnerabilities.append(
                    _create_ssl_vuln(
                        check="tlsv1_3_downgrade",
                        ssl_settings=ssl_settings,
                        line=SSLSnippetLine.max_version,
                        finding=core_model.FindingEnum.F052_TLS,
                        check_kwargs={"version": f"{ssl_versions[version]}"},
                    )
                )

    return _create_core_vulns(ssl_vulnerabilities)


def _heartbleed_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    suits: List[str] = [
        "ECDHE_RSA_WITH_AES_256_CBC_SHA",
        "ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
        "SRP_SHA_DSS_WITH_AES_256_CBC_SHA",
        "SRP_SHA_RSA_WITH_AES_256_CBC_SHA",
        "DHE_RSA_WITH_AES_256_CBC_SHA",
        "DHE_DSS_WITH_AES_256_CBC_SHA",
        "DHE_RSA_WITH_CAMELLIA_256_CBC_SHA",
        "DHE_DSS_WITH_CAMELLIA_256_CBC_SHA",
        "ECDH_RSA_WITH_AES_256_CBC_SHA",
        "ECDH_ECDSA_WITH_AES_256_CBC_SHA",
        "RSA_WITH_AES_256_CBC_SHA",
        "RSA_WITH_CAMELLIA_256_CBC_SHA",
        "ECDHE_RSA_WITH_3DES_EDE_CBC_SHA",
        "ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA",
        "SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA",
        "SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA",
        "DHE_RSA_WITH_3DES_EDE_CBC_SHA",
        "DHE_DSS_WITH_3DES_EDE_CBC_SHA",
        "ECDH_RSA_WITH_3DES_EDE_CBC_SHA",
        "ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA",
        "RSA_WITH_3DES_EDE_CBC_SHA",
        "ECDHE_RSA_WITH_AES_128_CBC_SHA",
        "ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
        "SRP_SHA_DSS_WITH_AES_128_CBC_SHA",
        "SRP_SHA_RSA_WITH_AES_128_CBC_SHA",
        "DHE_RSA_WITH_AES_128_CBC_SHA",
        "DHE_DSS_WITH_AES_128_CBC_SHA",
        "DHE_RSA_WITH_SEED_CBC_SHA",
        "DHE_DSS_WITH_SEED_CBC_SHA",
        "DHE_RSA_WITH_CAMELLIA_128_CBC_SHA",
        "DHE_DSS_WITH_CAMELLIA_128_CBC_SHA",
        "ECDH_RSA_WITH_AES_128_CBC_SHA",
        "ECDH_ECDSA_WITH_AES_128_CBC_SHA",
        "RSA_WITH_AES_128_CBC_SHA",
        "RSA_WITH_SEED_CBC_SHA",
        "RSA_WITH_CAMELLIA_128_CBC_SHA",
        "ECDHE_RSA_WITH_RC4_128_SHA",
        "ECDHE_ECDSA_WITH_RC4_128_SHA",
        "ECDH_RSA_WITH_RC4_128_SHA",
        "ECDH_ECDSA_WITH_RC4_128_SHA",
        "RSA_WITH_RC4_128_SHA",
        "RSA_WITH_RC4_128_MD5",
        "DHE_RSA_WITH_DES_CBC_SHA",
        "DHE_DSS_WITH_DES_CBC_SHA",
        "RSA_WITH_DES_CBC_SHA",
        "DHE_RSA_EXPORT_WITH_DES40_CBC_SHA",
        "DHE_DSS_EXPORT_WITH_DES40_CBC_SHA",
        "RSA_EXPORT_WITH_DES40_CBC_SHA",
        "RSA_EXPORT_WITH_RC2_CBC_40_MD5",
        "RSA_EXPORT_WITH_RC4_40_MD5",
        "EMPTY_RENEGOTIATION_INFO_SCSV",
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()
    extensions += get_heartbeat_ext()

    for version_id in [3, 2, 1, 0]:
        version: Tuple[int, int] = (3, version_id)

        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                "check if server is vulnerable to heartbleed attack with"
                " {version}".format(
                    version=ssl_versions[version],
                )
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor es vulnerable a un ataque heartbleed"
                "con {version}".format(
                    version=ssl_versions[version],
                )
            ),
        }

        sock = tcp_connect(
            ctx.target.host,
            ctx.target.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            break

        package = get_client_hello_package(version_id, suits, extensions)
        sock.send(bytes(package))
        handshake_record = read_ssl_record(sock)

        if handshake_record is not None:
            handshake_type, _, _ = handshake_record

            if handshake_type == 22:
                package = get_malicious_heartbeat(version_id, n_payload=16384)
                sock.send(bytes(package))

                heartbeat_record = read_ssl_record(sock)

                if heartbeat_record is not None:
                    heartbeat_type, _, _ = heartbeat_record

                    if heartbeat_type == 24:
                        ssl_vulnerabilities.append(
                            _create_ssl_vuln(
                                check="heartbleed_possible",
                                line=SSLSnippetLine.max_version,
                                ssl_settings=SSLSettings(
                                    ctx.target.host,
                                    ctx.target.port,
                                    min_version=version,
                                    max_version=version,
                                    intention=intention,
                                ),
                                finding=core_model.FindingEnum.F052_TLS,
                            )
                        )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _freak_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    suits: List[str] = [
        "RESERVED_SUITE_00_62",
        "RESERVED_SUITE_00_61",
        "RESERVED_SUITE_00_64",
        "RESERVED_SUITE_00_60",
        "DHE_RSA_EXPORT_WITH_DES40_CBC_SHA",
        "DHE_DSS_EXPORT_WITH_DES40_CBC_SHA",
        "RSA_EXPORT_WITH_DES40_CBC_SHA",
        "RSA_EXPORT_WITH_RC2_CBC_40_MD5",
        "RSA_EXPORT_WITH_RC4_40_MD5",
        "EMPTY_RENEGOTIATION_INFO_SCSV",
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()
    extensions += get_heartbeat_ext()

    for version_id in [3, 2, 1, 0]:
        version: Tuple[int, int] = (3, version_id)

        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                "check if server is vulnerable to FREAK attack with"
                " {version}".format(
                    version=ssl_versions[version],
                )
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor es vulnerable a un ataque FREAK"
                "con {version}".format(
                    version=ssl_versions[version],
                )
            ),
        }

        sock = tcp_connect(
            ctx.target.host,
            ctx.target.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            break

        package = get_client_hello_package(version_id, suits, extensions)
        sock.send(bytes(package))
        handshake_record = read_ssl_record(sock)

        if handshake_record is not None:
            handshake_type, _, _ = handshake_record

            if handshake_type == 22:
                ssl_vulnerabilities.append(
                    _create_ssl_vuln(
                        check="freak_possible",
                        line=SSLSnippetLine.max_version,
                        ssl_settings=SSLSettings(
                            ctx.target.host,
                            ctx.target.port,
                            min_version=version,
                            max_version=version,
                            intention=intention,
                        ),
                        finding=core_model.FindingEnum.F052_TLS,
                    )
                )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def get_check_ctx(ssl_ctx: SSLContext) -> SSLContext:
    return ssl_ctx


CHECKS: Dict[
    core_model.FindingEnum,
    List[Callable[[SSLContext], core_model.Vulnerabilities]],
] = {
    core_model.FindingEnum.F052: [_weak_ciphers_allowed],
    core_model.FindingEnum.F052_ANON: [_anonymous_suits_allowed],
    core_model.FindingEnum.F052_CBC: [
        _beast_possible,
        _cbc_enabled,
        _sweet32_possible,
    ],
    core_model.FindingEnum.F052_PFS: [_pfs_disabled],
    core_model.FindingEnum.F052_SSLV3: [_sslv3_enabled],
    core_model.FindingEnum.F052_TLS: [
        _tlsv1_enabled,
        _tlsv1_1_enabled,
        _tlsv1_3_disabled,
        _fallback_scsv_disabled,
        _tlsv1_3_downgrade,
        _heartbleed_possible,
        _freak_possible,
    ],
}
