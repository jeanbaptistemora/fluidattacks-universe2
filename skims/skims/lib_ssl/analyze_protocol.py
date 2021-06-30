from lib_ssl.as_string import (
    snippet,
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
        finding=core_model.FindingEnum.F011_SSLV3,
        ctx=ctx,
        conn_established=conn_established,
        line=SSLSnippetLine.max_version,
        ssl_settings=ssl_settings,
    )


def get_check_ctx(ssl_ctx: SSLContext) -> SSLContext:
    return ssl_ctx


CHECKS: Dict[
    core_model.FindingEnum,
    List[Callable[[SSLContext], core_model.Vulnerabilities]],
] = {
    core_model.FindingEnum.F011_SSLV3: [_sslv3_enabled],
    core_model.FindingEnum.F052_PFS: [_pfs_disabled],
}
