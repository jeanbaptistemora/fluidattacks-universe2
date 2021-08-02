# pylint: disable=too-many-lines
from lib_ssl.as_string import (
    snippet,
    ssl_id2ssl_name,
)
from lib_ssl.ssl_connection import (
    get_client_hello_package,
    get_ec_point_formats_ext,
    get_elliptic_curves_ext,
    get_heartbeat_ext,
    get_malicious_heartbeat,
    get_session_ticket_ext,
    read_ssl_record,
    ssl_connect,
)
from lib_ssl.types import (
    SSLContext,
    SSLSettings,
    SSLSnippetLine,
    SSLSuite,
    SSLVersionId,
    SSLVulnerability,
)
from model import (
    core_model,
)
from typing import (
    Callable,
    Dict,
    List,
    Optional,
)
from utils.ctx import (
    CTX,
)
from utils.http import (
    request_blocking,
)
from utils.sockets import (
    tcp_connect,
)
from zone import (
    t,
)


def supports_tls(host: str, port: int, v_id: SSLVersionId) -> Optional[bool]:
    intention_en = "verify if server supports " + ssl_id2ssl_name(v_id)
    ssl_settings = SSLSettings(
        host=host,
        port=port,
        min_version=v_id,
        max_version=v_id,
        intention={core_model.LocalesEnum.EN: intention_en},
    )

    supported: bool = False
    with ssl_connect(ssl_settings) as ssl_socket:
        if ssl_socket is not None:
            supported = True
    return supported


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

    suites: List[SSLSuite] = [
        SSLSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_DES_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_DES_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_AES_128_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_AES_256_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_AES_256_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_SEED_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_SEED_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.DHE_RSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.DHE_DSS_WITH_AES_128_GCM_SHA256,
        SSLSuite.DHE_DSS_WITH_AES_256_GCM_SHA384,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_NULL_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_RC4_128_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_NULL_SHA,
        SSLSuite.ECDHE_RSA_WITH_RC4_128_SHA,
        SSLSuite.ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA384,
        SSLSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA384,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.ECDHE_RSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.ECDHE_RSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.DHE_DSS_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.DHE_RSA_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.ECDHE_ECDSA_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.ECDHE_RSA_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.ECDHE_RSA_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.DHE_RSA_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.DHE_RSA_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.DHE_DSS_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.DHE_DSS_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.ECDHE_RSA_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.ECDHE_RSA_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.ECDHE_ECDSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.ECDHE_RSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.ECDHE_RSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DHE_RSA_WITH_AES_128_CCM,
        SSLSuite.DHE_RSA_WITH_AES_256_CCM,
        SSLSuite.DHE_RSA_WITH_AES_128_CCM_8,
        SSLSuite.DHE_RSA_WITH_AES_256_CCM_8,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_CCM,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_CCM,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_CCM_8,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_CCM_8,
        SSLSuite.ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,
        SSLSuite.DHE_RSA_WITH_CHACHA20_POLY1305_SHA256,
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()

    for v_id in ctx.tls_versions:
        if v_id == SSLVersionId.tlsv1_3:
            continue

        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                "check if server accepts key exchange with PFS support in"
                " {v_name}".format(
                    v_name=ssl_id2ssl_name(v_id),
                )
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor acepta intercambio de llaves con"
                "soporte PFS en {v_name}".format(
                    v_name=ssl_id2ssl_name(v_id),
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

        package = get_client_hello_package(v_id, suites, extensions)
        sock.send(bytes(package))
        handshake_record = read_ssl_record(sock)

        if handshake_record is not None:
            handshake_type, _, _ = handshake_record

            if handshake_type != 22:
                ssl_vulnerabilities.append(
                    _create_ssl_vuln(
                        check="pfs_disabled",
                        line=SSLSnippetLine.key_exchange,
                        ssl_settings=SSLSettings(
                            ctx.target.host,
                            ctx.target.port,
                            min_version=v_id,
                            max_version=v_id,
                            key_exchange_names=[
                                "dhe_rsa",
                                "ecdhe_rsa",
                                "ecdh_anon",
                                "dh_anon",
                            ],
                            intention=intention,
                        ),
                        finding=core_model.FindingEnum.F133,
                    )
                )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _sslv3_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    suites: List[SSLSuite] = [
        SSLSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_AES_256_CBC_SHA,
        SSLSuite.DH_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.DH_DSS_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DH_RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DH_DSS_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.ECDH_anon_WITH_AES_256_CBC_SHA,
        SSLSuite.DH_anon_WITH_AES_256_CBC_SHA,
        SSLSuite.DH_anon_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_AES_256_CBC_SHA,
        SSLSuite.RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_AES_128_CBC_SHA,
        SSLSuite.DH_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DH_DSS_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_SEED_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_SEED_CBC_SHA,
        SSLSuite.DH_RSA_WITH_SEED_CBC_SHA,
        SSLSuite.DH_DSS_WITH_SEED_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DH_RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DH_DSS_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.ECDH_anon_WITH_AES_128_CBC_SHA,
        SSLSuite.DH_anon_WITH_AES_128_CBC_SHA,
        SSLSuite.DH_anon_WITH_SEED_CBC_SHA,
        SSLSuite.DH_anon_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_AES_128_CBC_SHA,
        SSLSuite.RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.RSA_WITH_SEED_CBC_SHA,
        SSLSuite.RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.RSA_WITH_IDEA_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_RC4_128_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_RC4_128_SHA,
        SSLSuite.RESERVED_SUITE_00_66,
        SSLSuite.ECDH_anon_WITH_RC4_128_SHA,
        SSLSuite.DH_anon_WITH_RC4_128_MD5,
        SSLSuite.ECDH_RSA_WITH_RC4_128_SHA,
        SSLSuite.ECDH_ECDSA_WITH_RC4_128_SHA,
        SSLSuite.RSA_WITH_RC4_128_SHA,
        SSLSuite.RSA_WITH_RC4_128_MD5,
        SSLSuite.RSA_PSK_WITH_RC4_128_SHA,
        SSLSuite.ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_anon_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_anon_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RESERVED_SUITE_00_63,
        SSLSuite.DHE_RSA_WITH_DES_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_DES_CBC_SHA,
        SSLSuite.DH_RSA_WITH_DES_CBC_SHA,
        SSLSuite.DH_DSS_WITH_DES_CBC_SHA,
        SSLSuite.DH_anon_WITH_DES_CBC_SHA,
        SSLSuite.RESERVED_SUITE_00_62,
        SSLSuite.RSA_WITH_DES_CBC_SHA,
        SSLSuite.RESERVED_SUITE_00_61,
        SSLSuite.RESERVED_SUITE_00_65,
        SSLSuite.RESERVED_SUITE_00_64,
        SSLSuite.RESERVED_SUITE_00_60,
        SSLSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_anon_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5,
        SSLSuite.DH_anon_EXPORT_WITH_RC4_40_MD5,
        SSLSuite.RSA_EXPORT_WITH_RC4_40_MD5,
        SSLSuite.ECDHE_RSA_WITH_NULL_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_NULL_SHA,
        SSLSuite.ECDH_anon_WITH_NULL_SHA,
        SSLSuite.ECDH_RSA_WITH_NULL_SHA,
        SSLSuite.ECDH_ECDSA_WITH_NULL_SHA,
        SSLSuite.RSA_WITH_NULL_SHA,
        SSLSuite.RSA_WITH_NULL_MD5,
        SSLSuite.EMPTY_RENEGOTIATION_INFO_SCSV,
    ]

    intention: Dict[core_model.LocalesEnum, str] = {
        core_model.LocalesEnum.EN: (
            "check if server accepts connections with SSLv3"
        ),
        core_model.LocalesEnum.ES: (
            "verificar si el servidor acepta conexiones con SSLv3"
        ),
    }

    sock = tcp_connect(
        ctx.target.host,
        ctx.target.port,
        intention[core_model.LocalesEnum.EN],
    )

    if sock is None:
        return tuple()

    package = get_client_hello_package(SSLVersionId.sslv3_0, suites)
    sock.send(bytes(package))
    handshake_record = read_ssl_record(sock)

    if handshake_record is not None:
        handshake_type, _, _ = handshake_record

        if handshake_type == 22:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="sslv3_enabled",
                    line=SSLSnippetLine.max_version,
                    ssl_settings=SSLSettings(
                        host=ctx.target.host,
                        port=ctx.target.port,
                        max_version=SSLVersionId.sslv3_0,
                        intention=intention,
                    ),
                    finding=core_model.FindingEnum.F016,
                )
            )
    sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    if SSLVersionId.tlsv1_0 in ctx.tls_versions:
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                check="tlsv1_enabled",
                ssl_settings=SSLSettings(
                    host=ctx.target.host,
                    port=ctx.target.port,
                    min_version=SSLVersionId.tlsv1_0,
                    max_version=SSLVersionId.tlsv1_0,
                    intention={
                        core_model.LocalesEnum.EN: (
                            "check if server accepts connections with TLSv1.0"
                        ),
                        core_model.LocalesEnum.ES: (
                            "verificar si el servidor acepta TLSv1.0"
                        ),
                    },
                ),
                line=SSLSnippetLine.max_version,
                finding=core_model.FindingEnum.F016,
            )
        )

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_1_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    if SSLVersionId.tlsv1_1 in ctx.tls_versions:
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                check="tlsv1_1_enabled",
                ssl_settings=SSLSettings(
                    host=ctx.target.host,
                    port=ctx.target.port,
                    min_version=SSLVersionId.tlsv1_1,
                    max_version=SSLVersionId.tlsv1_1,
                    intention={
                        core_model.LocalesEnum.EN: (
                            "check if server accepts connections with TLSv1.1"
                        ),
                        core_model.LocalesEnum.ES: (
                            "verificar si el servidor acepta TLSv1.1"
                        ),
                    },
                ),
                line=SSLSnippetLine.max_version,
                finding=core_model.FindingEnum.F016,
            )
        )

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_2_or_higher_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    if not ctx.tls_versions:
        return tuple()

    if (
        SSLVersionId.tlsv1_2 not in ctx.tls_versions
        and SSLVersionId.tlsv1_3 not in ctx.tls_versions
    ):
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                check="tlsv1_2_or_higher_disabled",
                ssl_settings=SSLSettings(
                    ctx.target.host,
                    ctx.target.port,
                    min_version=SSLVersionId.tlsv1_2,
                    max_version=SSLVersionId.tlsv1_3,
                    intention={
                        core_model.LocalesEnum.EN: (
                            "check if server accepts TLSv1.2 or TLSv1.3"
                        ),
                        core_model.LocalesEnum.ES: (
                            "verificar si el servidor acepta TLSv1.2 o TLSv1.3"
                        ),
                    },
                ),
                line=SSLSnippetLine.max_version,
                finding=core_model.FindingEnum.F016,
            )
        )

    return _create_core_vulns(ssl_vulnerabilities)


def _weak_ciphers_allowed(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    suites: List[SSLSuite] = [
        SSLSuite.NULL_WITH_NULL_NULL,
        SSLSuite.KRB5_EXPORT_WITH_RC4_40_SHA,
        SSLSuite.DH_anon_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.DH_anon_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.DHE_PSK_WITH_NULL_SHA256,
        SSLSuite.ECDHE_PSK_WITH_RC4_128_SHA,
        SSLSuite.PSK_WITH_RC4_128_SHA,
        SSLSuite.RSA_WITH_NULL_SHA256,
        SSLSuite.RSA_WITH_DES_CBC_SHA,
        SSLSuite.PSK_WITH_NULL_SHA384,
        SSLSuite.DH_anon_WITH_AES_256_CBC_SHA256,
        SSLSuite.ECDHE_PSK_WITH_NULL_SHA,
        SSLSuite.SM4_GCM_SM3,
        SSLSuite.DH_RSA_WITH_DES_CBC_SHA,
        SSLSuite.KRB5_WITH_RC4_128_SHA,
        SSLSuite.DH_anon_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DH_DSS_WITH_DES_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_RC4_128_SHA,
        SSLSuite.RSA_WITH_RC4_128_MD5,
        SSLSuite.DH_anon_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_anon_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.PSK_WITH_NULL_SHA,
        SSLSuite.RSA_EXPORT_WITH_RC4_40_MD5,
        SSLSuite.RSA_WITH_NULL_MD5,
        SSLSuite.KRB5_EXPORT_WITH_DES_CBC_40_SHA,
        SSLSuite.DH_anon_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_PSK_WITH_NULL_SHA,
        SSLSuite.PSK_WITH_NULL_SHA256,
        SSLSuite.ECDH_ECDSA_WITH_RC4_128_SHA,
        SSLSuite.ECDH_anon_WITH_AES_128_CBC_SHA,
        SSLSuite.DH_anon_WITH_SEED_CBC_SHA,
        SSLSuite.ECDH_anon_WITH_NULL_SHA,
        SSLSuite.ECDH_anon_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDHE_PSK_WITH_NULL_SHA384,
        SSLSuite.DH_anon_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_NULL_SHA256,
        SSLSuite.ECDHE_RSA_WITH_RC4_128_SHA,
        SSLSuite.RSA_WITH_RC4_128_SHA,
        SSLSuite.KRB5_EXPORT_WITH_RC2_CBC_40_MD5,
        SSLSuite.DH_anon_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.ECDH_ECDSA_WITH_NULL_SHA,
        SSLSuite.DH_anon_EXPORT_WITH_RC4_40_MD5,
        SSLSuite.KRB5_WITH_IDEA_CBC_MD5,
        SSLSuite.RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.KRB5_EXPORT_WITH_DES_CBC_40_MD5,
        SSLSuite.DHE_PSK_WITH_RC4_128_SHA,
        SSLSuite.DH_anon_WITH_AES_256_CBC_SHA,
        SSLSuite.KRB5_EXPORT_WITH_RC2_CBC_40_SHA,
        SSLSuite.DH_anon_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DH_anon_WITH_RC4_128_MD5,
        SSLSuite.DH_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.KRB5_WITH_RC4_128_MD5,
        SSLSuite.DH_anon_WITH_DES_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_NULL_SHA,
        SSLSuite.KRB5_WITH_DES_CBC_MD5,
        SSLSuite.DH_anon_WITH_AES_128_CBC_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_RC4_128_SHA,
        SSLSuite.ECDH_anon_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_anon_WITH_RC4_128_SHA,
        SSLSuite.DHE_RSA_WITH_DES_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_NULL_SHA384,
        SSLSuite.KRB5_WITH_3DES_EDE_CBC_MD5,
        SSLSuite.DHE_PSK_WITH_NULL_SHA384,
        SSLSuite.DH_anon_WITH_AES_128_GCM_SHA256,
        SSLSuite.ECDH_RSA_WITH_NULL_SHA,
        SSLSuite.SM4_CCM_SM3,
        SSLSuite.DH_anon_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.RSA_PSK_WITH_RC4_128_SHA,
        SSLSuite.KRB5_WITH_DES_CBC_SHA,
        SSLSuite.DH_anon_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_NULL_SHA,
        SSLSuite.DH_anon_WITH_AES_256_GCM_SHA384,
        SSLSuite.KRB5_EXPORT_WITH_RC4_40_MD5,
        SSLSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.RSA_WITH_NULL_SHA,
        SSLSuite.DH_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_anon_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.ECDHE_PSK_WITH_NULL_SHA256,
        SSLSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5,
        SSLSuite.DH_anon_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_DES_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_NULL_SHA,
        SSLSuite.RSA_PSK_WITH_CHACHA20_POLY1305_SHA256,
        SSLSuite.ECDHE_PSK_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.PSK_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.ECDHE_PSK_WITH_AES_128_CBC_SHA256,
        SSLSuite.DH_DSS_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.RSA_PSK_WITH_AES_128_CBC_SHA,
        SSLSuite.DH_DSS_WITH_AES_128_CBC_SHA256,
        SSLSuite.RSA_PSK_WITH_AES_256_CBC_SHA384,
        SSLSuite.ECDH_ECDSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.DHE_PSK_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.PSK_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.ECDH_ECDSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.DHE_DSS_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_AES_256_CBC_SHA,
        SSLSuite.DH_DSS_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.DH_DSS_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.RSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.RSA_WITH_SEED_CBC_SHA,
        SSLSuite.DH_RSA_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.ECDH_RSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.DH_DSS_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.ECDHE_PSK_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_PSK_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.PSK_WITH_AES_256_CCM_8,
        SSLSuite.RSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.ECDH_RSA_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.DHE_RSA_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.DH_RSA_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.KRB5_WITH_IDEA_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DH_RSA_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.PSK_WITH_AES_128_CCM,
        SSLSuite.ECDH_ECDSA_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.RSA_PSK_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.ECDH_RSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.SRP_SHA_DSS_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.DH_DSS_WITH_AES_256_GCM_SHA384,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.RSA_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.RSA_PSK_WITH_AES_128_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.DH_RSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DHE_RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.RSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DH_RSA_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.PSK_DHE_WITH_AES_128_CCM_8,
        SSLSuite.DHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.ECDH_RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.ECDHE_RSA_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.DH_DSS_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.PSK_WITH_CHACHA20_POLY1305_SHA256,
        SSLSuite.RSA_PSK_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.DH_DSS_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.DHE_PSK_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.SRP_SHA_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DH_DSS_WITH_SEED_CBC_SHA,
        SSLSuite.DH_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.PSK_WITH_AES_256_CCM,
        SSLSuite.RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.ECDH_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.PSK_WITH_AES_256_CBC_SHA384,
        SSLSuite.PSK_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_SEED_CBC_SHA,
        SSLSuite.DH_DSS_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.ECDH_ECDSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.PSK_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.RSA_WITH_AES_128_CCM,
        SSLSuite.RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_AES_128_CBC_SHA256,
        SSLSuite.RSA_PSK_WITH_AES_128_GCM_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DH_DSS_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.SRP_SHA_WITH_AES_256_CBC_SHA,
        SSLSuite.PSK_WITH_AES_128_CCM_8,
        SSLSuite.SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_RSA_WITH_SEED_CBC_SHA,
        SSLSuite.ECDHE_PSK_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.ECDH_RSA_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.ECDH_ECDSA_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.DHE_PSK_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.RSA_PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.DH_RSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.SRP_SHA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.DH_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.ECDH_RSA_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.PSK_WITH_AES_128_GCM_SHA256,
        SSLSuite.RSA_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.PSK_WITH_AES_256_GCM_SHA384,
        SSLSuite.DH_RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.DHE_PSK_WITH_AES_256_CBC_SHA,
        SSLSuite.RSA_WITH_AES_256_CBC_SHA256,
        SSLSuite.SRP_SHA_DSS_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_AES_256_CBC_SHA384,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.DH_DSS_WITH_AES_128_GCM_SHA256,
        SSLSuite.DH_DSS_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DHE_PSK_WITH_AES_128_CBC_SHA256,
        SSLSuite.RSA_PSK_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.DH_RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RSA_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.RSA_PSK_WITH_AES_256_GCM_SHA384,
        SSLSuite.PSK_WITH_AES_128_CBC_SHA256,
        SSLSuite.DHE_PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.DH_RSA_WITH_AES_256_CBC_SHA256,
        SSLSuite.RSA_WITH_ARIA_128_GCM_SHA256,
        SSLSuite.ECDHE_PSK_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA384,
        SSLSuite.PSK_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.ECDHE_PSK_WITH_AES_256_CBC_SHA384,
        SSLSuite.PSK_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_AES_256_CBC_SHA256,
        SSLSuite.PSK_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.ECDHE_PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_DSS_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_PSK_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.ECDH_RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.DH_RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.RSA_PSK_WITH_ARIA_128_CBC_SHA256,
        SSLSuite.KRB5_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA384,
        SSLSuite.ECDHE_PSK_WITH_AES_128_CBC_SHA,
        SSLSuite.RSA_WITH_AES_128_CCM_8,
        SSLSuite.ECDHE_PSK_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.RSA_WITH_AES_256_CCM_8,
        SSLSuite.ECDHE_RSA_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.DHE_PSK_WITH_AES_256_CBC_SHA384,
        SSLSuite.SRP_SHA_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_SEED_CBC_SHA,
        SSLSuite.DH_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DH_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.RSA_WITH_IDEA_CBC_SHA,
        SSLSuite.DH_RSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DHE_RSA_WITH_AES_256_CBC_SHA256,
        SSLSuite.RSA_PSK_WITH_AES_256_CBC_SHA,
        SSLSuite.RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.SRP_SHA_WITH_AES_128_CBC_SHA,
        SSLSuite.RSA_WITH_AES_256_CCM,
        SSLSuite.ECDH_ECDSA_WITH_AES_128_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.PSK_DHE_WITH_AES_256_CCM_8,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DH_DSS_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DH_RSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.RSA_PSK_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.RSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DH_RSA_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.PSK_WITH_ARIA_256_CBC_SHA384,
        SSLSuite.DH_DSS_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.PSK_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.ECDH_ECDSA_WITH_AES_256_CBC_SHA384,
        SSLSuite.DH_DSS_WITH_AES_256_CBC_SHA256,
        SSLSuite.ECDH_ECDSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.ECDH_ECDSA_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.PSK_WITH_ARIA_256_GCM_SHA384,
        SSLSuite.RSA_WITH_CAMELLIA_256_CBC_SHA256,
    ]

    for v_id in ctx.tls_versions:
        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                "check if server accepts connections with weak ciphers"
                " in {v_name}".format(v_name=ssl_id2ssl_name(v_id))
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor acepta conexiones con cifrado débil"
                " en {v_name}".format(v_name=ssl_id2ssl_name(v_id))
            ),
        }

        sock = tcp_connect(
            ctx.target.host,
            ctx.target.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            continue

        package = get_client_hello_package(v_id, suites)
        sock.send(bytes(package))
        handshake_record = read_ssl_record(sock)

        if handshake_record is not None:
            handshake_type, _, _ = handshake_record

            if handshake_type == 22:
                ssl_vulnerabilities.append(
                    _create_ssl_vuln(
                        check="weak_ciphers_allowed",
                        line=SSLSnippetLine.ciphers,
                        ssl_settings=SSLSettings(
                            host=ctx.target.host,
                            port=ctx.target.port,
                            min_version=v_id,
                            max_version=v_id,
                            cipher_names=["null", "des", "rc4"],
                            intention=intention,
                        ),
                        finding=core_model.FindingEnum.F052,
                    )
                )

        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _cbc_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    suites: List[SSLSuite] = [
        SSLSuite.RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.RSA_WITH_DES_CBC_SHA,
        SSLSuite.RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_DSS_WITH_DES_CBC_SHA,
        SSLSuite.DH_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_RSA_WITH_DES_CBC_SHA,
        SSLSuite.DH_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_DES_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_DES_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_anon_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_anon_WITH_DES_CBC_SHA,
        SSLSuite.DH_anon_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.KRB5_WITH_DES_CBC_SHA,
        SSLSuite.KRB5_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.KRB5_WITH_DES_CBC_MD5,
        SSLSuite.KRB5_WITH_3DES_EDE_CBC_MD5,
        SSLSuite.KRB5_EXPORT_WITH_DES_CBC_40_SHA,
        SSLSuite.KRB5_EXPORT_WITH_DES_CBC_40_MD5,
        SSLSuite.PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_anon_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.SRP_SHA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RSA_WITH_IDEA_CBC_SHA,
        SSLSuite.KRB5_WITH_IDEA_CBC_SHA,
        SSLSuite.KRB5_WITH_IDEA_CBC_MD5,
        SSLSuite.ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.ECDH_ECDSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.ECDH_ECDSA_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.ECDH_RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.ECDH_RSA_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.RSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.RSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DH_RSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DH_RSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DH_DSS_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DH_DSS_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DH_anon_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DH_anon_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.ECDHE_ECDSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.ECDH_ECDSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.ECDH_ECDSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.ECDHE_RSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.ECDHE_RSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.ECDH_RSA_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.ECDH_RSA_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.PSK_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.PSK_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.DHE_PSK_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.DHE_PSK_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.RSA_PSK_WITH_CAMELLIA_128_GCM_SHA256,
        SSLSuite.RSA_PSK_WITH_CAMELLIA_256_GCM_SHA384,
        SSLSuite.PSK_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.PSK_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.DHE_PSK_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DHE_PSK_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.RSA_PSK_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.RSA_PSK_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.ECDHE_PSK_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.ECDHE_PSK_WITH_CAMELLIA_256_CBC_SHA384,
        SSLSuite.RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DH_DSS_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DH_RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.DH_anon_WITH_CAMELLIA_128_CBC_SHA256,
        SSLSuite.RSA_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.DH_DSS_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.DH_RSA_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.DH_anon_WITH_CAMELLIA_256_CBC_SHA256,
        SSLSuite.RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DH_DSS_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DH_RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DH_anon_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DH_DSS_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DH_RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DH_anon_WITH_CAMELLIA_128_CBC_SHA,
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()

    for v_id in ctx.tls_versions:
        if v_id == SSLVersionId.tlsv1_3:
            continue

        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                "check if server accepts connections with ciphers that use"
                " CBC in {v_name}".format(v_name=ssl_id2ssl_name(v_id))
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor soporta cifrado con CBC"
                " en {v_name}".format(v_name=ssl_id2ssl_name(v_id))
            ),
        }

        sock = tcp_connect(
            ctx.target.host,
            ctx.target.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            return tuple()

        package = get_client_hello_package(v_id, suites, extensions)
        sock.send(bytes(package))
        handshake_record = read_ssl_record(sock)

        if handshake_record is not None:
            handshake_type, _, _ = handshake_record

            if handshake_type == 22:
                ssl_vulnerabilities.append(
                    _create_ssl_vuln(
                        check="cbc_enabled",
                        line=SSLSnippetLine.ciphers,
                        ssl_settings=SSLSettings(
                            host=ctx.target.host,
                            port=ctx.target.port,
                            min_version=v_id,
                            max_version=v_id,
                            cipher_names=["3des", "camellia", "idea"],
                            intention=intention,
                        ),
                        finding=core_model.FindingEnum.F094,
                    )
                )

        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _sweet32_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    suites: List[SSLSuite] = [
        SSLSuite.RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.RSA_WITH_DES_CBC_SHA,
        SSLSuite.RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_DSS_WITH_DES_CBC_SHA,
        SSLSuite.DH_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_RSA_WITH_DES_CBC_SHA,
        SSLSuite.DH_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_DES_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_DES_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DH_anon_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DH_anon_WITH_DES_CBC_SHA,
        SSLSuite.DH_anon_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.KRB5_WITH_DES_CBC_SHA,
        SSLSuite.KRB5_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.KRB5_WITH_DES_CBC_MD5,
        SSLSuite.KRB5_WITH_3DES_EDE_CBC_MD5,
        SSLSuite.KRB5_EXPORT_WITH_DES_CBC_40_SHA,
        SSLSuite.KRB5_EXPORT_WITH_DES_CBC_40_MD5,
        SSLSuite.PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RSA_PSK_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_anon_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.SRP_SHA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_PSK_WITH_3DES_EDE_CBC_SHA,
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()

    for v_id in ctx.tls_versions:
        if v_id == SSLVersionId.tlsv1_3:
            continue

        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                "check if server is vulnerable to SWEET32 attacks"
                " in {v_name}".format(v_name=ssl_id2ssl_name(v_id))
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor es vulnerable a ataques SWEET32"
                " en {v_name}".format(v_name=ssl_id2ssl_name(v_id))
            ),
        }

        sock = tcp_connect(
            ctx.target.host,
            ctx.target.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            return tuple()

        package = get_client_hello_package(v_id, suites, extensions)
        sock.send(bytes(package))
        handshake_record = read_ssl_record(sock)

        if handshake_record is not None:
            handshake_type, _, _ = handshake_record

            if handshake_type == 22:
                ssl_vulnerabilities.append(
                    _create_ssl_vuln(
                        check="sweet32_possible",
                        line=SSLSnippetLine.ciphers,
                        ssl_settings=SSLSettings(
                            host=ctx.target.host,
                            port=ctx.target.port,
                            min_version=v_id,
                            max_version=v_id,
                            cipher_names=["3des"],
                            intention=intention,
                        ),
                        finding=core_model.FindingEnum.F094,
                    )
                )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _fallback_scsv_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    if len(ctx.tls_versions) < 2:
        return tuple()

    suites: List[SSLSuite] = [
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.ECDHE_RSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.DHE_RSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,
        SSLSuite.ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,
        SSLSuite.DHE_RSA_WITH_CHACHA20_POLY1305_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.ECDHE_RSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.DHE_RSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA384,
        SSLSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA384,
        SSLSuite.DHE_RSA_WITH_AES_256_CBC_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.RSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.RSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.RSA_WITH_AES_256_CBC_SHA256,
        SSLSuite.RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.FALLBACK_SCSV,
    ]

    min_v_id: SSLVersionId = min(ctx.tls_versions)

    intention: Dict[core_model.LocalesEnum, str] = {
        core_model.LocalesEnum.EN: (
            "check if server supports TLS_FALLBACK_SCSV"
        ),
        core_model.LocalesEnum.ES: (
            "verificar si el servidor soporta TLS_FALLBACK_SCSV"
        ),
    }

    sock = tcp_connect(
        ctx.target.host,
        ctx.target.port,
        intention[core_model.LocalesEnum.EN],
    )

    if sock is None:
        return tuple()

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()

    package = get_client_hello_package(min_v_id, suites, extensions)
    sock.send(bytes(package))
    handshake_record = read_ssl_record(sock)

    if handshake_record is not None:
        handshake_type, _, _ = handshake_record

        if handshake_type == 22:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="fallback_scsv_disabled",
                    line=SSLSnippetLine.min_version,
                    ssl_settings=SSLSettings(
                        host=ctx.target.host,
                        port=ctx.target.port,
                        min_version=min_v_id,
                        max_version=min_v_id,
                        intention=intention,
                    ),
                    finding=core_model.FindingEnum.F016,
                )
            )
    sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_3_downgrade(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    if SSLVersionId.tlsv1_3 not in ctx.tls_versions:
        return tuple()

    for v_id in ctx.tls_versions:
        if v_id in (SSLVersionId.tlsv1_2, SSLVersionId.tlsv1_3):
            continue

        v_name: str = ssl_id2ssl_name(v_id)
        ssl_settings = SSLSettings(
            ctx.target.host,
            ctx.target.port,
            min_version=v_id,
            max_version=v_id,
            intention={
                core_model.LocalesEnum.EN: (
                    "check if TLSv1.3 can be downgraded to {v_name}".format(
                        v_name=v_name
                    )
                ),
                core_model.LocalesEnum.ES: (
                    "verificar si TLSv1.3 puede degradarse a {v_name}".format(
                        v_name=v_name
                    )
                ),
            },
        )

        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                check="tlsv1_3_downgrade",
                ssl_settings=ssl_settings,
                line=SSLSnippetLine.max_version,
                finding=core_model.FindingEnum.F016,
                check_kwargs={"version": v_name},
            )
        )

    return _create_core_vulns(ssl_vulnerabilities)


def _heartbleed_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    suites: List[SSLSuite] = [
        SSLSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA,
        SSLSuite.SRP_SHA_DSS_WITH_AES_256_CBC_SHA,
        SSLSuite.SRP_SHA_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_AES_256_CBC_SHA,
        SSLSuite.RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.RSA_WITH_CAMELLIA_256_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.RSA_WITH_3DES_EDE_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA,
        SSLSuite.SRP_SHA_DSS_WITH_AES_128_CBC_SHA,
        SSLSuite.SRP_SHA_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_SEED_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_SEED_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.ECDH_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.ECDH_ECDSA_WITH_AES_128_CBC_SHA,
        SSLSuite.RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.RSA_WITH_SEED_CBC_SHA,
        SSLSuite.RSA_WITH_CAMELLIA_128_CBC_SHA,
        SSLSuite.ECDHE_RSA_WITH_RC4_128_SHA,
        SSLSuite.ECDHE_ECDSA_WITH_RC4_128_SHA,
        SSLSuite.ECDH_RSA_WITH_RC4_128_SHA,
        SSLSuite.ECDH_ECDSA_WITH_RC4_128_SHA,
        SSLSuite.RSA_WITH_RC4_128_SHA,
        SSLSuite.RSA_WITH_RC4_128_MD5,
        SSLSuite.DHE_RSA_WITH_DES_CBC_SHA,
        SSLSuite.DHE_DSS_WITH_DES_CBC_SHA,
        SSLSuite.RSA_WITH_DES_CBC_SHA,
        SSLSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5,
        SSLSuite.RSA_EXPORT_WITH_RC4_40_MD5,
        SSLSuite.EMPTY_RENEGOTIATION_INFO_SCSV,
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()
    extensions += get_heartbeat_ext()

    for v_id in ctx.tls_versions:
        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                "check if server is vulnerable to heartbleed attack with"
                " {v_name}".format(
                    v_name=ssl_id2ssl_name(v_id),
                )
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor es vulnerable a un ataque heartbleed"
                "con {v_name}".format(
                    v_name=ssl_id2ssl_name(v_id),
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

        package = get_client_hello_package(v_id, suites, extensions)
        sock.send(bytes(package))
        handshake_record = read_ssl_record(sock)

        if handshake_record is not None:
            handshake_type, _, _ = handshake_record

            if handshake_type == 22:
                package = get_malicious_heartbeat(v_id, n_payload=16384)
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
                                    min_version=v_id,
                                    max_version=v_id,
                                    intention=intention,
                                ),
                                finding=core_model.FindingEnum.F016,
                            )
                        )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _freak_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    suites: List[SSLSuite] = [
        SSLSuite.RESERVED_SUITE_00_62,
        SSLSuite.RESERVED_SUITE_00_61,
        SSLSuite.RESERVED_SUITE_00_64,
        SSLSuite.RESERVED_SUITE_00_60,
        SSLSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.RSA_EXPORT_WITH_DES40_CBC_SHA,
        SSLSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5,
        SSLSuite.RSA_EXPORT_WITH_RC4_40_MD5,
        SSLSuite.EMPTY_RENEGOTIATION_INFO_SCSV,
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()
    extensions += get_heartbeat_ext()

    for v_id in ctx.tls_versions:
        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                "check if server is vulnerable to FREAK attack with"
                " {v_name}".format(
                    v_name=ssl_id2ssl_name(v_id),
                )
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor es vulnerable a un ataque FREAK"
                " con {v_name}".format(
                    v_name=ssl_id2ssl_name(v_id),
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

        package = get_client_hello_package(v_id, suites, extensions)
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
                            min_version=v_id,
                            max_version=v_id,
                            intention=intention,
                        ),
                        finding=core_model.FindingEnum.F016,
                    )
                )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _raccoon_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    suites: List[SSLSuite] = [
        SSLSuite.DHE_RSA_WITH_CHACHA20_POLY1305_SHA256,
        SSLSuite.DHE_RSA_WITH_AES_256_GCM_SHA384,
        SSLSuite.DHE_RSA_WITH_AES_128_GCM_SHA256,
        SSLSuite.DHE_RSA_WITH_AES_256_CCM,
        SSLSuite.DHE_RSA_WITH_AES_128_CCM,
        SSLSuite.DHE_RSA_WITH_AES_256_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_AES_128_CBC_SHA256,
        SSLSuite.DHE_RSA_WITH_AES_256_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_AES_128_CBC_SHA,
        SSLSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA,
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()
    extensions += get_heartbeat_ext()

    for v_id in ctx.tls_versions:
        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                "check if server is vulnerable to RACCOON attack with"
                " {v_name}".format(
                    v_name=ssl_id2ssl_name(v_id),
                )
            ),
            core_model.LocalesEnum.ES: (
                "verificar si el servidor es vulnerable a un ataque RACCOON"
                " con {v_name}".format(
                    v_name=ssl_id2ssl_name(v_id),
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

        package = get_client_hello_package(v_id, suites, extensions)
        sock.send(bytes(package))
        handshake_record = read_ssl_record(sock)

        if handshake_record is not None:
            handshake_type, _, _ = handshake_record

            if handshake_type == 22:
                ssl_vulnerabilities.append(
                    _create_ssl_vuln(
                        check="raccoon_possible",
                        line=SSLSnippetLine.max_version,
                        ssl_settings=SSLSettings(
                            ctx.target.host,
                            ctx.target.port,
                            min_version=v_id,
                            max_version=v_id,
                            intention=intention,
                        ),
                        finding=core_model.FindingEnum.F016,
                    )
                )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _breach_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    url: str = f"https://{ctx}"
    common_compressors: List[str] = [
        "compress",
        "exi",
        "gzip",
        "identity",
        "pack200-gzip",
        "br",
        "bzip2",
        "lzma",
        "peerdist",
        "sdch",
        "xpress",
        "xz",
    ]

    for compression in common_compressors:
        response = request_blocking(
            url=url,
            headers={"Accept-Encoding": f"{compression},deflate"},
        )

        if response is None:
            continue

        if compression in response.headers.get("Content-Encoding", ""):
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="breach_possible",
                    line=SSLSnippetLine.ssl_connection,
                    ssl_settings=SSLSettings(
                        ctx.target.host,
                        ctx.target.port,
                        intention={
                            core_model.LocalesEnum.EN: (
                                "check if server is vulnerable to BREACH"
                                " attack with {compression} as encoding"
                                " method".format(
                                    compression=compression,
                                )
                            ),
                            core_model.LocalesEnum.ES: (
                                "verificar si el servidor es vulnerable a un"
                                " ataque BREACH al usar {compression} como"
                                " método de codificación".format(
                                    compression=compression,
                                )
                            ),
                        },
                    ),
                    finding=core_model.FindingEnum.F016,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


CHECKS: Dict[
    core_model.FindingEnum,
    List[Callable[[SSLContext], core_model.Vulnerabilities]],
] = {
    core_model.FindingEnum.F052: [_weak_ciphers_allowed],
    core_model.FindingEnum.F094: [
        _cbc_enabled,
        _sweet32_possible,
    ],
    core_model.FindingEnum.F133: [_pfs_disabled],
    core_model.FindingEnum.F016: [
        _sslv3_enabled,
        _tlsv1_enabled,
        _tlsv1_1_enabled,
        _tlsv1_2_or_higher_disabled,
        _fallback_scsv_disabled,
        _tlsv1_3_downgrade,
        _heartbleed_possible,
        _freak_possible,
        _raccoon_possible,
        _breach_possible,
    ],
}
