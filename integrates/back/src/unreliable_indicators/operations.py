from . import (
    model as unreliable_indicators_model,
)
from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.enums import (
    FindingStatus,
)
from db_model.findings.types import (
    Finding,
    FindingUnreliableIndicatorsToUpdate,
)
from findings import (
    domain as findings_domain,
)
from typing import (
    cast,
    Set,
)
from unreliable_indicators.enums import (
    Entity,
    EntityAttr,
    EntityDependency,
    EntityId,
)


async def update_finding_unreliable_indicators(
    loaders: Dataloaders,
    finding_id: str,
    attrs_to_update: Set[EntityAttr],
) -> None:
    finding: Finding = await loaders.finding_new.load(finding_id)
    indicators = dict()

    if EntityAttr.age in attrs_to_update:
        indicators[EntityAttr.age] = findings_domain.get_finding_age(
            loaders, finding.id
        )

    if EntityAttr.closed_vulnerabilities in attrs_to_update:
        indicators[
            EntityAttr.closed_vulnerabilities
        ] = findings_domain.get_closed_vulnerabilities(loaders, finding.id)

    if EntityAttr.is_verified in attrs_to_update:
        indicators[EntityAttr.is_verified] = findings_domain.get_is_verified(
            loaders, finding.id
        )

    if EntityAttr.last_vulnerability in attrs_to_update:
        indicators[
            EntityAttr.last_vulnerability
        ] = findings_domain.get_finding_last_vuln_report(loaders, finding.id)

    if EntityAttr.open_age in attrs_to_update:
        indicators[EntityAttr.open_age] = findings_domain.get_finding_open_age(
            loaders, finding.id
        )

    if EntityAttr.open_vulnerabilities in attrs_to_update:
        indicators[
            EntityAttr.open_vulnerabilities
        ] = findings_domain.get_open_vulnerabilities(loaders, finding.id)

    if EntityAttr.report_date in attrs_to_update:
        indicators[
            EntityAttr.report_date
        ] = findings_domain.get_report_date_new(loaders, finding.id)

    if EntityAttr.status in attrs_to_update:
        indicators[EntityAttr.status] = findings_domain.get_status(
            loaders, finding.id
        )

    if EntityAttr.where in attrs_to_update:
        indicators[EntityAttr.where] = findings_domain.get_where(
            loaders, finding.id
        )

    result = dict(zip(indicators.keys(), await collect(indicators.values())))
    indicators = FindingUnreliableIndicatorsToUpdate(
        unreliable_age=result.get(EntityAttr.age),
        unreliable_closed_vulnerabilities=result.get(
            EntityAttr.closed_vulnerabilities
        ),
        unreliable_is_verified=result.get(EntityAttr.is_verified),
        unreliable_last_vulnerability=result.get(
            EntityAttr.last_vulnerability
        ),
        unreliable_open_age=result.get(EntityAttr.open_age),
        unreliable_open_vulnerabilities=result.get(
            EntityAttr.open_vulnerabilities
        ),
        unreliable_report_date=result.get(EntityAttr.report_date),
        unreliable_status=FindingStatus[
            cast(str, result[EntityAttr.status]).upper()
        ]
        if result.get(EntityAttr.status)
        else None,
        unreliable_where=result.get(EntityAttr.where),
    )
    await findings_model.update_unreliable_indicators(
        group_name=finding.group_name,
        finding_id=finding.id,
        indicators=indicators,
    )


async def update_unreliable_indicators_by_deps(
    dependency: EntityDependency, **args: str
) -> None:
    loaders: Dataloaders = get_new_context()
    entities_to_update = (
        unreliable_indicators_model.get_entities_to_update_by_dependency(
            dependency, **args
        )
    )
    updations = []

    if Entity.finding in entities_to_update:
        updations.append(
            update_finding_unreliable_indicators(
                loaders,
                entities_to_update[Entity.finding].entity_ids[EntityId.id],
                entities_to_update[Entity.finding].attributes_to_update,
            )
        )

    await collect(updations)
