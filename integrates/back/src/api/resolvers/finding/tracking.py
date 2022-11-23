from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    VulnerabilityTreatment,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    Tracking,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def _get_treatments(
    *, loaders: Dataloaders, vulnerabilities_id: tuple[str, ...]
) -> tuple[tuple[VulnerabilityTreatment, ...], ...]:
    return await loaders.vulnerability_historic_treatment.load_many(
        vulnerabilities_id
    )


async def _get_states(
    *, loaders: Dataloaders, vulnerabilities_id: tuple[str, ...]
) -> tuple[tuple[VulnerabilityTreatment, ...], ...]:
    return await loaders.vulnerability_historic_state.load_many(
        vulnerabilities_id
    )


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> list[Tracking]:
    if not parent.approval:
        return []

    loaders: Dataloaders = info.context.loaders
    finding_vulns_loader = loaders.finding_vulnerabilities_nzr
    vulns = await finding_vulns_loader.load(parent.id)
    vulnerabilities_id = tuple(vuln.id for vuln in vulns)
    vulns_state, vulns_treatment = await collect(
        (
            _get_states(
                loaders=info.context.loaders,
                vulnerabilities_id=vulnerabilities_id,
            ),
            _get_treatments(
                loaders=info.context.loaders,
                vulnerabilities_id=vulnerabilities_id,
            ),
        )
    )

    return findings_domain.get_tracking_vulnerabilities(
        vulns_state=vulns_state,  # type: ignore
        vulns_treatment=vulns_treatment,
    )
