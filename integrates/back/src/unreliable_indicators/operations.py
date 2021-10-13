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
    FindingTreatmentSummary,
    FindingUnreliableIndicatorsToUpdate,
)
from findings import (
    domain as findings_domain,
)
from newutils.vulnerabilities import (
    Treatments,
)
from typing import (
    Optional,
    Set,
)
from unreliable_indicators.enums import (
    Entity,
    EntityAttr,
    EntityDependency,
    EntityId,
)


def _format_unreliable_status(
    status: Optional[str],
) -> Optional[FindingStatus]:
    unreliable_status = None
    if status:
        unreliable_status = FindingStatus[status.upper()]
    return unreliable_status


def _format_unreliable_treatment_summary(
    treatment_summary: Optional[Treatments],
) -> Optional[FindingTreatmentSummary]:
    unreliable_treatment_summary = None
    if treatment_summary:
        unreliable_treatment_summary = FindingTreatmentSummary(
            accepted=treatment_summary.ACCEPTED,
            accepted_undefined=treatment_summary.ACCEPTED_UNDEFINED,
            in_progress=treatment_summary.IN_PROGRESS,
            new=treatment_summary.NEW,
        )
    return unreliable_treatment_summary


async def update_finding_unreliable_indicators(  # noqa: C901
    loaders: Dataloaders,
    finding_id: str,
    attrs_to_update: Set[EntityAttr],
) -> None:
    finding: Finding = await loaders.finding.load(finding_id)
    indicators = {}

    if EntityAttr.closed_vulnerabilities in attrs_to_update:
        indicators[
            EntityAttr.closed_vulnerabilities
        ] = findings_domain.get_closed_vulnerabilities(loaders, finding.id)

    if EntityAttr.is_verified in attrs_to_update:
        indicators[EntityAttr.is_verified] = findings_domain.get_is_verified(
            loaders, finding.id
        )

    if EntityAttr.newest_vulnerability_report_date in attrs_to_update:
        indicators[
            EntityAttr.newest_vulnerability_report_date
        ] = findings_domain.get_newest_vulnerability_report_date(
            loaders, finding.id
        )

    if EntityAttr.oldest_open_vulnerability_report_date in attrs_to_update:
        indicators[
            EntityAttr.oldest_open_vulnerability_report_date
        ] = findings_domain.get_oldest_open_vulnerability_report_date(
            loaders, finding.id
        )

    if EntityAttr.oldest_vulnerability_report_date in attrs_to_update:
        indicators[
            EntityAttr.oldest_vulnerability_report_date
        ] = findings_domain.get_oldest_vulnerability_report_date(
            loaders, finding.id
        )

    if EntityAttr.open_vulnerabilities in attrs_to_update:
        indicators[
            EntityAttr.open_vulnerabilities
        ] = findings_domain.get_open_vulnerabilities(loaders, finding.id)

    if EntityAttr.status in attrs_to_update:
        indicators[EntityAttr.status] = findings_domain.get_status(
            loaders, finding.id
        )

    if EntityAttr.where in attrs_to_update:
        indicators[EntityAttr.where] = findings_domain.get_where(
            loaders, finding.id
        )

    if EntityAttr.treatment_summary in attrs_to_update:
        indicators[
            EntityAttr.treatment_summary
        ] = findings_domain.get_treatment_summary(loaders, finding.id)

    result = dict(zip(indicators.keys(), await collect(indicators.values())))
    indicators = FindingUnreliableIndicatorsToUpdate(
        unreliable_closed_vulnerabilities=result.get(
            EntityAttr.closed_vulnerabilities
        ),
        unreliable_is_verified=result.get(EntityAttr.is_verified),
        unreliable_newest_vulnerability_report_date=result.get(
            EntityAttr.newest_vulnerability_report_date
        ),
        unreliable_oldest_open_vulnerability_report_date=result.get(
            EntityAttr.oldest_open_vulnerability_report_date
        ),
        unreliable_oldest_vulnerability_report_date=result.get(
            EntityAttr.oldest_vulnerability_report_date
        ),
        unreliable_open_vulnerabilities=result.get(
            EntityAttr.open_vulnerabilities
        ),
        unreliable_status=_format_unreliable_status(
            result.get(EntityAttr.status)
        ),
        unreliable_where=result.get(EntityAttr.where),
        unreliable_treatment_summary=_format_unreliable_treatment_summary(
            result.get(EntityAttr.treatment_summary)
        ),
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
