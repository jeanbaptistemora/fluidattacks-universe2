from lib_ssl.as_string import (
    snippet,
    ssl_versions,
)
from lib_ssl.ssl_connection import (
    connect,
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
        intention="check if server accepts key_exchange with PFS support",
        key_exchange_names=["dhe_rsa", "ecdhe_rsa", "ecdh_anon", "dh_anon"],
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
        intention="check if server supports SSLv3",
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
        intention="check if server supports TLSv1.0",
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
        intention="check if server supports TLSv1.1",
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
        intention="check if server supports TLSv1.3",
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
        intention="check if server supports anonymous cipher suits",
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
        intention="check if server supports weak ciphers",
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
        intention="check if server is vulnerable to BEAST attacks",
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
        intention="check if server supports CBC",
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
        intention="check if server is vulnerable to SWEET32 attacks",
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
        intention=f"check if server supports {ssl_versions[version]}",
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
        intention="check if server supports TLS_FALLBACK_SCSV",
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
            intention=f"check TLSv1.3 downgrade to {ssl_versions[version]}",
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
    ],
}
