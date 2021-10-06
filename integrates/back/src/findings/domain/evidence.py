from .core import (
    get_finding,
)
from backports import (  # type: ignore
    csv,
)
from custom_exceptions import (
    EvidenceNotFound,
    InvalidFileSize,
    InvalidFileType,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.enums import (
    FindingEvidenceName,
)
from db_model.findings.types import (
    Finding,
    FindingEvidence,
    FindingEvidenceToUpdate,
)
from findings import (
    dal as findings_dal,
)
import io
import itertools
import logging
import logging.config
from magic import (
    Magic,
)
from newutils import (
    datetime as datetime_utils,
    files as files_utils,
    findings as finding_utils,
    utils,
    validations,
)
from newutils.utils import (
    get_key_or_fallback,
)
from settings import (
    LOGGING,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
EVIDENCE_NAMES = {
    "animation": "animation",
    "evidence_route_1": "evidence1",
    "evidence_route_2": "evidence2",
    "evidence_route_3": "evidence3",
    "evidence_route_4": "evidence4",
    "evidence_route_5": "evidence5",
    "exploitation": "exploitation",
    "fileRecords": "records",
}
LOGGER = logging.getLogger(__name__)


async def download_evidence_file(
    group_name: str, finding_id: str, file_name: str
) -> str:
    file_id = "/".join([group_name.lower(), finding_id, file_name])
    file_exists = await findings_dal.search_evidence(file_id)
    if file_exists:
        start = file_id.find(finding_id) + len(finding_id)
        localfile = f"/tmp{file_id[start:]}"  # nosec
        ext = {".py": ".tmp"}
        tmp_filepath = utils.replace_all(localfile, ext)
        await findings_dal.download_evidence(file_id, tmp_filepath)
        return cast(str, tmp_filepath)
    raise Exception("Evidence not found")


async def get_records_from_file(
    group_name: str, finding_id: str, file_name: str
) -> List[Dict[object, object]]:
    file_path = await download_evidence_file(group_name, finding_id, file_name)
    file_content = []
    encoding = Magic(mime_encoding=True).from_file(file_path)
    try:
        with io.open(file_path, mode="r", encoding=encoding) as records_file:
            csv_reader = csv.reader(records_file)
            max_rows = 1000
            headers = next(csv_reader)
            file_content = [
                utils.list_to_dict(headers, row)
                for row in itertools.islice(csv_reader, max_rows)
            ]
    except (csv.Error, LookupError, UnicodeDecodeError) as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return file_content


async def remove_evidence(evidence_name: str, finding_id: str) -> bool:
    finding = await get_finding(finding_id)
    group_name = get_key_or_fallback(finding, "groupName", "projectName")
    files = cast(List[Dict[str, str]], finding.get("files", []))

    evidence: Dict[str, str] = next(
        (item for item in files if item["name"] == evidence_name), {}
    )
    if not evidence:
        raise EvidenceNotFound()

    evidence_id = str(evidence.get("file_url", ""))
    full_name = f"{group_name}/{finding_id}/{evidence_id}"
    await findings_dal.remove_evidence(full_name)
    index = files.index(evidence)
    del files[index]
    return await findings_dal.update(finding_id, {"files": files})


async def remove_evidence_new(
    loaders: Any, evidence_id: str, finding_id: str
) -> None:
    finding_loader = loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    evidence: Optional[FindingEvidence] = getattr(
        finding.evidences, EVIDENCE_NAMES[evidence_id]
    )
    if not evidence:
        raise EvidenceNotFound()

    full_name = f"{finding.group_name}/{finding.id}/{evidence.url}"
    await findings_dal.remove_evidence(full_name)
    await findings_model.remove_evidence(
        group_name=finding.group_name,
        finding_id=finding.id,
        evidence_name=FindingEvidenceName[EVIDENCE_NAMES[evidence_id]],
    )


async def update_evidence(
    finding_id: str, evidence_type: str, file: UploadFile
) -> bool:
    finding = await get_finding(finding_id)
    files = cast(List[Dict[str, str]], finding.get("files", []))
    group_name = str(
        get_key_or_fallback(finding, "groupName", "projectName", "")
    )
    today = datetime_utils.get_now_as_str()

    if evidence_type == "fileRecords":
        old_file_name: str = next(
            (
                item["file_url"]
                for item in files
                if item["name"] == "fileRecords"
            ),
            "",
        )
        if old_file_name != "":
            old_records = await get_records_from_file(
                group_name, finding_id, old_file_name
            )
            if old_records:
                file = await finding_utils.append_records_to_file(
                    cast(List[Dict[str, str]], old_records), file
                )

    mime_type = await files_utils.get_uploaded_file_mime(file)
    try:
        extension = {
            "image/gif": ".gif",
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "application/x-empty": ".exp",
            "text/x-python": ".exp",
            "application/csv": ".csv",
            "text/csv": ".csv",
            "text/plain": ".txt",
        }[mime_type]
    except KeyError:
        extension = ""
    evidence_id = f"{group_name}-{finding_id}-{evidence_type}{extension}"
    full_name = f"{group_name}/{finding_id}/{evidence_id}"
    await findings_dal.save_evidence(file, full_name)
    evidence: Union[Dict[str, str], List[Optional[Any]]] = next(
        (item for item in files if item["name"] == evidence_type), []
    )
    if evidence:
        index = files.index(cast(Dict[str, str], evidence))
        return await findings_dal.update(
            finding_id,
            {
                f"files[{index}].file_url": evidence_id,
                f"files[{index}].upload_date": today,
            },
        )

    return await findings_dal.list_append(
        finding_id,
        "files",
        [
            {
                "name": evidence_type,
                "file_url": evidence_id,
                "upload_date": today,
            }
        ],
    )


async def update_evidence_new(
    loaders: Any, finding_id: str, evidence_id: str, file: UploadFile
) -> None:
    await validate_evidence(evidence_id, file)
    finding_loader = loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    mime_type = await files_utils.get_uploaded_file_mime(file)
    try:
        extension = {
            "image/gif": ".gif",
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "application/x-empty": ".exp",
            "text/x-python": ".exp",
            "application/csv": ".csv",
            "text/csv": ".csv",
            "text/plain": ".txt",
        }[mime_type]
    except KeyError:
        extension = ""
    filename = f"{finding.group_name}-{finding.id}-{evidence_id}{extension}"
    full_name = f"{finding.group_name}/{finding.id}/{filename}"
    if evidence_id == "fileRecords":
        old_filename = (
            finding.evidences.records.url if finding.evidences.records else ""
        )
        if old_filename != "":
            old_records = await get_records_from_file(
                finding.group_name, finding.id, old_filename
            )
            if old_records:
                file = await finding_utils.append_records_to_file(
                    cast(List[Dict[str, str]], old_records), file
                )

    await findings_dal.save_evidence(file, full_name)
    evidence: Optional[FindingEvidence] = getattr(
        finding.evidences, EVIDENCE_NAMES[evidence_id]
    )
    if evidence:
        evidence_to_update = FindingEvidenceToUpdate(
            url=filename, modified_date=datetime_utils.get_iso_date()
        )
        await findings_model.update_evidence(
            group_name=finding.group_name,
            finding_id=finding.id,
            evidence_name=FindingEvidenceName[EVIDENCE_NAMES[evidence_id]],
            evidence=evidence_to_update,
        )
    else:
        evidence = FindingEvidence(
            description="",
            modified_date=datetime_utils.get_iso_date(),
            url=filename,
        )
        await findings_model.add_evidence(
            group_name=finding.group_name,
            finding_id=finding.id,
            evidence_name=FindingEvidenceName[EVIDENCE_NAMES[evidence_id]],
            evidence=evidence,
        )


async def update_evidence_description(
    finding_id: str, evidence_type: str, description: str
) -> bool:
    validations.validate_fields(cast(List[str], [description]))
    finding = await get_finding(finding_id)
    files = cast(List[Dict[str, str]], finding.get("files", []))
    success = False

    evidence: Union[Dict[str, str], List[Optional[Any]]] = next(
        (item for item in files if item["name"] == evidence_type), []
    )
    if evidence:
        index = files.index(cast(Dict[str, str], evidence))
        success = await findings_dal.update(
            finding_id, {f"files[{index}].description": description}
        )
    else:
        raise EvidenceNotFound()
    return success


async def update_evidence_description_new(
    loaders: Any, finding_id: str, evidence_id: str, description: str
) -> None:
    validations.validate_fields([description])
    finding_loader = loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    evidence: Optional[FindingEvidence] = getattr(
        finding.evidences, EVIDENCE_NAMES[evidence_id]
    )
    if not evidence:
        raise EvidenceNotFound()

    await findings_model.update_evidence(
        group_name=finding.group_name,
        finding_id=finding.id,
        evidence_name=FindingEvidenceName[EVIDENCE_NAMES[evidence_id]],
        evidence=FindingEvidenceToUpdate(description=description),
    )


async def validate_and_upload_evidence(
    finding_id: str, evidence_id: str, file: UploadFile
) -> bool:
    success = False
    if await validate_evidence(evidence_id, file):
        success = await update_evidence(finding_id, evidence_id, file)
    return success


async def validate_evidence(evidence_id: str, file: UploadFile) -> bool:
    mib = 1048576
    success = False
    allowed_mimes = []
    max_size = 10

    if evidence_id in ["animation", "exploitation"]:
        allowed_mimes = ["image/gif", "image/png"]
    elif evidence_id.startswith("evidence"):
        allowed_mimes = ["image/png"]
    elif evidence_id == "fileRecords":
        allowed_mimes = ["text/csv", "text/plain", "application/csv"]

    if not await files_utils.assert_uploaded_file_mime(file, allowed_mimes):
        raise InvalidFileType()

    if await files_utils.get_file_size(file) < max_size * mib:
        success = True
    else:
        raise InvalidFileSize()
    return success
