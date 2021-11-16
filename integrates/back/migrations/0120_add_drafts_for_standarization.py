# pylint: disable=invalid-name
"""
This migration aims to create the needed drafts for continuing with
the findings standarization.

The new drafts info are uploaded from a csv.

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/4903

Execution Time:    2021-08-19 at 11:19:50 UTC-05
Finalization Time: 2021-08-19 at 11:21:48 UTC-05

Execution Time:    2021-08-20 at 21:22:10 UTC-05
Finalization Time: 2021-08-20 at 21:33:12 UTC-05

Execution Time:    2021-08-23 at 09:59:38 UTC-05
Finalization Time: 2021-08-23 at 11:55:16 UTC-05

Execution Time:    2021-08-23 at 14:26:22 UTC-05
Finalization Time: 2021-08-23 at 16:08:33 UTC-05

Execution Time:    2021-08-24 at 09:35:14 UTC-05
Finalization Time: 2021-08-24 at 11:20:03 UTC-05

Execution Time:    2021-08-24 at 12:16:32 UTC-05
Finalization Time: 2021-08-24 at 13:03:30 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
import csv
from custom_exceptions import (
    InvalidFindingTitle,
)
from custom_types import (
    Finding as FindingType,
    Historic as HistoricType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from findings import (
    dal as findings_dal,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
)
import time
from typing import (
    Any,
    cast,
    Dict,
)
import uuid
import yaml  # type: ignore

PROD: bool = True

attackComplexityOptions = {  # noqa
    "H": "0.44",
    "L": "0.77",
}

attackVectorOptions = {  # noqa
    "A": "0.62",
    "L": "0.55",
    "N": "0.85",
    "P": "0.2",
}

availabilityImpactOptions = {  # noqa
    "H": "0.56",
    "L": "0.22",
    "N": "0",
}

confidentialityImpactOptions = {  # noqa
    "H": "0.56",
    "L": "0.22",
    "N": "0",
}

exploitabilityOptions = {  # noqa
    "F": "0.97",
    "H": "1",
    "P": "0.94",
    "U": "0.91",
}

integrityImpactOptions = {  # noqa
    "H": "0.56",
    "L": "0.22",
    "N": "0",
}

severityScopeOptions = {  # noqa
    "C": "1",
    "U": "0",
}

privilegesRequiredScope = {  # noqa
    "H": "0.5",
    "L": "0.68",
    "N": "0.85",
}

privilegesRequiredNoScope = {  # noqa
    "H": "0.27",
    "L": "0.62",
    "N": "0.85",
}

remediationLevelOptions = {  # noqa
    "O": "0.95",
    "T": "0.96",
    "U": "1",
    "W": "0.97",
}

reportConfidenceOptions = {  # noqa
    "C": "1",
    "R": "0.96",
    "U": "0.92",
}

userInteractionOptions = {  # noqa
    "N": "0.85",
    "R": "0.62",
}


def _validate_not_empty(field: str) -> str:
    if field != "__empty__" and field != "X":  # noqa
        return field.strip()
    return ""


def _get_privileges_required(
    severityScope: str,  # noqa
    privilegesRequired: str,
) -> str:
    if severityScope == severityScopeOptions["C"]:
        return privilegesRequiredScope[privilegesRequired]
    return privilegesRequiredNoScope[privilegesRequired]


def _get_draft_data(  # noqa
    data: Any,
    draft_name: str,
    language: str,
) -> Dict[str, str]:
    cve = draft_name[:3]
    criteria = data[cve]

    if draft_name != f'{cve}. {criteria[language]["title"]}':
        print(f"   --- ERROR draft name NOT compliant: {draft_name}")
        return {}

    # Create finding data
    attackVectorRaw = _validate_not_empty(  # noqa
        criteria["score"]["base"]["attack_vector"]
    )
    attackComplexityRaw = _validate_not_empty(  # noqa
        criteria["score"]["base"]["attack_complexity"]
    )
    availabilityRaw = _validate_not_empty(  # noqa
        criteria["score"]["base"]["availability"]
    )
    confidentialityRaw = _validate_not_empty(  # noqa
        criteria["score"]["base"]["confidentiality"]
    )
    exploitabilityRaw = _validate_not_empty(  # noqa
        criteria["score"]["temporal"]["exploit_code_maturity"]
    )
    integrityRaw = _validate_not_empty(  # noqa
        criteria["score"]["base"]["integrity"]
    )
    privilegesRequiredRaw = _validate_not_empty(  # noqa
        criteria["score"]["base"]["privileges_required"]
    )
    remediationLevelRaw = _validate_not_empty(  # noqa
        criteria["score"]["temporal"]["remediation_level"]
    )
    reportConfidenceRaw = _validate_not_empty(  # noqa
        criteria["score"]["temporal"]["report_confidence"]
    )
    scopeRaw = _validate_not_empty(criteria["score"]["base"]["scope"])  # noqa
    userInteractionRaw = _validate_not_empty(  # noqa
        criteria["score"]["base"]["user_interaction"]
    )
    draft_data = {
        "attack_complexity": attackComplexityOptions[attackComplexityRaw]
        if attackComplexityRaw in attackComplexityOptions
        else "",
        "attack_vector": attackVectorOptions[attackVectorRaw]
        if attackVectorRaw in attackVectorOptions
        else "",
        "attack_vector_desc": _validate_not_empty(
            criteria[language]["impact"]
        ),
        "availability_impact": availabilityImpactOptions[availabilityRaw]
        if availabilityRaw in availabilityImpactOptions
        else "",
        "confidentiality_impact": confidentialityImpactOptions[
            confidentialityRaw
        ]
        if confidentialityRaw in confidentialityImpactOptions
        else "",
        "description": _validate_not_empty(criteria[language]["description"]),
        "exploitability": exploitabilityOptions[exploitabilityRaw]
        if exploitabilityRaw in exploitabilityOptions
        else "",
        "integrity_impact": integrityImpactOptions[integrityRaw]
        if integrityRaw in integrityImpactOptions
        else "",
        "privileges_required": _get_privileges_required(
            severityScopeOptions[scopeRaw]
            if scopeRaw in severityScopeOptions
            else "",
            privilegesRequiredRaw,
        ),
        "recommendation": _validate_not_empty(
            criteria[language]["recommendation"]
        ),
        "remediation_level": remediationLevelOptions[remediationLevelRaw]
        if remediationLevelRaw in remediationLevelOptions
        else "",
        "report_confidence": reportConfidenceOptions[reportConfidenceRaw]
        if reportConfidenceRaw in reportConfidenceOptions
        else "",
        "requirements": _validate_not_empty(
            ",".join(criteria["requirements"])
        ),
        "severity_scope": severityScopeOptions[scopeRaw]
        if scopeRaw in severityScopeOptions
        else "",
        "threat": _validate_not_empty(criteria[language]["threat"]),
        "title": f'{cve}. {criteria[language]["title"]}',
        "user_interaction": userInteractionOptions[userInteractionRaw]
        if userInteractionRaw in userInteractionOptions
        else "",
    }
    return draft_data


async def _add_draft(
    group_name: str,
    analyst_email: str,
    source: str,
    draft_data: Dict[str, str],
) -> bool:
    finding_id = str(uuid.uuid4())
    group_name = group_name.lower()
    creation_date = datetime_utils.get_now_as_str()
    submission_history = {
        "analyst": analyst_email,
        "date": creation_date,
        "source": source,
        "state": "CREATED",
    }

    if "description" in draft_data:
        draft_data["vulnerability"] = draft_data.pop("description")
    if "recommendation" in draft_data:
        draft_data["effect_solution"] = draft_data.pop("recommendation")
    if "type" in draft_data:
        draft_data["finding_type"] = draft_data.pop("type")

    finding_attrs: Dict[str, Any] = draft_data.copy()
    finding_attrs.update(
        {
            "analyst": analyst_email,
            "cvss_version": "3.1",
            "files": [],
            "finding": draft_data["title"],
            "historic_state": [submission_history],
        }
    )

    if findings_utils.is_valid_finding_title(draft_data["title"]):
        return await findings_dal.add(finding_id, group_name, finding_attrs)
    raise InvalidFindingTitle()


def _get_finding_source(finding: Dict[str, FindingType]) -> str:
    historic_state = cast(HistoricType, finding.get("historic_state", [{}]))
    source = historic_state[0].get("source", "")
    if source.lower() == "skims":
        source = "machine"
    if source.lower() == "integrates":
        source = "asm"
    return source


async def process_draft(  # noqa
    context: Dataloaders,
    data: Any,
    new_draft: Dict[str, str],
) -> bool:
    group_name = new_draft["group_name"]
    new_draft_title = new_draft["new_draft"]

    group_loader = context.group
    group = await group_loader.load(group_name)
    language = group["language"]

    group_findings_loader = context.group_findings
    group_findings = await group_findings_loader.load(group_name)
    group_findings_titles = [finding["title"] for finding in group_findings]
    if new_draft_title in group_findings_titles:
        print(
            f"   --- WARNING {group_name}, "
            f'finding "{new_draft_title}" ALREADY in db'
        )
        return True

    group_drafts_loader = context.group_drafts
    group_drafts = await group_drafts_loader.load(group_name)
    group_drafts_titles = [draft["title"] for draft in group_drafts]
    if new_draft_title in group_drafts_titles:
        print(
            f"   --- WARNING {group_name}, "
            f'draft "{new_draft_title}" ALREADY in db'
        )
        return True

    old_finding_id = new_draft["finding_id"]
    old_finding: Dict[str, FindingType] = await findings_dal.get_finding(
        old_finding_id
    )
    affected_systems = old_finding.get("affected_systems", "")
    analyst_email = old_finding["analyst"]
    source = _get_finding_source(old_finding)
    draft_data = _get_draft_data(data, new_draft["new_draft"], language)
    if not draft_data:
        print(f"   --- ERROR with draft_data {group_name}: {draft_data}")
        return False
    draft_data["affected_systems"] = affected_systems
    draft_data["exploitability"] = old_finding.get("exploitability", "")
    draft_data["remediation_level"] = old_finding.get("remediation_level", "")
    draft_data["report_confidence"] = old_finding.get("report_confidence", "")

    success = False
    if PROD:
        success = await _add_draft(
            group_name, analyst_email, source, draft_data
        )
        print(
            f"   === draft {group_name} - "
            f'"{new_draft["new_draft"]}" created: {success}'
        )
    else:
        print(
            f"   === draft_data {group_name} - "
            f'{new_draft["new_draft"]} parsed OK'
        )
    return success


async def main() -> None:
    # Read file with new drafts info
    with open("0120.csv", mode="r", encoding="utf8") as f:
        reader = csv.reader(f)
        new_drafts_info = [
            {
                "group_name": row[0],
                "new_draft": row[1],
                "finding_id": row[2],
            }
            for row in reader
            if row[0] != "group_name"
        ]
    print(f"   === new drafts: {len(new_drafts_info)}")
    print(f"   === sample: {new_drafts_info[:1]}")

    # Read file with criteria
    with open(
        "../../../makes/makes/criteria/src/vulnerabilities/data.yaml",
        mode="r",
        encoding="utf8",
    ) as data_yaml:
        criteria_data = yaml.safe_load(data_yaml)

    context: Dataloaders = get_new_context()
    success = all(
        await collect(
            [
                process_draft(context, criteria_data, new_draft)
                for new_draft in new_drafts_info
            ]
        )
    )

    print(f"   === success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
