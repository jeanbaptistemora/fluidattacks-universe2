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
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
    FindingEvidence,
)
import io
import itertools
from newutils import (
    datetime as datetime_utils,
)
import re
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
)


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


def get_item_date(item: Any) -> Datetime:
    return datetime_utils.get_from_str(item["date"].split(" ")[0], "%Y-%m-%d")


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


def get_updated_evidence_date(
    finding: Finding, evidence: FindingEvidence
) -> datetime:
    evidence_date = datetime.fromisoformat(evidence.modified_date)
    updated_date = evidence_date
    if finding.approval:
        release_date = datetime.fromisoformat(finding.approval.modified_date)
        if release_date > evidence_date:
            updated_date = release_date
    return updated_date


def format_evidence(
    finding: Finding, evidence: Optional[FindingEvidence]
) -> Dict[str, str]:
    return (
        {
            "description": "",
            "url": "",
        }
        if evidence is None
        else {
            "date": datetime_utils.get_as_str(
                get_updated_evidence_date(finding, evidence)
            ),
            "description": evidence.description,
            "url": evidence.url,
        }
    )


def get_formatted_evidence(parent: Finding) -> Dict[str, Dict[str, str]]:
    return {
        "animation": format_evidence(parent, parent.evidences.animation),
        "evidence1": format_evidence(parent, parent.evidences.evidence1),
        "evidence2": format_evidence(parent, parent.evidences.evidence2),
        "evidence3": format_evidence(parent, parent.evidences.evidence3),
        "evidence4": format_evidence(parent, parent.evidences.evidence4),
        "evidence5": format_evidence(parent, parent.evidences.evidence5),
        "exploitation": format_evidence(parent, parent.evidences.exploitation),
    }
