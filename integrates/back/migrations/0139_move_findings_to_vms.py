# pylint: disable=invalid-name
"""
This migration aims to move/copy all the findings to the single table model
using the new finding entity

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from custom_exceptions import (
    AlreadyCreated,
)
from custom_types import (
    DynamoQuery as DynamoQueryType,
    Finding as FindingType,
    Historic as HistoricType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    findings as findings_model,
    MASKED,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingSorts,
    FindingStateJustification,
    FindingStateStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingUnreliableIndicators,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
)
from decimal import (
    Decimal,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from findings.domain import (
    get_closed_vulnerabilities,
    get_is_verified,
    get_newest_vulnerability_report_date,
    get_oldest_open_vulnerability_report_date,
    get_oldest_vulnerability_report_date,
    get_open_vulnerabilities,
    get_status,
    get_treatment_summary,
    get_where,
)
from findings.domain.evidence import (
    EVIDENCE_NAMES,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
)
from newutils.requests import (
    map_source,
)
import time
from typing import (
    cast,
    Dict,
    List,
    Union,
)
from unreliable_indicators.enums import (
    EntityAttr,
)
from unreliable_indicators.operations import (
    _format_unreliable_status,
    _format_unreliable_treatment_summary,
)

FINDING_TABLE: str = "FI_findings"
PROD: bool = False


async def _populate_finding_unreliable_indicator(
    loaders: Dataloaders,
    group_name: str,
    finding_id: str,
) -> None:
    indicators = {
        EntityAttr.closed_vulnerabilities: get_closed_vulnerabilities(
            loaders, finding_id
        )
    }
    indicators[EntityAttr.is_verified] = get_is_verified(loaders, finding_id)
    indicators[
        EntityAttr.newest_vulnerability_report_date
    ] = get_newest_vulnerability_report_date(loaders, finding_id)
    indicators[
        EntityAttr.oldest_open_vulnerability_report_date
    ] = get_oldest_open_vulnerability_report_date(loaders, finding_id)
    indicators[
        EntityAttr.oldest_vulnerability_report_date
    ] = get_oldest_vulnerability_report_date(loaders, finding_id)
    indicators[EntityAttr.open_vulnerabilities] = get_open_vulnerabilities(
        loaders, finding_id
    )
    indicators[EntityAttr.status] = get_status(loaders, finding_id)
    indicators[EntityAttr.where] = get_where(loaders, finding_id)
    indicators[EntityAttr.treatment_summary] = get_treatment_summary(
        loaders, finding_id
    )

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
        group_name=group_name,
        finding_id=finding_id,
        indicators=indicators,
    )


async def _populate_finding_historic_state(
    group_name: str,
    finding_id: str,
    historic_state: HistoricType,
) -> None:
    for old_state in historic_state:
        if "date" in old_state and old_state["date"]:
            state = _format_state(old_state)
            await findings_model.update_state(
                group_name=group_name,
                finding_id=finding_id,
                state=state,
            )


async def _populate_finding_historic_verification(
    group_name: str,
    finding_id: str,
    historic_verification: HistoricType,
) -> None:
    for old_verification in historic_verification:
        verification = _format_verification(old_verification)
        await findings_model.update_verification(
            group_name=group_name,
            finding_id=finding_id,
            verification=verification,
        )


def _format_source(source: str) -> Source:
    source = map_source(source)
    return Source[source.upper()]


def _format_state(
    state: HistoricType,
    initial: bool = False,
) -> FindingState:
    return FindingState(
        modified_by=state.get("analyst", ""),
        modified_date=datetime_utils.get_as_utc_iso_format(
            datetime_utils.get_from_str(state.get("date", ""))
        ),
        source=_format_source(state["source"]),
        status=FindingStateStatus.CREATED
        if initial
        else FindingStateStatus[str(state["state"]).upper()],
        justification=FindingStateJustification[state["justification"]]
        if state.get("justification")
        else FindingStateJustification.NO_JUSTIFICATION,
    )


def _format_verification(state: HistoricType) -> FindingVerification:
    return FindingVerification(
        comment_id=str(state["comment"]),
        modified_by=state.get("user", ""),
        modified_date=datetime_utils.get_as_utc_iso_format(
            datetime_utils.get_from_str(state["date"])
        ),
        status=FindingVerificationStatus[str(state["status"]).upper()],
        vulnerability_ids=set(state["vulns"]) if "vulns" in state else None,
    )


def _format_severity(
    finding: FindingType,
) -> Union[Finding31Severity, Finding20Severity]:
    if str(finding.get("cvssVersion", "3.1")) == "3.1":
        return Finding31Severity(
            attack_complexity=finding.get("attack_complexity", Decimal("0.0")),
            attack_vector=finding.get("attack_vector", Decimal("0.0")),
            availability_impact=finding.get(
                "availability_impact", Decimal("0.0")
            ),
            availability_requirement=finding.get(
                "availability_requirement", Decimal("0.0")
            ),
            confidentiality_impact=finding.get(
                "confidentiality_impact", Decimal("0.0")
            ),
            confidentiality_requirement=finding.get(
                "confidentiality_requirement", Decimal("0.0")
            ),
            exploitability=finding.get("exploitability", Decimal("0.0")),
            integrity_impact=finding.get("integrity_impact", Decimal("0.0")),
            integrity_requirement=finding.get(
                "integrity_requirement", Decimal("0.0")
            ),
            modified_attack_complexity=finding.get(
                "modified_attack_complexity", Decimal("0.0")
            ),
            modified_attack_vector=finding.get(
                "modified_attack_vector", Decimal("0.0")
            ),
            modified_availability_impact=finding.get(
                "modified_availability_impact", Decimal("0.0")
            ),
            modified_confidentiality_impact=finding.get(
                "modified_confidentiality_impact", Decimal("0.0")
            ),
            modified_integrity_impact=finding.get(
                "modified_integrity_impact", Decimal("0.0")
            ),
            modified_privileges_required=finding.get(
                "modified_privileges_required", Decimal("0.0")
            ),
            modified_user_interaction=finding.get(
                "modified_user_interaction", Decimal("0.0")
            ),
            modified_severity_scope=finding.get(
                "modified_severity_scope", Decimal("0.0")
            ),
            privileges_required=finding.get(
                "privileges_required", Decimal("0.0")
            ),
            remediation_level=finding.get("remediation_level", Decimal("0.0")),
            report_confidence=finding.get("report_confidence", Decimal("0.0")),
            severity_scope=finding.get("severity_scope", Decimal("0.0")),
            user_interaction=finding.get("user_interaction", Decimal("0.0")),
        )
    return Finding20Severity(
        access_complexity=finding.get("access_complexity", Decimal("0.0")),
        access_vector=finding.get("access_vector", Decimal("0.0")),
        authentication=finding.get("authentication", Decimal("0.0")),
        availability_impact=finding.get("availability_impact", Decimal("0.0")),
        availability_requirement=finding.get(
            "availability_requirement", Decimal("0.0")
        ),
        collateral_damage_potential=finding.get(
            "collateral_damage_potential", Decimal("0.0")
        ),
        confidence_level=finding.get("confidence_level", Decimal("0.0")),
        confidentiality_impact=finding.get(
            "confidentiality_impact", Decimal("0.0")
        ),
        confidentiality_requirement=finding.get(
            "confidentiality_requirement", Decimal("0.0")
        ),
        exploitability=finding.get("exploitability", Decimal("0.0")),
        finding_distribution=finding.get(
            "finding_distribution", Decimal("0.0")
        ),
        integrity_impact=finding.get("integrity_impact", Decimal("0.0")),
        integrity_requirement=finding.get(
            "integrity_requirement", Decimal("0.0")
        ),
        resolution_level=finding.get("resolution_level", Decimal("0.0")),
    )


def _format_masked_evidences(old_finding: FindingType) -> FindingEvidences:
    evidences = FindingEvidences()
    finding_files = cast(List[Dict[str, str]], old_finding.get("files", []))
    for name, file in zip(EVIDENCE_NAMES, finding_files):
        new_name = EVIDENCE_NAMES[name]
        date = (
            file.get("date", "")
            or file.get("upload_date", "")
            or findings_utils.get_approval_date(old_finding)
            or findings_utils.get_creation_date(old_finding)
        )
        evidence = FindingEvidence(
            description=MASKED,
            modified_date=datetime_utils.get_as_utc_iso_format(
                datetime_utils.get_from_str(date)
            )
            if date
            else "",
            url=MASKED,
        )
        evidences = evidences._replace(**{new_name: evidence})
    return evidences


def _format_non_masked_evidences(old_finding: FindingType) -> FindingEvidences:
    evidences = FindingEvidences()
    finding_files = cast(List[Dict[str, str]], old_finding.get("files", []))
    for old_file in finding_files:
        old_name = old_file["name"]
        new_name = EVIDENCE_NAMES[old_name]
        old_evidence = findings_utils.get_evidence(
            old_name, finding_files, old_finding
        )
        date = datetime_utils.get_as_utc_iso_format(
            datetime_utils.get_from_str(
                old_evidence.get("date", "")
                or old_evidence.get("upload_date", "")
            )
        )
        evidence = FindingEvidence(
            description=old_evidence["description"],
            modified_date=date,
            url=old_evidence["url"],
        )
        evidences = evidences._replace(**{new_name: evidence})

    return evidences


def _format_evidences(old_finding: FindingType) -> FindingEvidences:
    finding_files = cast(List[Dict[str, str]], old_finding.get("files", []))
    if not finding_files:
        return FindingEvidences()

    if [file for file in finding_files if str(file["name"]).upper() == MASKED]:
        return _format_masked_evidences(old_finding)

    return _format_non_masked_evidences(old_finding)


async def _proccess_finding(
    loaders: Dataloaders,
    old_finding: FindingType,
) -> bool:
    if "project_name" not in old_finding:
        print(f'ERROR - "{old_finding["finding_id"]}" project_name missing')
        return False

    if "historic_state" not in old_finding:
        print(f'ERROR - "{old_finding["finding_id"]}" historic_state missing')
        return False

    try:
        await findings_model.add(
            finding=Finding(
                hacker_email=old_finding.get("analyst", ""),
                group_name=old_finding["project_name"],
                id=old_finding["finding_id"],
                state=_format_state(
                    state=old_finding["historic_state"][0],
                    initial=True,
                ),
                title=old_finding.get("finding", ""),
                affected_systems=old_finding.get("affected_systems", ""),
                attack_vector_description=old_finding.get(
                    "attack_vector_description", ""
                )
                or old_finding.get("attack_vector_desc", ""),
                approval=None,
                compromised_attributes=old_finding.get("records", ""),
                creation=None,
                compromised_records=int(old_finding.get("records_number", 0)),
                description=old_finding.get("vulnerability", ""),
                evidences=_format_evidences(old_finding),
                severity=_format_severity(old_finding),
                sorts=FindingSorts[old_finding.get("sorts", "NO")],
                submission=None,
                recommendation=old_finding.get("effect_solution", ""),
                requirements=old_finding.get("requirements", ""),
                threat=old_finding.get("threat", ""),
                unreliable_indicators=FindingUnreliableIndicators(),
                verification=_format_verification(
                    old_finding["historic_verification"][0]
                )
                if old_finding.get("historic_verification")
                else None,
            )
        )
    except AlreadyCreated:
        print(f'ERROR - "{old_finding["finding_id"]}" already created at vms')
        return False

    await _populate_finding_historic_state(
        old_finding["project_name"],
        old_finding["finding_id"],
        old_finding["historic_state"],
    )

    if old_finding.get("historic_verification"):
        await _populate_finding_historic_verification(
            old_finding["project_name"],
            old_finding["finding_id"],
            old_finding["historic_verification"],
        )

    await _populate_finding_unreliable_indicator(
        loaders,
        old_finding["project_name"],
        old_finding["finding_id"],
    )

    print(f'"{old_finding["finding_id"]}" migration OK')
    return True


async def main() -> None:
    success = False
    scan_attrs: DynamoQueryType = {}
    findings: List[FindingType] = await dynamodb_ops.scan(
        FINDING_TABLE, scan_attrs
    )
    loaders = get_new_context()
    print(f"old findings: len({len(findings)})")

    if PROD:
        success = all(
            await collect(
                _proccess_finding(
                    loaders=loaders,
                    old_finding=old_finding,
                )
                for old_finding in findings
            )
        )

    print(f"Success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
