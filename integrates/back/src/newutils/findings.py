from custom_exceptions import (
    InvalidFileStructure,
    InvalidFindingTitle,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
    FindingEvidence,
    FindingVerificationSummary,
)
import io
from newutils import (
    datetime as datetime_utils,
)
import re
import requests  # type: ignore
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    cast,
    Dict,
    List,
    Optional,
)
import yaml  # type: ignore


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


def get_vulns_file() -> Dict:
    """Parses the vulns info yaml from the repo into a dictionary."""
    base_url: str = (
        "https://gitlab.com/api/v4/projects/20741933/repository/files"
    )
    branch_ref: str = "master"
    vulns_file_id = "common%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml"
    url: str = f"{base_url}/{vulns_file_id}/raw?ref={branch_ref}"
    response = requests.get(url)
    return yaml.safe_load(response.text)


def is_valid_finding_title(title: str) -> bool:
    """
    Validates that new Draft and Finding titles conform to the standard
    format and are present in the whitelist.
    """
    if re.match(r"^[0-9]{3}\. .+", title):
        vulns_info: Dict = get_vulns_file()
        try:
            vuln_number: str = title[:3]
            expected_vuln_title: str = vulns_info[vuln_number]["en"]["title"]
            if title == f"{vuln_number}. {expected_vuln_title}":
                return True
            # Invalid non-standard title
            raise InvalidFindingTitle()
        # Invalid vuln number
        except KeyError as error:
            raise InvalidFindingTitle() from error
    # Invalid format
    raise InvalidFindingTitle()


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
) -> Dict[str, Optional[str]]:
    return (
        {
            "date": None,
            "description": None,
            "url": None,
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


def get_formatted_evidence(
    parent: Finding,
) -> Dict[str, Dict[str, Optional[str]]]:
    return {
        "animation": format_evidence(parent, parent.evidences.animation),
        "evidence_1": format_evidence(parent, parent.evidences.evidence1),
        "evidence_2": format_evidence(parent, parent.evidences.evidence2),
        "evidence_3": format_evidence(parent, parent.evidences.evidence3),
        "evidence_4": format_evidence(parent, parent.evidences.evidence4),
        "evidence_5": format_evidence(parent, parent.evidences.evidence5),
        "exploitation": format_evidence(parent, parent.evidences.exploitation),
    }


def is_verified(
    verification_summary: FindingVerificationSummary,
) -> bool:
    return verification_summary.requested == 0
