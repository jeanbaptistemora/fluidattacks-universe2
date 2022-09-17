# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# type: ignore

# pylint: disable=invalid-name,missing-kwoa
"""
This migration aims to move/copy all the findings to the integrates_vms table
using the new finding entity, from the current finding dedicated table.

Findings with status deleted, or that were masked, are skipped in an initial
run for this migration as their priority is low.

An initial cleaning of the integrates_vms table is possible, for removing
previously migrated findings in an inconsistent state.

Execution Time:    2021-10-05 at 01:50:11 UTCUTC
Finalization Time: 2021-10-05 at 02:58:41 UTCUTC

Execution Time:    2021-10-06 at 02:05:41 UTCUTC
Finalization Time: 2021-10-06 at 03:55:23 UTCUTC

Execution Time:    2021-10-07 at 20:52:10 UTCUTC
Finalization Time: 2021-10-07 at 21:33:07 UTCUTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    AlreadyCreated,
)
from custom_types import (  # pylint: disable=import-error
    DynamoQuery as DynamoQueryType,
    Finding as FindingType,
    Historic as HistoricType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    findings as findings_model,
    MASKED,
    TABLE,
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
from dynamodb.operations_legacy import (
    DynamoDelete as DynamoDeleteType,
)
from dynamodb.types import (
    Item,
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
from groups import (
    dal as groups_dal,
)
from newutils import (
    findings as findings_utils,
)
from newutils.datetime import (
    get_as_str,
    get_as_utc_iso_format,
    get_from_str,
    get_minus_delta,
    get_plus_delta,
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

RESULTS_FILE: str = "0139_results.txt"
ERROR: str = "ERROR"
FINDING_TABLE: str = "FI_findings"

CLEAN_FINDINGS: bool = False
MIGRATE_NON_DELETED_FINDINGS: bool = True
MIGRATE_DELETED_FINDINGS: bool = True
MIGRATE_MASKED_FINDINGS: bool = True
PROD: bool = True


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


async def _update_state_entry(
    group_name: str,
    finding_id: str,
    old_state: FindingState,
) -> None:
    state = _format_state(old_state)
    await findings_model.update_state(
        current_value=state,
        group_name=group_name,
        finding_id=finding_id,
        state=state,
    )


async def _populate_finding_historic_state(
    group_name: str,
    finding_id: str,
    historic_state: HistoricType,
) -> None:
    await collect(
        [
            _update_state_entry(
                group_name=group_name,
                finding_id=finding_id,
                old_state=old_state,
            )
            for old_state in historic_state
        ]
    )


async def _update_verification_entry(
    group_name: str,
    finding_id: str,
    old_verification: FindingVerification,
) -> None:
    verification = _format_verification(old_verification)
    await findings_model.update_verification(
        current_value=verification,
        group_name=group_name,
        finding_id=finding_id,
        verification=verification,
    )


async def _populate_finding_historic_verification(
    group_name: str,
    finding_id: str,
    historic_verification: HistoricType,
) -> None:
    await collect(
        [
            _update_verification_entry(
                group_name=group_name,
                finding_id=finding_id,
                old_verification=old_verification,
            )
            for old_verification in historic_verification
        ]
    )


def _format_source(source: str) -> Source:
    source = map_source(source)
    return Source[source.upper()]


def _format_state(state: Dict[str, str]) -> FindingState:
    return FindingState(
        modified_by=state.get("analyst", ""),
        modified_date=get_as_utc_iso_format(get_from_str(state["date"])),
        source=_format_source(state["source"]),
        status=FindingStateStatus[str(state["state"]).upper()],
        justification=FindingStateJustification[state["justification"]]
        if state.get("justification")
        else FindingStateJustification.NO_JUSTIFICATION,
    )


# Check if historic dates are in ascending order and fix them otherwise
def _fix_historic_dates(
    historic: HistoricType,
) -> HistoricType:
    new_historic = []
    comparison_date = ""
    for entry in historic:
        if entry["date"] > comparison_date:
            comparison_date = entry["date"]
        else:
            fixed_date = get_plus_delta(
                get_from_str(comparison_date), seconds=1
            )
            entry["date"] = comparison_date = get_as_str(fixed_date)
        new_historic.append(entry)
    return new_historic


# Validate if the first state is CREATED and fix it
def _fix_historic_state_creation(
    historic: HistoricType,
    analyst: str,
) -> HistoricType:
    current_state = str(historic[0]["state"]).upper()
    if current_state == "CREATED":
        return historic

    if str(historic[0]["state"]).upper() == MASKED:
        historic[0]["state"] = "CREATED"
        return historic

    # Guess the creation date and add new historic entry
    creation_date = get_minus_delta(
        get_from_str(historic[0]["date"]), seconds=1
    )
    creation_state = {
        "date": get_as_str(creation_date),
        "analyst": analyst or historic[0]["analyst"],
        "state": "CREATED",
        "source": historic[0]["source"],
    }
    return [creation_state, *historic]


def _format_verification(state: Dict[str, str]) -> FindingVerification:
    return FindingVerification(
        comment_id=str(state["comment"]),
        modified_by=state.get("user", ""),
        modified_date=get_as_utc_iso_format(get_from_str(state["date"])),
        status=FindingVerificationStatus[str(state["status"]).upper()],
        vulnerability_ids=set(state["vulns"]) if "vulns" in state else None,
    )


def _format_severity(
    finding: FindingType,
) -> Union[Finding31Severity, Finding20Severity]:

    if str(finding.get("cvssVersion", "3.1")) == "3.1":
        return Finding31Severity(
            attack_complexity=Decimal(finding.get("attack_complexity", "0.0")),
            attack_vector=Decimal(finding.get("attack_vector", "0.0")),
            availability_impact=Decimal(
                finding.get("availability_impact", "0.0")
            ),
            availability_requirement=Decimal(
                finding.get("availability_requirement", "0.0")
            ),
            confidentiality_impact=Decimal(
                finding.get("confidentiality_impact", "0.0")
            ),
            confidentiality_requirement=Decimal(
                finding.get("confidentiality_requirement", "0.0")
            ),
            exploitability=Decimal(finding.get("exploitability", "0.0")),
            integrity_impact=Decimal(finding.get("integrity_impact", "0.0")),
            integrity_requirement=Decimal(
                finding.get("integrity_requirement", "0.0")
            ),
            modified_attack_complexity=Decimal(
                finding.get("modified_attack_complexity", "0.0")
            ),
            modified_attack_vector=Decimal(
                finding.get("modified_attack_vector", "0.0")
            ),
            modified_availability_impact=Decimal(
                finding.get("modified_availability_impact", "0.0")
            ),
            modified_confidentiality_impact=Decimal(
                finding.get("modified_confidentiality_impact", "0.0")
            ),
            modified_integrity_impact=Decimal(
                finding.get("modified_integrity_impact", "0.0")
            ),
            modified_privileges_required=Decimal(
                finding.get("modified_privileges_required", "0.0")
            ),
            modified_user_interaction=Decimal(
                finding.get("modified_user_interaction", "0.0")
            ),
            modified_severity_scope=Decimal(
                finding.get("modified_severity_scope", "0.0")
            ),
            privileges_required=Decimal(
                finding.get("privileges_required", "0.0")
            ),
            remediation_level=Decimal(finding.get("remediation_level", "0.0")),
            report_confidence=Decimal(finding.get("report_confidence", "0.0")),
            severity_scope=Decimal(finding.get("severity_scope", "0.0")),
            user_interaction=Decimal(finding.get("user_interaction", "0.0")),
        )
    return Finding20Severity(
        access_complexity=Decimal(finding.get("access_complexity", "0.0")),
        access_vector=Decimal(finding.get("access_vector", "0.0")),
        authentication=Decimal(finding.get("authentication", "0.0")),
        availability_impact=Decimal(finding.get("availability_impact", "0.0")),
        availability_requirement=Decimal(
            finding.get("availability_requirement", "0.0")
        ),
        collateral_damage_potential=Decimal(
            finding.get("collateral_damage_potential", "0.0")
        ),
        confidence_level=Decimal(finding.get("confidence_level", "0.0")),
        confidentiality_impact=Decimal(
            finding.get("confidentiality_impact", "0.0")
        ),
        confidentiality_requirement=Decimal(
            finding.get("confidentiality_requirement", "0.0")
        ),
        exploitability=Decimal(finding.get("exploitability", "0.0")),
        finding_distribution=Decimal(
            finding.get("finding_distribution", "0.0")
        ),
        integrity_impact=Decimal(finding.get("integrity_impact", "0.0")),
        integrity_requirement=Decimal(
            finding.get("integrity_requirement", "0.0")
        ),
        resolution_level=Decimal(finding.get("resolution_level", "0.0")),
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
            modified_date=get_as_utc_iso_format(get_from_str(date))
            if date
            else MASKED,
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
        date = get_as_utc_iso_format(
            get_from_str(
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
    progress: float,
    is_deleted: bool = False,
    is_masked: bool = False,
) -> str:
    finding_id: str = old_finding["finding_id"]

    if "project_name" not in old_finding:
        print(f'ERROR - "{finding_id}" project_name missing')
        return ERROR

    if "historic_state" not in old_finding:
        print(f'ERROR - "{finding_id}" historic_state missing')
        return ERROR

    try:
        analyst = old_finding.get("analyst", "")
        historic_state = _fix_historic_state_creation(
            _fix_historic_dates(old_finding["historic_state"]), analyst
        )

        # This add() was modified berofe hand for not populating the initial
        # facets state, unreliable indicators and verification, as they would
        # be overwritten later
        await findings_model.add(
            finding=Finding(
                hacker_email=analyst,
                group_name=old_finding["project_name"],
                id=finding_id,
                state=_format_state(historic_state[0]),
                title=old_finding.get("finding", ""),
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
                verification=None
                if old_finding.get("historic_verification")
                else None,
            )
        )
    except AlreadyCreated:
        print(f'ERROR - "{finding_id}" already created at vms')
        return ERROR

    await _populate_finding_historic_state(
        old_finding["project_name"],
        finding_id,
        historic_state,
    )

    if old_finding.get("historic_verification"):
        historic_verification = _fix_historic_dates(
            old_finding["historic_verification"]
        )
    if old_finding.get("historic_verification"):
        await _populate_finding_historic_verification(
            old_finding["project_name"],
            finding_id,
            historic_verification,
        )

    # It was decided to skip the facet for this states
    if not is_deleted and not is_masked:
        await _populate_finding_unreliable_indicator(
            loaders,
            old_finding["project_name"],
            finding_id,
        )

    if is_deleted:
        await findings_model.remove(
            group_name=old_finding["project_name"],
            finding_id=finding_id,
        )

    print(f'Progress: {round(progress, 4)} - "{finding_id}" migration OK')
    return finding_id


# Delete a previously migrated item as it is no longer needed in the vms table
# or because there is some inconsistency
async def _delete_item(
    table_name: str,
    item: Item,
    progress: float,
) -> bool:
    success = await dynamodb_ops.delete_item(
        table_name,
        DynamoDeleteType(Key={"pk": item["pk"], "sk": item["sk"]}),
    )
    print(
        f"Progress: {round(progress, 4)} - "
        f'" {item["pk"]} : {item["sk"]} " deletion OK'
    )
    return success


def _filter_deleted_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    return [
        finding
        for finding in findings
        if cast(HistoricType, finding.get("historic_state", [{}]))[-1].get(
            "state", ""
        )
        == "DELETED"
    ]


# Delete previous items if needed
async def _clean_findings() -> bool:
    success = False
    start_time = datetime.now()
    scan_attrs: DynamoQueryType = {
        "FilterExpression": Attr("pk").begins_with("FIN")
        | Attr("pk").begins_with("REMOVED"),
    }
    to_delete_findings = await dynamodb_ops.scan(TABLE.name, scan_attrs)
    print(f"--- scan in {datetime.now() - start_time} ---")
    print(f"Items for deletion found: {len(to_delete_findings)}")

    if PROD and len(to_delete_findings) > 0:
        start_time = datetime.now()
        results = await collect(
            _delete_item(
                table_name=TABLE.name,
                item=item,
                progress=count / len(to_delete_findings),
            )
            for count, item in enumerate(to_delete_findings)
        )
        if ERROR not in results:
            success = True
        print(f"--- deletion in {datetime.now() - start_time} ---")

    return success


# Load findings for 'ACTIVE' and 'SUSPENDED' groups,
# excluding findings with 'DELETED' status
async def _migrate_non_deleted_findings(
    loaders: Dataloaders,
    findings: List[FindingType],
) -> bool:
    success = False
    alive_groups = {
        group["project_name"] for group in await groups_dal.get_alive_groups()
    }
    print(f"Alive groups: {len(alive_groups)}")
    non_deleted_findings = [
        finding
        for finding in findings_utils.filter_non_deleted_findings(findings)
        if finding.get("project_name", "") in alive_groups
    ]
    print(f"Non deleted findings: {len(non_deleted_findings)}")

    if PROD:
        start_time = datetime.now()
        results = await collect(
            _proccess_finding(
                loaders=loaders,
                old_finding=old_finding,
                progress=count / len(non_deleted_findings),
            )
            for count, old_finding in enumerate(non_deleted_findings)
        )
        if ERROR not in results:
            success = True
        print(f"--- processing in {datetime.now() - start_time} ---")

    return success


# Deleted findings from these groups are filtered out
async def _migrate_deleted_findings(
    loaders: Dataloaders,
    findings: List[FindingType],
) -> bool:
    success = False
    excluded_groups = ["worcester"]  # Group left out from this migration
    deleted_findings = [
        finding
        for finding in _filter_deleted_findings(findings)
        if finding.get("project_name", "") not in excluded_groups
    ]
    print(f"Deleted findings: {len(deleted_findings)}")

    if PROD:
        start_time = datetime.now()
        results = await collect(
            _proccess_finding(
                loaders=loaders,
                old_finding=old_finding,
                progress=count / len(deleted_findings),
                is_deleted=True,
            )
            for count, old_finding in enumerate(deleted_findings)
        )
        if ERROR not in results:
            success = True
            print(f"--- processing in {datetime.now() - start_time} ---")

    return success


# Load findings for not "alive" groups
# These findings are MASKED or WIPED
async def _migrate_masked_findings(
    loaders: Dataloaders,
    findings: List[FindingType],
) -> bool:
    success = False
    filtering_exp = (
        Attr("project_status").eq("DELETED")
        | Attr("project_status").eq("FINISHED")
        | Attr("project_status").eq("PENDING_DELETION")
    )
    masked_groups = {
        group["project_name"]
        for group in await groups_dal.get_all(filtering_exp=filtering_exp)
    }
    print(f"Masked groups: {len(masked_groups)}")
    masked_findings = [
        finding
        for finding in findings
        if finding.get("project_name", "") in masked_groups
    ]
    print(f"Masked findings: {len(masked_findings)}")

    if PROD:
        start_time = datetime.now()
        results = await collect(
            _proccess_finding(
                loaders=loaders,
                old_finding=old_finding,
                progress=count / len(masked_findings),
                is_masked=True,
            )
            for count, old_finding in enumerate(masked_findings)
        )
        if ERROR not in results:
            success = True
        print(f"--- processing in {datetime.now() - start_time} ---")

    return success


async def main() -> None:
    success = False
    loaders: Dataloaders = get_new_context()

    if CLEAN_FINDINGS:
        await _clean_findings()

    # Scan old findings table
    start_time = datetime.now()
    scan_attrs: DynamoQueryType = {}
    findings: List[FindingType] = await dynamodb_ops.scan(
        FINDING_TABLE, scan_attrs
    )
    print(f"--- scan in {datetime.now() - start_time} ---")
    print(f"Scan findings: {len(findings)}")

    if MIGRATE_NON_DELETED_FINDINGS:
        await _migrate_non_deleted_findings(
            loaders=loaders,
            findings=findings,
        )

    if MIGRATE_DELETED_FINDINGS:
        await _migrate_deleted_findings(
            loaders=loaders,
            findings=findings,
        )

    if MIGRATE_MASKED_FINDINGS:
        await _migrate_masked_findings(
            loaders=loaders,
            findings=findings,
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
