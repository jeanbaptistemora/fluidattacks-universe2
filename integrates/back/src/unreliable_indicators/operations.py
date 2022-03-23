from . import (
    model as unreliable_indicators_model,
)
from aioextensions import (
    collect,
    schedule,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    IndicatorAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    findings as findings_model,
    roots as roots_model,
    vulnerabilities as vulns_model,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingStatus,
)
from db_model.findings.types import (
    Finding,
    FindingTreatmentSummary,
    FindingUnreliableIndicatorsToUpdate,
)
from db_model.roots.types import (
    RootItem,
    RootUnreliableIndicatorsToUpdate,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityUnreliableIndicatorsToUpdate,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from findings import (
    domain as findings_domain,
)
from mailer import (
    findings as findings_mail,
)
import newrelic.agent
from roots import (
    domain as roots_domain,
)
from typing import (
    List,
    Optional,
    Set,
    Tuple,
)
from unreliable_indicators.enums import (
    Entity,
    EntityAttr,
    EntityDependency,
    EntityId,
)
from vulnerabilities import (
    domain as vulns_domain,
)
from vulnerabilities.types import (
    Treatments,
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
            accepted=treatment_summary.accepted,
            accepted_undefined=treatment_summary.accepted_undefined,
            in_progress=treatment_summary.in_progress,
            new=treatment_summary.new,
        )
    return unreliable_treatment_summary


@newrelic.agent.function_trace()
async def update_findings_unreliable_indicators(
    finding_ids: List[str],
    attrs_to_update: Set[EntityAttr],
) -> None:
    await collect(
        tuple(
            update_finding_unreliable_indicators(
                finding_id,
                attrs_to_update,
            )
            for finding_id in set(finding_ids)
        )
    )


@retry_on_exceptions(
    exceptions=(
        IndicatorAlreadyUpdated,
        UnavailabilityError,
    ),
    max_attempts=20,
    sleep_seconds=0,
)
async def update_finding_unreliable_indicators(  # noqa: C901
    finding_id: str,
    attrs_to_update: Set[EntityAttr],
) -> None:
    loaders: Dataloaders = get_new_context()
    finding: Finding = await loaders.finding.load(finding_id)
    indicators = {}
    group_name = finding.group_name
    severity_score = findings_domain.get_severity_score(finding.severity)

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
    indicators_to_update = FindingUnreliableIndicatorsToUpdate(
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

    if (
        indicators_to_update.unreliable_status == FindingStatus.CLOSED
        and finding.state.status == FindingStateStatus.APPROVED
    ):
        if severity_score >= 7.0:
            schedule(
                findings_mail.send_mail_vulnerability_report(
                    loaders=loaders,
                    group_name=group_name,
                    finding_title=finding.title,
                    finding_id=finding_id,
                    severity=severity_score,
                    is_closed=True,
                )
            )
    await findings_model.update_unreliable_indicators(
        current_value=finding.unreliable_indicators,
        group_name=finding.group_name,
        finding_id=finding.id,
        indicators=indicators_to_update,
    )


@retry_on_exceptions(
    exceptions=(IndicatorAlreadyUpdated,),
    max_attempts=20,
    sleep_seconds=0,
)
@newrelic.agent.function_trace()
async def update_vulnerabilities_unreliable_indicators(
    vulnerability_ids: List[str],
    attrs_to_update: Set[EntityAttr],
) -> None:
    # Placed the loader here since the same finding_historic_verification is
    # shared by many vulnerabilities
    loaders: Dataloaders = get_new_context()
    await collect(
        tuple(
            update_vulnerability_unreliable_indicators(
                loaders,
                vulnerability_id,
                attrs_to_update,
            )
            for vulnerability_id in set(vulnerability_ids)
        )
    )


async def update_root_unreliable_indicators(
    loaders: Dataloaders,
    root_id: Tuple[str, str],
    attrs_to_update: Set[EntityAttr],
) -> None:
    root: RootItem = await loaders.root.load(root_id)
    indicators = {}

    if EntityAttr.last_status_update in attrs_to_update:
        indicators[
            EntityAttr.last_status_update
        ] = roots_domain.get_last_status_update(loaders, root.id)

    result = dict(zip(indicators.keys(), await collect(indicators.values())))

    with suppress(IndicatorAlreadyUpdated):
        await roots_model.update_unreliable_indicators(
            current_value=root,
            indicators=RootUnreliableIndicatorsToUpdate(
                unreliable_last_status_update=result.get(
                    EntityAttr.last_status_update
                ),
            ),
        )


@newrelic.agent.function_trace()
async def update_roots_unreliable_indicators(
    root_ids: List[Tuple[str, str]],
    attrs_to_update: Set[EntityAttr],
) -> None:
    loaders = get_new_context()
    await collect(
        tuple(
            update_root_unreliable_indicators(
                loaders,
                root_id,
                attrs_to_update,
            )
            for root_id in set(root_ids)
        )
    )


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    max_attempts=20,
    sleep_seconds=0,
)
async def update_vulnerability_unreliable_indicators(
    loaders: Dataloaders,
    vulnerability_id: str,
    attrs_to_update: Set[EntityAttr],
) -> None:
    vulnerability: Vulnerability = await loaders.vulnerability.load(
        vulnerability_id
    )
    indicators = {}

    if EntityAttr.efficacy in attrs_to_update:
        indicators[EntityAttr.efficacy] = vulns_domain.get_efficacy(
            loaders, vulnerability
        )

    if EntityAttr.last_reattack_date in attrs_to_update:
        indicators[
            EntityAttr.last_reattack_date
        ] = vulns_domain.get_last_reattack_date(loaders, vulnerability)

    if EntityAttr.last_reattack_requester in attrs_to_update:
        indicators[
            EntityAttr.last_reattack_requester
        ] = vulns_domain.get_reattack_requester(loaders, vulnerability)

    if EntityAttr.last_requested_reattack_date in attrs_to_update:
        indicators[
            EntityAttr.last_requested_reattack_date
        ] = vulns_domain.get_last_requested_reattack_date(
            loaders, vulnerability
        )

    if EntityAttr.reattack_cycles in attrs_to_update:
        indicators[
            EntityAttr.reattack_cycles
        ] = vulns_domain.get_reattack_cycles(loaders, vulnerability)

    if EntityAttr.report_date in attrs_to_update:
        indicators[EntityAttr.report_date] = vulns_domain.get_report_date(
            loaders, vulnerability
        )

    if EntityAttr.treatment_changes in attrs_to_update:
        indicators[
            EntityAttr.treatment_changes
        ] = vulns_domain.get_treatment_changes(loaders, vulnerability)

    result = dict(zip(indicators.keys(), await collect(indicators.values())))
    indicators = VulnerabilityUnreliableIndicatorsToUpdate(
        unreliable_efficacy=result.get(EntityAttr.efficacy),
        unreliable_last_reattack_date=result.get(
            EntityAttr.last_reattack_date
        ),
        unreliable_last_reattack_requester=result.get(
            EntityAttr.last_reattack_requester
        ),
        unreliable_last_requested_reattack_date=result.get(
            EntityAttr.last_requested_reattack_date
        ),
        unreliable_reattack_cycles=result.get(EntityAttr.reattack_cycles),
        unreliable_report_date=result.get(EntityAttr.report_date),
        unreliable_treatment_changes=result.get(EntityAttr.treatment_changes),
    )
    await vulns_model.update_unreliable_indicators(
        current_value=vulnerability,
        indicators=indicators,
    )


async def update_unreliable_indicators_by_deps(
    dependency: EntityDependency, **args: List[str]
) -> None:
    entities_to_update = (
        unreliable_indicators_model.get_entities_to_update_by_dependency(
            dependency, **args
        )
    )
    updates = []

    if Entity.finding in entities_to_update:
        updates.append(
            update_findings_unreliable_indicators(
                entities_to_update[Entity.finding].entity_ids[EntityId.ids],
                entities_to_update[Entity.finding].attributes_to_update,
            )
        )

    if Entity.root in entities_to_update:
        updates.append(
            update_roots_unreliable_indicators(
                entities_to_update[Entity.root].entity_ids[EntityId.ids],
                entities_to_update[Entity.root].attributes_to_update,
            )
        )

    if Entity.vulnerability in entities_to_update:
        updates.append(
            update_vulnerabilities_unreliable_indicators(
                entities_to_update[Entity.vulnerability].entity_ids[
                    EntityId.ids
                ],
                entities_to_update[Entity.vulnerability].attributes_to_update,
            )
        )

    await collect(updates)
