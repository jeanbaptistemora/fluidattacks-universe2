from . import (
    model as unreliable_indicators_model,
)
from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
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
    EntityAttrName,
    EntityIdName,
    EntityName,
)


async def update_finding_unreliable_indicators(
    loaders: Dataloaders,
    finding_id: str,
    attrs_to_update: Set[EntityAttrName],
) -> None:
    finding: Finding = await loaders.finding_new.load(finding_id)
    indicators = dict()

    if EntityAttrName.age in attrs_to_update:
        indicators[EntityAttrName.age] = findings_domain.get_finding_age(
            loaders, finding.id
        )

    if EntityAttrName.closed_vulnerabilities in attrs_to_update:
        indicators[
            EntityAttrName.closed_vulnerabilities
        ] = findings_domain.get_closed_vulnerabilities(loaders, finding.id)

    if EntityAttrName.is_verified in attrs_to_update:
        indicators[
            EntityAttrName.is_verified
        ] = findings_domain.get_is_verified(loaders, finding.id)

    if EntityAttrName.last_vulnerability in attrs_to_update:
        indicators[
            EntityAttrName.last_vulnerability
        ] = findings_domain.get_finding_last_vuln_report(loaders, finding.id)

    if EntityAttrName.open_age in attrs_to_update:
        indicators[
            EntityAttrName.open_age
        ] = findings_domain.get_finding_open_age(loaders, finding.id)

    if EntityAttrName.open_vulnerabilities in attrs_to_update:
        indicators[
            EntityAttrName.open_vulnerabilities
        ] = findings_domain.get_open_vulnerabilities(loaders, finding.id)

    if EntityAttrName.report_date in attrs_to_update:
        indicators[
            EntityAttrName.report_date
        ] = findings_domain.get_report_date_new(loaders, finding.id)

    if EntityAttrName.status in attrs_to_update:
        indicators[EntityAttrName.status] = findings_domain.get_status(
            loaders, finding.id
        )

    result = dict(zip(indicators.keys(), await collect(indicators.values())))
    indicators = FindingUnreliableIndicatorsToUpdate(
        unreliable_age=result.get(EntityAttrName.age),
        unreliable_closed_vulnerabilities=result.get(
            EntityAttrName.closed_vulnerabilities
        ),
        unreliable_is_verified=result.get(EntityAttrName.is_verified),
        unreliable_last_vulnerability=result.get(
            EntityAttrName.last_vulnerability
        ),
        unreliable_open_age=result.get(EntityAttrName.open_age),
        unreliable_open_vulnerabilities=result.get(
            EntityAttrName.open_vulnerabilities
        ),
        unreliable_report_date=result.get(EntityAttrName.report_date),
        unreliable_status=FindingStatus[
            cast(str, result[EntityAttrName.status]).upper()
        ]
        if result.get(EntityAttrName.status)
        else None,
    )
    await findings_model.update_unreliable_indicators(
        group_name=finding.group_name,
        finding_id=finding.id,
        indicators=indicators,
    )


async def update_unreliable_indicators_by_deps(
    loaders: Dataloaders, dependency: str, **args: str
) -> None:
    entities_to_update = (
        unreliable_indicators_model.get_entities_to_update_by_dependency(
            dependency, **args
        )
    )
    updations = []

    if EntityName.finding in entities_to_update:
        updations.append(
            update_finding_unreliable_indicators(
                loaders,
                entities_to_update[EntityName.finding].entity_ids[
                    EntityIdName.id
                ],
                entities_to_update[EntityName.finding].attributes_to_update,
            )
        )

    await collect(updations)
