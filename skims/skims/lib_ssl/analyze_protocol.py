from lib_ssl.as_string import (
    snippet,
    ssl_versions,
    SSLSnippetLine,
)
from lib_ssl.ssl_connection import (
    connect,
)
from lib_ssl.types import (
    SSLContext,
    SSLSettings,
)
from model import (
    core_model,
)
import tlslite
from typing import (
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)
from utils.ctx import (
    CTX,
)
from zone import (
    t,
)


class Location(NamedTuple):
    description: str


class Locations(NamedTuple):
    locations: List[Location]

    def append(
        self,
        desc: str,
        desc_kwargs: Optional[Dict[str, str]] = None,
    ) -> None:
        self.locations.append(
            Location(
                description=t(
                    f"lib_ssl.analyze_protocol.{desc}",
                    **(desc_kwargs or {}),
                ),
            )
        )


# pylint: disable=too-many-arguments
def _create_vulns(
    locations: Locations,
    finding: core_model.FindingEnum,
    ctx: SSLContext,
    conn_established: bool,
    line: SSLSnippetLine,
    ssl_settings: SSLSettings,
) -> core_model.Vulnerabilities:
    return tuple(
        core_model.Vulnerability(
            finding=finding,
            kind=core_model.VulnerabilityKindEnum.INPUTS,
            namespace=CTX.config.namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            stream="home,socket-send,socket-response",
            what=f"{ctx.target.host}:{ctx.target.port}",
            where=location.description,
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=(finding.value.cwe,),
                description=location.description,
                snippet=snippet(
                    host=ctx.target.host,
                    port=ctx.target.port,
                    conn_established=conn_established,
                    line=line,
                    ssl_settings=ssl_settings,
                ),
            ),
        )
        for location in locations.locations
    )


def _pfs_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    conn_established: bool = False
    ssl_settings = SSLSettings(
        key_exchange_names=["dhe_rsa", "ecdhe_rsa", "ecdh_anon", "dh_anon"]
    )

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        intention="check if pfs is enabled",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            if not conn_established:
                locations.append(
                    desc="pfs_disabled",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_PFS,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.key_exchange,
        ssl_settings=ssl_settings,
    )


def _sslv3_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    conn_established: bool = False
    ssl_settings = SSLSettings(max_version=(3, 0))

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        intention="check if sslv3 enabled",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            if conn_established:
                locations.append(
                    desc="sslv3_enabled",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_SSLV3,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.max_version,
        ssl_settings=ssl_settings,
    )


def _tlsv1_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    conn_established: bool = False
    ssl_settings = SSLSettings(min_version=(3, 1), max_version=(3, 1))

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        intention="check if tlsv1 enabled",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            if conn_established:
                locations.append(
                    desc="tlsv1_enabled",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_TLS,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.max_version,
        ssl_settings=ssl_settings,
    )


def _tlsv1_1_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    conn_established: bool = False
    ssl_settings = SSLSettings(min_version=(3, 2), max_version=(3, 2))

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        intention="check if tlsv1.1 enabled",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            if conn_established:
                locations.append(
                    desc="tlsv1_1_enabled",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_TLS,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.max_version,
        ssl_settings=ssl_settings,
    )


def _tlsv1_3_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    conn_established: bool = False
    ssl_settings = SSLSettings(min_version=(3, 4), max_version=(3, 4))

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        intention="check if tlsv1.3 disabled",
        expected_exceptions=(tlslite.errors.TLSLocalAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            if connection.closed:
                locations.append(
                    desc="tlsv1_3_disabled",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_TLS,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.max_version,
        ssl_settings=ssl_settings,
    )


def _anonymous_ciphers_allowed(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    conn_established: bool = False
    ssl_settings = SSLSettings()

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        anonymous=True,
        intention="check if anonymous ciphers allowed",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            if conn_established:
                locations.append(
                    desc="anonymous_ciphers_allowed",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_ANON,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.ciphers,
        ssl_settings=ssl_settings,
    )


def _weak_ciphers_allowed(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    conn_established: bool = False
    ssl_settings = SSLSettings(cipher_names=["rc4", "3des", "null"])

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        intention="check if weak ciphers allowed",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            if conn_established:
                locations.append(
                    desc="weak_ciphers_allowed",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.ciphers,
        ssl_settings=ssl_settings,
    )


def _beast_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    conn_established: bool = False
    ssl_settings = SSLSettings(min_version=(3, 1), max_version=(3, 1))

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        intention="check if beast attack is possible",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            # pylint: disable=protected-access
            if conn_established and connection._recordLayer.isCBCMode():
                locations.append(
                    desc="beast_possible",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_CBC,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.ciphers,
        ssl_settings=ssl_settings,
    )


def _cbc_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    conn_established: bool = False
    ssl_settings = SSLSettings(min_version=(3, 2), max_version=(3, 3))

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        intention="check if cbc is enabled",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            # pylint: disable=protected-access
            if conn_established and connection._recordLayer.isCBCMode():
                locations.append(
                    desc="cbc_enabled",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_CBC,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.ciphers,
        ssl_settings=ssl_settings,
    )


def _sweet32_possible(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    conn_established: bool = False
    ssl_settings = SSLSettings(
        min_version=(3, 1),
        max_version=(3, 3),
        cipher_names=["3des"],
    )

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        intention="check if sweet32 attack is possible",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            if conn_established:
                locations.append(
                    desc="sweet32_possible",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_CBC,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.ciphers,
        ssl_settings=ssl_settings,
    )


def _server_supports_tls(ctx: SSLContext, version: Tuple[int, int]) -> bool:
    with connect(
        ctx.target.host,
        ctx.target.port,
        SSLSettings(min_version=version, max_version=version),
        intention=f"check if server supports {ssl_versions[version]}",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            return True
    return False


def _fallback_scsv_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    min_version_id: int = -1

    for version_id in range(0, 3):
        if _server_supports_tls(ctx, version=(3, version_id)):
            min_version_id = version_id
            break

    if min_version_id == -1:
        return tuple()

    conn_established: bool = False
    min_version: Tuple[int, int] = (3, min_version_id)

    ssl_settings = SSLSettings(
        scsv=True,
        min_version=min_version,
        max_version=min_version,
    )

    with connect(
        ctx.target.host,
        ctx.target.port,
        ssl_settings,
        intention="check if fallback scsv is disabled",
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None:
            conn_established = not connection.closed
            if conn_established:
                locations.append(
                    desc="fallback_scsv_disabled",
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_TLS,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.max_version,
        ssl_settings=ssl_settings,
    )


def _tlsv1_3_downgrade(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    if not _server_supports_tls(ctx, version=(3, 4)):
        return tuple()

    for version_id in range(0, 3):
        version: Tuple[int, int] = (3, version_id)
        ssl_settings = SSLSettings(min_version=version, max_version=version)

        with connect(
            ctx.target.host,
            ctx.target.port,
            ssl_settings,
            intention=f"check TLSv1.3 downgraded to {ssl_versions[version]}",
            expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
        ) as connection:
            if connection is not None and not connection.closed:
                locations.append(
                    desc="tlsv1_3_downgrade",
                    desc_kwargs={"version": f"{ssl_versions[version]}"},
                )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_TLS,
        ctx=ctx,
        conn_established=True,
        line=SSLSnippetLine.max_version,
        ssl_settings=ssl_settings,
    )


def get_check_ctx(ssl_ctx: SSLContext) -> SSLContext:
    return ssl_ctx


CHECKS: Dict[
    core_model.FindingEnum,
    List[Callable[[SSLContext], core_model.Vulnerabilities]],
] = {
    core_model.FindingEnum.F052: [_weak_ciphers_allowed],
    core_model.FindingEnum.F052_ANON: [_anonymous_ciphers_allowed],
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
