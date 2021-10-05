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
    parse_server_response,
    read_ssl_record,
    ssl_connect,
)
from lib_ssl.suites import (
    get_suite_by_openssl_name,
    get_suites_with_cbc,
    get_suites_with_pfs,
    get_weak_suites,
    SSLCipherSuite,
    SSLSpecialSuite,
    SSLSuiteInfo,
    SSLVersionId,
)
from lib_ssl.types import (
    SSLContext,
    SSLHandshakeRecord,
    SSLRecord,
    SSLServerHandshake,
    SSLServerResponse,
    SSLSettings,
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
    Tuple,
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


def tls_connect(
    host: str, port: int, v_id: SSLVersionId
) -> Optional[SSLServerResponse]:
    intention_en = "verify if server supports " + ssl_id2ssl_name(v_id)
    ssl_settings = SSLSettings(
        context=SSLContext(host=host, port=port),
        tls_version=v_id,
        intention={core_model.LocalesEnum.EN: intention_en},
    )

    with ssl_connect(ssl_settings) as ssl_socket:
        if ssl_socket is not None and (cipher_info := ssl_socket.cipher()):
            openssl_name, _, _ = cipher_info
            return SSLServerResponse(
                record=SSLRecord.HANDSHAKE,
                version_id=v_id,
                handshake=SSLServerHandshake(
                    record=SSLHandshakeRecord.SERVER_HELLO,
                    version_id=v_id,
                    cipher_suite=get_suite_by_openssl_name(openssl_name),
                ),
            )
    return None


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
            what=str(ssl_vulnerability),
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
    ssl_settings: SSLSettings,
    server_response: Optional[SSLServerResponse],
    finding: core_model.FindingEnum,
    check_kwargs: Optional[Dict[str, str]] = None,
) -> SSLVulnerability:
    return SSLVulnerability(
        finding=finding,
        ssl_settings=ssl_settings,
        server_response=server_response,
        description=t(
            f"lib_ssl.analyze_protocol.{check}", **(check_kwargs or {})
        ),
    )


def _pfs_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    suites: List[SSLSuiteInfo] = list(get_suites_with_pfs())

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()

    en_intention = (
        "Perform a {v_name} request offering only key exchange algorithms\n"
        "with PFS support and check if the connection is accepted by the\n"
        "server"
    )

    es_intention = (
        "Realizar una petición {v_name} ofreciendo únicamente algoritmos\n"
        "de intercambio de llaves con soporte PFS y verificar si la conexión\n"
        "es aceptada por el servidor"
    )

    for v_id in tls_versions:
        if v_id == SSLVersionId.tlsv1_3:
            continue

        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core_model.LocalesEnum.ES: (
                es_intention.format(
                    v_name=ssl_id2ssl_name(v_id),
                )
            ),
        }

        sock = tcp_connect(
            ctx.host,
            ctx.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            break

        package = get_client_hello_package(v_id, suites, extensions)
        sock.send(bytes(package))
        response: Optional[SSLServerResponse] = parse_server_response(sock)

        if response is not None and response.alert is not None:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="pfs_disabled",
                    ssl_settings=SSLSettings(
                        context=ctx,
                        tls_version=v_id,
                        key_exchange_names=[
                            "DHE",
                            "ECDHE",
                            "SRP",
                            "ECCPWD",
                        ],
                        intention=intention,
                    ),
                    server_response=response,
                    finding=core_model.FindingEnum.F133,
                )
            )

        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _sslv3_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []

    suites: List[SSLSuiteInfo] = [
        SSLCipherSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.ECDH_anon_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.RSA_PSK_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.ECDH_anon_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_IDEA_CBC_SHA.value,
        SSLCipherSuite.RSA_PSK_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_RC4_128_SHA.value,
        SSLSpecialSuite.RESERVED_SUITE_00_66.value,
        SSLCipherSuite.ECDH_anon_WITH_RC4_128_SHA.value,
        SSLCipherSuite.DH_anon_WITH_RC4_128_MD5.value,
        SSLCipherSuite.ECDH_RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.RSA_WITH_RC4_128_MD5.value,
        SSLCipherSuite.RSA_PSK_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDH_anon_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.RSA_PSK_WITH_3DES_EDE_CBC_SHA.value,
        SSLSpecialSuite.RESERVED_SUITE_00_63.value,
        SSLCipherSuite.DHE_RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_DES_CBC_SHA.value,
        SSLSpecialSuite.RESERVED_SUITE_00_62.value,
        SSLCipherSuite.RSA_WITH_DES_CBC_SHA.value,
        SSLSpecialSuite.RESERVED_SUITE_00_61.value,
        SSLSpecialSuite.RESERVED_SUITE_00_65.value,
        SSLSpecialSuite.RESERVED_SUITE_00_64.value,
        SSLSpecialSuite.RESERVED_SUITE_00_60.value,
        SSLCipherSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DH_anon_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5.value,
        SSLCipherSuite.DH_anon_EXPORT_WITH_RC4_40_MD5.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC4_40_MD5.value,
        SSLCipherSuite.ECDHE_RSA_WITH_NULL_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_NULL_SHA.value,
        SSLCipherSuite.ECDH_anon_WITH_NULL_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_NULL_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_NULL_SHA.value,
        SSLCipherSuite.RSA_WITH_NULL_SHA.value,
        SSLCipherSuite.RSA_WITH_NULL_MD5.value,
        SSLSpecialSuite.EMPTY_RENEGOTIATION_INFO_SCSV.value,
    ]

    en_intention = (
        "Perform a SSLv3 request offering any cipher suite and check if the\n"
        "connection is accepted by the server"
    )

    es_intention = (
        "Realizar una petición SSLv3 ofreciendo cualquier suite de cifrado\n"
        "y verificar si la conexión es aceptada por el servidor"
    )

    intention: Dict[core_model.LocalesEnum, str] = {
        core_model.LocalesEnum.EN: en_intention,
        core_model.LocalesEnum.ES: es_intention,
    }

    sock = tcp_connect(
        ctx.host,
        ctx.port,
        intention[core_model.LocalesEnum.EN],
    )

    if sock is None:
        return tuple()

    package = get_client_hello_package(SSLVersionId.sslv3_0, suites)
    sock.send(bytes(package))
    response: Optional[SSLServerResponse] = parse_server_response(sock)

    if response is not None and response.handshake is not None:
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                check="sslv3_enabled",
                ssl_settings=SSLSettings(
                    context=ctx,
                    tls_version=SSLVersionId.sslv3_0,
                    intention=intention,
                ),
                server_response=response,
                finding=core_model.FindingEnum.F016,
            )
        )
    sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    en_intention = (
        "Perform a TLSv1.0 request offering any cipher suite and check if\n"
        "the server accepts the connection"
    )

    es_intention = (
        "Realizar una petición TLSv1.0 ofreciendo cualquier suite de\n"
        "cifrado y verificar si el servidor acepta la conexión"
    )

    if SSLVersionId.tlsv1_0 in tls_versions:
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                check="tlsv1_enabled",
                ssl_settings=SSLSettings(
                    context=ctx,
                    tls_version=SSLVersionId.tlsv1_0,
                    intention={
                        core_model.LocalesEnum.EN: en_intention,
                        core_model.LocalesEnum.ES: es_intention,
                    },
                ),
                server_response=ctx.get_tls_response(SSLVersionId.tlsv1_0),
                finding=core_model.FindingEnum.F016,
            )
        )

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_1_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    en_intention = (
        "Perform a TLSv1.1 request offering any cipher suite and check if\n"
        "the server accepts the connection"
    )

    es_intention = (
        "Realizar una petición TLSv1.1 ofreciendo cualquier suite de\n"
        "cifrado y verificar si el servidor acepta la conexión"
    )

    if SSLVersionId.tlsv1_1 in tls_versions:
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                check="tlsv1_1_enabled",
                ssl_settings=SSLSettings(
                    context=ctx,
                    tls_version=SSLVersionId.tlsv1_1,
                    intention={
                        core_model.LocalesEnum.EN: en_intention,
                        core_model.LocalesEnum.ES: es_intention,
                    },
                ),
                server_response=ctx.get_tls_response(SSLVersionId.tlsv1_1),
                finding=core_model.FindingEnum.F016,
            )
        )

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_2_or_higher_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    if not tls_versions:
        return tuple()

    en_intention = (
        "Perform a request offering any cipher suite on versions TLSv1.2 or\n"
        "TLSv1.3 and check if the server accepts the connection"
    )

    es_intention = (
        "Realizar una petición ofreciendo cualquier suite de cifrado con\n"
        "las versiones TLSv1.2 o TLSv1.3 y verificar si el servidor acepta\n"
        "la conexión"
    )

    if (
        SSLVersionId.tlsv1_2 not in tls_versions
        and SSLVersionId.tlsv1_3 not in tls_versions
    ):
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                check="tlsv1_2_or_higher_disabled",
                ssl_settings=SSLSettings(
                    context=ctx,
                    tls_version=SSLVersionId.tlsv1_3,
                    intention={
                        core_model.LocalesEnum.EN: en_intention,
                        core_model.LocalesEnum.ES: es_intention,
                    },
                ),
                server_response=None,
                finding=core_model.FindingEnum.F016,
            )
        )

    return _create_core_vulns(ssl_vulnerabilities)


def _weak_ciphers_allowed(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    suites: List[SSLSuiteInfo] = list(get_weak_suites())

    en_intention = (
        "Perform a {v_name} request offering only weak cipher suites and\n"
        "check if the connection is accepted by the server"
    )

    es_intention = (
        "Realizar una petición {v_name} ofreciendo solamente suites de\n"
        "cifrado débiles y verificar si la conexión es aceptada por el\n"
        "servidor"
    )

    for v_id in tls_versions:
        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core_model.LocalesEnum.ES: (
                es_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
        }

        sock = tcp_connect(
            ctx.host,
            ctx.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            continue

        package = get_client_hello_package(v_id, suites)
        sock.send(bytes(package))
        response: Optional[SSLServerResponse] = parse_server_response(sock)

        if response is not None and response.handshake is not None:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="weak_ciphers_allowed",
                    ssl_settings=SSLSettings(
                        context=ctx,
                        tls_version=v_id,
                        cipher_names=[
                            "NULL",
                            "RC2",
                            "RC4",
                            "DES",
                            "DES3",
                            "SM3",
                            "SM4",
                            "CBC",
                        ],
                        hash_names=[
                            "SHA",
                            "MD5",
                            "SM3",
                        ],
                        intention=intention,
                    ),
                    server_response=response,
                    finding=core_model.FindingEnum.F052,
                )
            )

        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _cbc_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    suites: List[SSLSuiteInfo] = list(get_suites_with_cbc())

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()

    en_intention = (
        "Perform a {v_name} request offering any cipher suite \n"
        "and check if the connection is accepted by the server"
    )

    es_intention = (
        "Realizar una petición {v_name} ofreciendo solamente suites de\n"
        "cifrado que usen CBC y verificar si la conexión es aceptada por el\n"
        "servidor"
    )

    for v_id in tls_versions:
        if v_id == SSLVersionId.tlsv1_3:
            continue

        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core_model.LocalesEnum.ES: (
                es_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
        }

        sock = tcp_connect(
            ctx.host,
            ctx.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            return tuple()

        package = get_client_hello_package(v_id, suites, extensions)
        sock.send(bytes(package))
        response: Optional[SSLServerResponse] = parse_server_response(sock)

        if response is not None and response.handshake is not None:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="cbc_enabled",
                    ssl_settings=SSLSettings(
                        context=ctx,
                        tls_version=v_id,
                        cipher_names=["CBC"],
                        intention=intention,
                    ),
                    server_response=response,
                    finding=core_model.FindingEnum.F094,
                )
            )

        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _fallback_scsv_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    if len(tls_versions) < 2:
        return tuple()

    suites: List[SSLSuiteInfo] = [
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_256_GCM_SHA384.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_256_GCM_SHA384.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_GCM_SHA384.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256.value,
        SSLCipherSuite.ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256.value,
        SSLCipherSuite.DHE_RSA_WITH_CHACHA20_POLY1305_SHA256.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_128_GCM_SHA256.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_128_GCM_SHA256.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_GCM_SHA256.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA384.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA384.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CBC_SHA256.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA256.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA256.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CBC_SHA256.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_256_GCM_SHA384.value,
        SSLCipherSuite.RSA_WITH_AES_128_GCM_SHA256.value,
        SSLCipherSuite.RSA_WITH_AES_256_CBC_SHA256.value,
        SSLCipherSuite.RSA_WITH_AES_128_CBC_SHA256.value,
        SSLCipherSuite.RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_128_CBC_SHA.value,
        SSLSpecialSuite.FALLBACK_SCSV.value,
    ]

    min_v_id: SSLVersionId = min(tls_versions)

    en_intention = (
        "Perform a request with the lower TLS version supported by the\n"
        "server with the TLS_FALLBACK_SCSV parameter set on true and check\n"
        "if the server accept the connection"
    )

    es_intention = (
        "Realizar una petición con la menor versión de TLS soportada por el\n"
        "servidor con el paremtro TLS_FALLBACK_SCSV activado y verificar si\n"
        "el servidor acepta la conexión"
    )

    intention: Dict[core_model.LocalesEnum, str] = {
        core_model.LocalesEnum.EN: en_intention,
        core_model.LocalesEnum.ES: es_intention,
    }

    sock = tcp_connect(
        ctx.host,
        ctx.port,
        intention[core_model.LocalesEnum.EN],
    )

    if sock is None:
        return tuple()

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()

    package = get_client_hello_package(min_v_id, suites, extensions)
    sock.send(bytes(package))
    response: Optional[SSLServerResponse] = parse_server_response(sock)

    if response is not None and response.handshake is not None:
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                check="fallback_scsv_disabled",
                ssl_settings=SSLSettings(
                    context=ctx,
                    tls_version=min_v_id,
                    intention=intention,
                ),
                server_response=response,
                finding=core_model.FindingEnum.F016,
            )
        )
    sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _tlsv1_3_downgrade(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    if SSLVersionId.tlsv1_3 not in tls_versions:
        return tuple()

    en_intention = (
        "Perform a {v_name} request offering any cipher suite to check if\n"
        "the connection is accepted by the server, meaning that a downgrade\n"
        "from TLSv1.3 is possible"
    )

    es_intention = (
        "Realizar una petición {v_name} ofreciendo cualquier suite de\n"
        "cifrado para verificar si la conexión es aceptada por el servidor,\n"
        "lo cual significaria que TLSv1.3 puede ser degradado"
    )

    for v_id in tls_versions:
        if v_id in (SSLVersionId.tlsv1_2, SSLVersionId.tlsv1_3):
            continue

        v_name: str = ssl_id2ssl_name(v_id)
        ssl_settings = SSLSettings(
            context=ctx,
            tls_version=v_id,
            intention={
                core_model.LocalesEnum.EN: en_intention.format(v_name=v_name),
                core_model.LocalesEnum.ES: es_intention.format(v_name=v_name),
            },
        )

        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                check="tlsv1_3_downgrade",
                ssl_settings=ssl_settings,
                server_response=ctx.get_tls_response(v_id),
                finding=core_model.FindingEnum.F016,
                check_kwargs={"version": v_name},
            )
        )

    return _create_core_vulns(ssl_vulnerabilities)


def _heartbleed_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    suites: List[SSLSuiteInfo] = [
        SSLCipherSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_DSS_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_DSS_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.RSA_WITH_RC4_128_MD5.value,
        SSLCipherSuite.DHE_RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC4_40_MD5.value,
        SSLSpecialSuite.EMPTY_RENEGOTIATION_INFO_SCSV.value,
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()
    extensions += get_heartbeat_ext()

    en_intention = (
        "Perform a {v_name} request offering any cipher suite and check if\n"
        "the server is vulnerable to a heartbleed attack"
    )

    es_intention = (
        "Realizar una petición {v_name} ofreciendo cualquier suite de\n"
        "cifrado y verificar si el servidor es vulnerable a un ataque\n"
        "heartbleed"
    )

    for v_id in tls_versions:
        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core_model.LocalesEnum.ES: (
                es_intention.format(
                    v_name=ssl_id2ssl_name(v_id),
                )
            ),
        }

        sock = tcp_connect(
            ctx.host,
            ctx.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            break

        package = get_client_hello_package(v_id, suites, extensions)
        sock.send(bytes(package))
        response: Optional[SSLServerResponse] = parse_server_response(sock)

        if response is not None and response.handshake is not None:
            package = get_malicious_heartbeat(v_id, n_payload=16384)
            sock.send(bytes(package))

            heartbeat_record = read_ssl_record(sock)

            if heartbeat_record is not None:
                heartbeat_type, _, _ = heartbeat_record

                if heartbeat_type == 24:
                    ssl_vulnerabilities.append(
                        _create_ssl_vuln(
                            check="heartbleed_possible",
                            ssl_settings=SSLSettings(
                                context=ctx,
                                tls_version=v_id,
                                intention=intention,
                            ),
                            server_response=response,
                            finding=core_model.FindingEnum.F016,
                        )
                    )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _freak_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    suites: List[SSLSuiteInfo] = [
        SSLSpecialSuite.RESERVED_SUITE_00_62.value,
        SSLSpecialSuite.RESERVED_SUITE_00_61.value,
        SSLSpecialSuite.RESERVED_SUITE_00_64.value,
        SSLSpecialSuite.RESERVED_SUITE_00_60.value,
        SSLCipherSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC4_40_MD5.value,
        SSLSpecialSuite.EMPTY_RENEGOTIATION_INFO_SCSV.value,
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()
    extensions += get_heartbeat_ext()

    en_intention = (
        "Check if server is vulnerable to FREAK attack with {v_name}"
    )

    es_intention = (
        "Verificar si el servidor es vulnerable a ataques FREAK en {v_name}"
    )

    for v_id in tls_versions:
        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core_model.LocalesEnum.ES: (
                es_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
        }

        sock = tcp_connect(
            ctx.host,
            ctx.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            break

        package = get_client_hello_package(v_id, suites, extensions)
        sock.send(bytes(package))
        response: Optional[SSLServerResponse] = parse_server_response(sock)

        if response is not None and response.handshake is not None:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="freak_possible",
                    ssl_settings=SSLSettings(
                        context=ctx,
                        tls_version=v_id,
                        key_exchange_names=["RSA"],
                        intention=intention,
                    ),
                    server_response=response,
                    finding=core_model.FindingEnum.F016,
                )
            )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities)


def _raccoon_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    ssl_vulnerabilities: List[SSLVulnerability] = []
    tls_versions: Tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    suites: List[SSLSuiteInfo] = [
        SSLCipherSuite.DHE_RSA_WITH_CHACHA20_POLY1305_SHA256.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_GCM_SHA384.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_GCM_SHA256.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CCM.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CCM.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CBC_SHA256.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CBC_SHA256.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA.value,
    ]

    extensions: List[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()
    extensions += get_heartbeat_ext()

    en_intention = (
        "check if server is vulnerable to RACCOON attack with {v_name}"
    )

    es_intention = (
        "verificar si el servidor es vulnerable a un ataque RACCOON - {v_name}"
    )

    for v_id in tls_versions:
        intention: Dict[core_model.LocalesEnum, str] = {
            core_model.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core_model.LocalesEnum.ES: (
                es_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
        }

        sock = tcp_connect(
            ctx.host,
            ctx.port,
            intention[core_model.LocalesEnum.EN],
        )

        if sock is None:
            break

        package = get_client_hello_package(v_id, suites, extensions)
        sock.send(bytes(package))
        response: Optional[SSLServerResponse] = parse_server_response(sock)

        if response is not None and response.handshake is not None:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    check="raccoon_possible",
                    ssl_settings=SSLSettings(
                        context=ctx,
                        tls_version=v_id,
                        key_exchange_names=["DHE"],
                        authentication_names=["RSA"],
                        intention=intention,
                    ),
                    server_response=response,
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

    en_intention = (
        "check if server is vulnerable to BREACH attack with {compression}\n"
        "as encoding method"
    )

    es_intention = (
        "verificar si el servidor es vulnerable a un ataque BREACH al usar\n"
        "{compression} como método de codificación"
    )

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
                    ssl_settings=SSLSettings(
                        context=ctx,
                        intention={
                            core_model.LocalesEnum.EN: (
                                en_intention.format(compression=compression)
                            ),
                            core_model.LocalesEnum.ES: (
                                es_intention.format(compression=compression)
                            ),
                        },
                    ),
                    server_response=None,
                    finding=core_model.FindingEnum.F016,
                )
            )

    return _create_core_vulns(ssl_vulnerabilities)


CHECKS: Dict[
    core_model.FindingEnum,
    List[Callable[[SSLContext], core_model.Vulnerabilities]],
] = {
    core_model.FindingEnum.F052: [_weak_ciphers_allowed],
    core_model.FindingEnum.F094: [_cbc_enabled],
    core_model.FindingEnum.F133: [_pfs_disabled],
    core_model.FindingEnum.F016: [
        _sslv3_enabled,
        _tlsv1_enabled,
        _tlsv1_1_enabled,
        _tlsv1_2_or_higher_disabled,
        _fallback_scsv_disabled,
        _tlsv1_3_downgrade,
        _heartbleed_possible,
    ],
}
