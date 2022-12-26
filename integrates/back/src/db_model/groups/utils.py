from .enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateJustification,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from .types import (
    Group,
    GroupFile,
    GroupMetadataToUpdate,
    GroupState,
    GroupTreatmentSummary,
    GroupUnreliableIndicators,
    UnfulfilledStandard,
)
from datetime import (
    datetime,
)
from db_model.organizations.utils import (
    add_org_id_prefix,
    format_policies,
)
from db_model.types import (
    CodeLanguage,
)
from db_model.utils import (
    get_as_utc_iso_format,
    get_first_day_iso_date,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Optional,
    Union,
)


def format_files(files: list[dict[str, str]]) -> list[GroupFile]:
    return [
        GroupFile(
            description=file["description"],
            file_name=file["file_name"],
            modified_by=file["modified_by"],
            modified_date=datetime.fromisoformat(file["modified_date"])
            if file.get("modified_date")
            else None,
        )
        for file in files
    ]


def format_files_items(
    files: list[GroupFile],
) -> list[dict[str, Optional[str]]]:
    return [
        {
            "description": file.description,
            "file_name": file.file_name,
            "modified_by": file.modified_by,
            "modified_date": get_as_utc_iso_format(file.modified_date)
            if file.modified_date
            else None,
        }
        for file in files
    ]


def format_group(item: Item) -> Group:
    return Group(
        created_by=item["created_by"],
        created_date=datetime.fromisoformat(item["created_date"]),
        agent_token=item.get("agent_token"),
        business_id=item.get("business_id"),
        business_name=item.get("business_name"),
        context=item.get("context"),
        description=item["description"],
        disambiguation=item.get("disambiguation"),
        files=format_files(item["files"]) if item.get("files") else None,
        language=GroupLanguage[item["language"]],
        name=item["name"],
        organization_id=add_org_id_prefix(item["organization_id"]),
        policies=format_policies(item["policies"])
        if item.get("policies")
        else None,
        sprint_duration=int(item.get("sprint_duration", 1)),
        sprint_start_date=datetime.fromisoformat(item["sprint_start_date"])
        if item.get("sprint_start_date")
        else get_first_day_iso_date(),
        state=format_state(item["state"]),
    )


def format_unreliable_indicators(item: Item) -> GroupUnreliableIndicators:
    return GroupUnreliableIndicators(
        closed_vulnerabilities=int(item["closed_vulnerabilities"])
        if "closed_vulnerabilities" in item
        else None,
        code_languages=[
            CodeLanguage(language=language["language"], loc=language["loc"])
            for language in item["code_languages"]
        ]
        if "code_languages" in item
        else None,
        exposed_over_time_cvssf=item.get("exposed_over_time_cvssf"),
        exposed_over_time_month_cvssf=item.get(
            "exposed_over_time_month_cvssf"
        ),
        exposed_over_time_year_cvssf=item.get("exposed_over_time_year_cvssf"),
        last_closed_vulnerability_days=int(
            item["last_closed_vulnerability_days"]
        )
        if "last_closed_vulnerability_days" in item
        else None,
        last_closed_vulnerability_finding=item.get(
            "last_closed_vulnerability_finding"
        ),
        max_open_severity=item.get("max_open_severity"),
        max_open_severity_finding=item.get("max_open_severity_finding"),
        max_severity=item.get("max_severity"),
        mean_remediate=item.get("mean_remediate"),
        mean_remediate_critical_severity=item.get(
            "mean_remediate_critical_severity"
        ),
        mean_remediate_high_severity=item.get("mean_remediate_high_severity"),
        mean_remediate_low_severity=item.get("mean_remediate_low_severity"),
        mean_remediate_medium_severity=item.get(
            "mean_remediate_medium_severity"
        ),
        open_findings=int(item["open_findings"])
        if "open_findings" in item
        else None,
        open_vulnerabilities=int(item["open_vulnerabilities"])
        if "open_vulnerabilities" in item
        else None,
        remediated_over_time=item.get("remediated_over_time"),
        remediated_over_time_30=item.get("remediated_over_time_30"),
        remediated_over_time_90=item.get("remediated_over_time_90"),
        remediated_over_time_cvssf=item.get("remediated_over_time_cvssf"),
        remediated_over_time_cvssf_30=item.get(
            "remediated_over_time_cvssf_30"
        ),
        remediated_over_time_cvssf_90=item.get(
            "remediated_over_time_cvssf_90"
        ),
        remediated_over_time_month=item.get("remediated_over_time_month"),
        remediated_over_time_month_cvssf=item.get(
            "remediated_over_time_month_cvssf"
        ),
        remediated_over_time_year=item.get("remediated_over_time_year"),
        remediated_over_time_year_cvssf=item.get(
            "remediated_over_time_year_cvssf"
        ),
        treatment_summary=format_treatment_summary(item["treatment_summary"])
        if item.get("treatment_summary")
        else None,
        unfulfilled_standards=[
            UnfulfilledStandard(
                name=standard["name"],
                unfulfilled_requirements=standard["unfulfilled_requirements"],
            )
            for standard in item["unfulfilled_standards"]
        ]
        if "unfulfilled_standards" in item
        else None,
    )


def format_unreliable_indicators_item(
    indicators: GroupUnreliableIndicators,
) -> Item:
    return {
        "closed_vulnerabilities": getattr(
            indicators, "closed_vulnerabilities"
        ),
        "code_languages": [
            format_code_language(code_language)
            for code_language in indicators.code_languages
        ]
        if indicators.code_languages
        else None,
        "exposed_over_time_cvssf": getattr(
            indicators, "exposed_over_time_cvssf"
        ),
        "exposed_over_time_month_cvssf": getattr(
            indicators, "exposed_over_time_month_cvssf"
        ),
        "exposed_over_time_year_cvssf": getattr(
            indicators, "exposed_over_time_year_cvssf"
        ),
        "last_closed_vulnerability_days": getattr(
            indicators, "last_closed_vulnerability_days"
        ),
        "last_closed_vulnerability_finding": getattr(
            indicators, "last_closed_vulnerability_finding"
        ),
        "max_open_severity": getattr(indicators, "max_open_severity"),
        "max_open_severity_finding": getattr(
            indicators, "max_open_severity_finding"
        ),
        "max_severity": getattr(indicators, "max_severity"),
        "mean_remediate": getattr(indicators, "mean_remediate"),
        "mean_remediate_critical_severity": getattr(
            indicators, "mean_remediate_critical_severity"
        ),
        "mean_remediate_high_severity": getattr(
            indicators, "mean_remediate_high_severity"
        ),
        "mean_remediate_low_severity": getattr(
            indicators, "mean_remediate_low_severity"
        ),
        "mean_remediate_medium_severity": getattr(
            indicators, "mean_remediate_medium_severity"
        ),
        "open_findings": getattr(indicators, "open_findings"),
        "open_vulnerabilities": getattr(indicators, "open_vulnerabilities"),
        "remediated_over_time": getattr(indicators, "remediated_over_time"),
        "remediated_over_time_30": getattr(
            indicators, "remediated_over_time_30"
        ),
        "remediated_over_time_90": getattr(
            indicators, "remediated_over_time_90"
        ),
        "remediated_over_time_cvssf": getattr(
            indicators, "remediated_over_time_cvssf"
        ),
        "remediated_over_time_cvssf_30": getattr(
            indicators, "remediated_over_time_cvssf_30"
        ),
        "remediated_over_time_cvssf_90": getattr(
            indicators, "remediated_over_time_cvssf_90"
        ),
        "remediated_over_time_month": getattr(
            indicators, "remediated_over_time_month"
        ),
        "remediated_over_time_month_cvssf": getattr(
            indicators, "remediated_over_time_month_cvssf"
        ),
        "remediated_over_time_year": getattr(
            indicators, "remediated_over_time_year"
        ),
        "remediated_over_time_year_cvssf": getattr(
            indicators, "remediated_over_time_year_cvssf"
        ),
        "treatment_summary": format_treatment_summary_item(
            indicators.treatment_summary
        )
        if indicators.treatment_summary
        else None,
        "unfulfilled_standards": [
            format_unfulfilled_standard_item(unfulfilled_standard)
            for unfulfilled_standard in indicators.unfulfilled_standards
        ]
        if indicators.unfulfilled_standards
        else None,
    }


def format_metadata_item(metadata: GroupMetadataToUpdate) -> Item:
    item = {
        "agent_token": metadata.agent_token,
        "business_id": metadata.business_id,
        "business_name": metadata.business_name,
        "description": metadata.description,
        "disambiguation": metadata.disambiguation,
        "context": metadata.context,
        "sprint_duration": metadata.sprint_duration,
        "sprint_start_date": get_as_utc_iso_format(metadata.sprint_start_date)
        if metadata.sprint_start_date
        else None,
        "files": format_files_items(metadata.files)
        if metadata.files is not None
        else None,
        "language": metadata.language.value if metadata.language else None,
    }
    if metadata.clean_sprint_start_date:
        item["sprint_start_date"] = ""
    return {
        key: None if not value else value
        for key, value in item.items()
        if value is not None
    }


def format_state_managed(managed: Union[bool, str]) -> GroupManaged:
    if not managed:
        return GroupManaged.NOT_MANAGED
    if managed is True:
        return GroupManaged.MANAGED
    return GroupManaged[managed]


def format_state(state: Item) -> GroupState:
    return GroupState(
        comments=state.get("comments"),
        has_machine=state["has_machine"],
        has_squad=state["has_squad"],
        managed=format_state_managed(state["managed"]),
        justification=GroupStateJustification[state["justification"]]
        if state.get("justification")
        else None,
        modified_by=state["modified_by"],
        modified_date=datetime.fromisoformat(state["modified_date"]),
        payment_id=state["payment_id"] if state.get("payment_id") else None,
        pending_deletion_date=datetime.fromisoformat(
            state["pending_deletion_date"]
        )
        if state.get("pending_deletion_date")
        else None,
        service=GroupService[state["service"]]
        if state.get("service")
        else None,
        status=GroupStateStatus[state["status"]],
        tags=set(state["tags"]) if state.get("tags") else None,
        tier=GroupTier[state["tier"]]
        if state.get("tier")
        else GroupTier.OTHER,
        type=GroupSubscriptionType[state["type"]],
    )


def format_treatment_summary(
    treatment_data: dict[str, int]
) -> GroupTreatmentSummary:
    return GroupTreatmentSummary(
        accepted=int(treatment_data["accepted"]),
        accepted_undefined=int(treatment_data["accepted_undefined"]),
        in_progress=int(treatment_data["in_progress"]),
        new=int(treatment_data["new"]),
    )


def format_treatment_summary_item(
    treatment_data: GroupTreatmentSummary,
) -> dict[str, int]:
    return {
        "accepted": treatment_data.accepted,
        "accepted_undefined": treatment_data.accepted_undefined,
        "in_progress": treatment_data.in_progress,
        "new": treatment_data.new,
    }


def format_code_language(
    code_language: CodeLanguage,
) -> dict[str, Union[str, int]]:
    return {
        "language": code_language.language,
        "loc": code_language.loc,
    }


def format_unfulfilled_standard_item(
    unfulfilled_standard: UnfulfilledStandard,
) -> dict[str, Union[str, list[str]]]:
    return {
        "name": unfulfilled_standard.name,
        "unfulfilled_requirements": (
            unfulfilled_standard.unfulfilled_requirements
        ),
    }
