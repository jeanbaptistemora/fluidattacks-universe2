from lib_ssl.types import (
    SSLContext,
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
from utils.ssl import (
    connect,
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


def _create_vulns(
    locations: Locations,
    finding: core_model.FindingEnum,
    ctx: SSLContext,
    snippet: str,
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
                snippet=snippet,
            ),
        )
        for location in locations.locations
    )


def _pfs_disabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    with connect(
        ctx.target.host,
        ctx.target.port,
        key_exchange_names=(
            "dhe_rsa",
            "ecdhe_rsa",
            "ecdh_anon",
            "dh_anon",
        ),
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and connection.closed:
            locations.append(
                desc="pfs_disabled",
            )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F052_PFS,
        ctx=ctx,
        snippet="pfs is disabled",
    )


def _sslv3_enabled(ctx: SSLContext) -> core_model.Vulnerabilities:
    locations = Locations(locations=[])

    with connect(
        ctx.target.host,
        ctx.target.port,
        max_version=(3, 0),
        expected_exceptions=(tlslite.errors.TLSRemoteAlert,),
    ) as connection:
        if connection is not None and not connection.closed:
            locations.append(
                desc="sslv3_enabled",
            )

    return _create_vulns(
        locations=locations,
        finding=core_model.FindingEnum.F011_SSLV3,
        ctx=ctx,
        snippet="ssl v3 is enabled",
    )


def get_check_ctx(ssl_ctx: SSLContext) -> SSLContext:
    return ssl_ctx


CHECKS: Dict[
    core_model.FindingEnum,
    Callable[[SSLContext], core_model.Vulnerabilities],
] = {
    core_model.FindingEnum.F011_SSLV3: _sslv3_enabled,
    core_model.FindingEnum.F052_PFS: _pfs_disabled,
}
