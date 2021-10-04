from custom_exceptions import (
    InvalidDateFormat,
    InvalidFileStructure,
)
from custom_types import (
    Action,
    Datetime,
    Finding as FindingType,
    Historic as HistoricType,
)
import io
import itertools
import logging
import logging.config
from newutils import (
    cvss,
    datetime as datetime_utils,
    forms as forms_utils,
    utils,
)
import re
from settings import (
    LOGGING,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    cast,
    Counter,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
CVSS_PARAMETERS = {
    "2": {
        "bs_factor_1": 0.6,
        "bs_factor_2": 0.4,
        "bs_factor_3": 1.5,
        "impact_factor": 10.41,
        "exploitability_factor": 20,
    },
    "3.1": {
        "impact_factor_1": 6.42,
        "impact_factor_2": 7.52,
        "impact_factor_3": 0.029,
        "impact_factor_4": 3.25,
        "impact_factor_5": 0.02,
        "impact_factor_6": 15,
        "exploitability_factor_1": 8.22,
        "basescore_factor": 1.08,
        "mod_impact_factor_1": 0.915,
        "mod_impact_factor_2": 6.42,
        "mod_impact_factor_3": 7.52,
        "mod_impact_factor_4": 0.029,
        "mod_impact_factor_5": 3.25,
        "mod_impact_factor_6": 0.02,
        "mod_impact_factor_7": 13,
        "mod_impact_factor_8": 0.9731,
    },
}
LOGGER = logging.getLogger(__name__)


async def append_records_to_file(
    records: List[Dict[str, str]], new_file: UploadFile
) -> UploadFile:
    header = records[0].keys()
    values = [list(v) for v in [record.values() for record in records]]
    new_file_records = await new_file.read()
    await new_file.seek(0)
    new_file_header = (
        cast(bytes, new_file_records).decode("utf-8").split("\n")[0]
    )
    new_file_records = r"\n".join(
        cast(bytes, new_file_records).decode("utf-8").split("\n")[1:]
    )
    records_str = ""
    for record in values:
        records_str += repr(str(",".join(record)) + "\n").replace("'", "")
    aux = records_str
    records_str = (
        str(",".join(header))
        + r"\n"
        + aux
        + str(new_file_records).replace("'", "")
    )
    if new_file_header != str(",".join(header)):
        raise InvalidFileStructure()

    buff = io.BytesIO(
        records_str.encode("utf-8").decode("unicode_escape").encode("utf-8")
    )
    uploaded_file = UploadFile(filename=new_file.filename)
    await uploaded_file.write(buff.read())
    await uploaded_file.seek(0)
    return uploaded_file


def clean_deleted_state(
    vuln: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    historic_state = cast(List[Dict[str, str]], vuln.get("historic_state", []))
    new_historic = list(
        filter(
            lambda historic: historic.get("state") != "DELETED", historic_state
        )
    )
    vuln["historic_state"] = new_historic
    return vuln


def filter_by_date(
    historic_items: List[Dict[str, str]], cycle_date: Datetime
) -> List[Dict[str, str]]:
    return list(
        filter(
            lambda historic: historic.get("date")
            and get_item_date(historic) <= cycle_date,
            historic_items,
        )
    )


def filter_non_approved_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    no_approved_findings = [
        finding
        for finding in findings
        if cast(HistoricType, finding.get("historic_state", [{}]))[-1].get(
            "state", ""
        )
        != "APPROVED"
    ]
    return no_approved_findings


def filter_non_created_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    non_submited_findings = [
        finding
        for finding in findings
        if cast(HistoricType, finding.get("historic_state", [{}]))[-1].get(
            "state", ""
        )
        != "CREATED"
    ]
    return non_submited_findings


def filter_non_deleted_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    no_deleted_findings = [
        finding
        for finding in findings
        if cast(HistoricType, finding.get("historic_state", [{}]))[-1].get(
            "state", ""
        )
        != "DELETED"
    ]
    return no_deleted_findings


def filter_non_rejected_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    non_rejected_findings = [
        finding
        for finding in findings
        if cast(HistoricType, finding.get("historic_state", [{}]))[-1].get(
            "state", ""
        )
        != "REJECTED"
    ]
    return non_rejected_findings


def filter_non_submitted_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    non_submitted_findings = [
        finding
        for finding in findings
        if cast(HistoricType, finding.get("historic_state", [{}]))[-1].get(
            "state", ""
        )
        != "SUBMITTED"
    ]
    return non_submitted_findings


# pylint: disable=simplifiable-if-expression
def format_data(finding: Dict[str, FindingType]) -> Dict[str, FindingType]:
    finding = {
        utils.snakecase_to_camelcase(attribute): finding.get(attribute)
        for attribute in finding
    }

    is_draft = not is_released(finding)
    if is_draft:
        finding["cvssVersion"] = finding.get("cvssVersion", "2")

    if "cvssVersion" not in finding:
        finding["cvssVersion"] = "3.1"

    finding["exploitable"] = (
        forms_utils.is_exploitable(
            float(str(finding.get("exploitability", 0))),
            str(finding.get("cvssVersion", "")),
        )
        == "Si"
    )

    historic_verification = cast(
        List[Dict[str, str]], finding.get("historicVerification", [{}])
    )
    finding["remediated"] = (
        historic_verification
        and historic_verification[-1].get("status") == "REQUESTED"
        and not historic_verification[-1].get("vulns", [])
    )

    finding_files = cast(List[Dict[str, str]], finding.get("files", []))
    finding["evidence"] = {
        "animation": get_evidence("animation", finding_files, finding),
        "evidence1": get_evidence("evidence_route_1", finding_files, finding),
        "evidence2": get_evidence("evidence_route_2", finding_files, finding),
        "evidence3": get_evidence("evidence_route_3", finding_files, finding),
        "evidence4": get_evidence("evidence_route_4", finding_files, finding),
        "evidence5": get_evidence("evidence_route_5", finding_files, finding),
        "exploitation": get_evidence("exploitation", finding_files, finding),
    }
    finding["compromisedAttrs"] = finding.get("records", "")
    finding["records"] = get_evidence("fileRecords", finding_files, finding)

    cvss_fields = {
        "2": [
            "accessComplexity",
            "accessVector",
            "authentication",
            "availabilityImpact",
            "availabilityRequirement",
            "collateralDamagePotential",
            "confidenceLevel",
            "confidentialityImpact",
            "confidentialityRequirement",
            "exploitability",
            "findingDistribution",
            "integrityImpact",
            "integrityRequirement",
            "resolutionLevel",
        ],
        "3.1": [
            "attackComplexity",
            "attackVector",
            "availabilityImpact",
            "availabilityRequirement",
            "confidentialityImpact",
            "confidentialityRequirement",
            "exploitability",
            "integrityImpact",
            "integrityRequirement",
            "modifiedAttackComplexity",
            "modifiedAttackVector",
            "modifiedAvailabilityImpact",
            "modifiedConfidentialityImpact",
            "modifiedIntegrityImpact",
            "modifiedPrivilegesRequired",
            "modifiedUserInteraction",
            "modifiedSeverityScope",
            "privilegesRequired",
            "remediationLevel",
            "reportConfidence",
            "severityScope",
            "userInteraction",
        ],
    }
    finding["severity"] = {
        field: cast(str, float(str(finding.get(field, 0))))
        for field in cvss_fields[str(finding["cvssVersion"])]
    }
    base_score = cvss.calculate_cvss_basescore(
        cast(Dict[str, float], finding["severity"]),
        CVSS_PARAMETERS[str(finding["cvssVersion"])],
        str(finding["cvssVersion"]),
    )
    finding["severityCvss"] = cvss.calculate_cvss_temporal(
        cast(Dict[str, float], finding["severity"]),
        base_score,
        str(finding["cvssVersion"]),
    )
    return finding


def format_finding(
    finding: Dict[str, FindingType], attrs: Optional[Set[str]] = None
) -> Dict[str, FindingType]:
    """Returns the data in the format expected by default resolvers"""
    # pylint: disable=unsubscriptable-object
    formated_finding = finding.copy()
    if not attrs or "finding_id" in attrs:
        formated_finding["id"] = finding["finding_id"]
    if not attrs or "finding" in attrs:
        formated_finding["title"] = finding["finding"]
    if not attrs or "historic_state" in attrs:
        formated_finding["historic_state"] = finding.get("historic_state", [])
    return formated_finding


def get_approval_date(finding: Dict[str, FindingType]) -> str:
    """Get approval date from the historic state"""
    approval_date = ""
    approval_info = None
    historic_state = get_historic_state(finding)
    if historic_state:
        approval_info = list(
            filter(
                lambda state_info: state_info["state"] == "APPROVED",
                historic_state,
            )
        )
    if approval_info:
        approval_date = approval_info[-1]["date"]
    return approval_date


def get_creation_date(finding: Dict[str, FindingType]) -> str:
    """Get creation date from the historic state"""
    creation_date = ""
    creation_info = None
    historic_state = get_historic_state(finding)
    if historic_state:
        creation_info = list(
            filter(
                lambda state_info: state_info["state"] == "CREATED",
                historic_state,
            )
        )
    if creation_info:
        creation_date = creation_info[-1]["date"]
    return creation_date


def get_date_with_format(item: Dict[str, str]) -> str:
    return str(item.get("date", "")).split(" ")[0]


def get_evidence(
    name: str,
    items: List[Dict[str, str]],
    finding: Dict[str, FindingType],
) -> Dict[str, str]:
    date_str: str = get_approval_date(finding) or get_creation_date(finding)
    release_date = datetime_utils.get_from_str(date_str)
    evidence = [
        {
            "date": (
                item["upload_date"]
                if datetime_utils.get_from_str(
                    item.get("upload_date", datetime_utils.DEFAULT_STR)
                )
                > release_date
                else date_str
            ),
            "description": item.get("description", ""),
            "url": item["file_url"],
        }
        for item in items
        if item["name"] == name
    ]
    return evidence[0] if evidence else {"url": "", "description": ""}


def get_first_historic_item_date(historic: List[Dict[str, str]]) -> str:
    date: str = ""
    if historic:
        date = get_date_with_format(historic[0])
    return date


def get_historic_dates(vuln: Dict[str, FindingType]) -> List[str]:
    historic_treatment = cast(List[Dict[str, str]], vuln["historic_treatment"])
    historic_state = cast(List[Dict[str, str]], vuln["historic_state"])
    treatment_dates = [
        get_date_with_format(treatment) for treatment in historic_treatment
    ]
    state_dates = [
        get_date_with_format(state)
        for state in historic_state
        if state.get("state", "") in {"open", "closed"}
    ]
    return treatment_dates + state_dates


def get_historic_state(finding: Dict[str, FindingType]) -> HistoricType:
    historic_state = []
    if "historic_state" in finding:
        historic_state = cast(HistoricType, finding["historic_state"])
    elif "historicState" in finding:
        historic_state = cast(HistoricType, finding["historicState"])
    return historic_state


def get_item_date(item: Any) -> Datetime:
    return datetime_utils.get_from_str(item["date"].split(" ")[0], "%Y-%m-%d")


def get_sorted_historics(
    vuln: Dict[str, FindingType]
) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    historic_treatment = cast(
        List[Dict[str, str]], vuln.get("historic_treatment", [])
    )
    historic_state = cast(List[Dict[str, str]], vuln.get("historic_state", []))
    sorted_historic = sort_historic_by_date(historic_state)
    sorted_treatment = sort_historic_by_date(historic_treatment)
    return sorted_historic, sorted_treatment


def get_state_actions(vulns: List[Dict[str, FindingType]]) -> List[Action]:
    states_actions = list(
        itertools.chain.from_iterable(
            get_vuln_state_action(
                sort_historic_by_date(vuln["historic_state"])
            )
            for vuln in vulns
        )
    )
    actions = [
        action._replace(times=times)
        for action, times in Counter(states_actions).most_common()
    ]
    return actions


def get_submission_date(finding: Dict[str, FindingType]) -> str:
    """Get submission date from the historic state"""
    submission_date = ""
    submission_info = None
    historic_state = get_historic_state(finding)
    if historic_state:
        submission_info = list(
            filter(
                lambda state_info: state_info["state"] == "SUBMITTED",
                historic_state,
            )
        )
    if submission_info:
        submission_date = submission_info[-1]["date"]
    return submission_date


def get_tracking_dates(
    vulnerabilities: List[Dict[str, FindingType]]
) -> List[str]:
    """Remove vulnerabilities that changes in the same day."""
    vuln_casted: List[List[str]] = [
        get_historic_dates(vuln) for vuln in vulnerabilities
    ]
    new_casted: List[str] = sorted(
        list({date for dates in vuln_casted for date in dates})
    )
    return new_casted


def get_treatment_actions(vulns: List[Dict[str, FindingType]]) -> List[Action]:
    treatments_actions = list(
        itertools.chain.from_iterable(
            get_vuln_treatment_actions(
                sort_historic_by_date(vuln["historic_treatment"])
            )
            for vuln in vulns
        )
    )
    actions = [
        action._replace(times=times)
        for action, times in Counter(treatments_actions).most_common()
    ]
    return actions


def get_vuln_state_action(historic_state: HistoricType) -> List[Action]:
    actions: List[Action] = [
        Action(
            action=state["state"],
            date=state["date"].split(" ")[0],
            justification="",
            manager="",
            times=1,
        )
        for state in historic_state
    ]
    return list({action.date: action for action in actions}.values())


def get_vuln_treatment_actions(
    historic_treatment: HistoricType,
) -> List[Action]:
    actions: List[Action] = [
        Action(
            action=treatment["treatment"],
            date=treatment["date"].split(" ")[0],
            justification=treatment["justification"],
            manager=treatment["treatment_manager"],
            times=1,
        )
        for treatment in historic_treatment
        if (
            treatment["treatment"] in {"ACCEPTED", "ACCEPTED_UNDEFINED"}
            and treatment.get("acceptance_status")
            not in {"REJECTED", "SUBMITTED"}
        )
    ]
    return list({action.date: action for action in actions}.values())


def is_approved(finding: Dict[str, FindingType]) -> bool:
    """Determine if a finding is approved from the historic state"""
    historic_state = get_historic_state(finding)
    return bool(historic_state and historic_state[-1]["state"] == "APPROVED")


def is_created(finding: Dict[str, FindingType]) -> bool:
    """Determine if a finding is created from the historic state"""
    historic_state = get_historic_state(finding)
    return bool(historic_state and historic_state[-1]["state"] == "CREATED")


def is_deleted(finding: Dict[str, FindingType]) -> bool:
    """Determine if a finding is deleted from the historic state"""
    historic_state = get_historic_state(finding)
    return bool(historic_state and historic_state[-1]["state"] == "DELETED")


def is_released(finding: Dict[str, FindingType]) -> bool:
    """Determine if a finding is released from the historic state"""
    return bool(get_approval_date(finding))


def is_submitted(finding: Dict[str, FindingType]) -> bool:
    """Determine if a finding is submitted from the historic state"""
    historic_state = get_historic_state(finding)
    return bool(historic_state and historic_state[-1]["state"] == "SUBMITTED")


def sort_historic_by_date(historic: Any) -> HistoricType:
    historic_sort = sorted(historic, key=lambda i: i["date"])
    return historic_sort


def validate_acceptance_date(values: Dict[str, str]) -> bool:
    """
    Check that the date set to temporarily accept a finding is logical
    """
    valid: bool = True
    if values["treatment"] == "ACCEPTED":
        if values.get("acceptance_date"):
            today = datetime_utils.get_now_as_str()
            values[
                "acceptance_date"
            ] = f'{values["acceptance_date"].split()[0]} {today.split()[1]}'
            if not datetime_utils.is_valid_format(values["acceptance_date"]):
                raise InvalidDateFormat()
        else:
            raise InvalidDateFormat()
    return valid


def is_valid_finding_title(title: str) -> bool:
    return bool(re.match(r"^[0-9]{3}\. .+", title))
