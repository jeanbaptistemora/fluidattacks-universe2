from .core import (
    get_finding,
)
from backports import (
    csv,
)
from custom_exceptions import (
    EvidenceNotFound,
    InvalidFileName,
    InvalidFileSize,
    InvalidFileType,
)
from dataloaders import (
    Dataloaders,
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
from db_model.groups.types import (
    Group,
)
from findings import (
    storage as findings_storage,
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
    validations as validations_utils,
)
from newutils.reports import (
    get_extension,
)
from organizations.utils import (
    get_organization,
)
from settings import (
    LOGGING,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    cast,
    Optional,
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
    file_exists = await findings_storage.search_evidence(file_id)
    if file_exists:
        start = file_id.find(finding_id) + len(finding_id)
        localfile = f"/tmp{file_id[start:]}"  # nosec
        ext = {".py": ".tmp"}
        tmp_filepath = utils.replace_all(localfile, ext)
        await findings_storage.download_evidence(file_id, tmp_filepath)
        return tmp_filepath
    raise Exception("Evidence not found")


async def get_records_from_file(
    group_name: str, finding_id: str, file_name: str
) -> list[dict[object, object]]:
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


async def remove_evidence(
    loaders: Dataloaders, evidence_id: str, finding_id: str
) -> None:
    finding = await get_finding(loaders, finding_id)
    evidence: Optional[FindingEvidence] = getattr(
        finding.evidences, EVIDENCE_NAMES[evidence_id]
    )
    if not evidence:
        raise EvidenceNotFound()

    full_name = f"{finding.group_name}/{finding.id}/{evidence.url}"
    await findings_storage.remove_evidence(full_name)
    await findings_model.remove_evidence(
        group_name=finding.group_name,
        finding_id=finding.id,
        evidence_name=FindingEvidenceName[EVIDENCE_NAMES[evidence_id]],
    )


async def validate_filename(
    loaders: Dataloaders, filename: str, finding: Finding
) -> None:
    group: Group = await loaders.group.load(finding.group_name)
    organization = await get_organization(loaders, group.organization_id)
    filename = filename.lower()
    validate_evidencename(
        organization_name=organization.name.lower(),
        group_name=group.name.lower(),
        filename=filename,
    )


def validate_evidencename(
    *, organization_name: str, group_name: str, filename: str
) -> None:
    detail: str = (
        "Format organizationName-groupName-10 alphanumeric chars.extension"
    )
    starts: str = f"{organization_name.lower()}-{group_name.lower()}-"
    if not filename.startswith(starts):
        raise InvalidFileName(detail)

    ends: str = filename.rsplit(".", 1)[-1]
    value: str = filename.replace(starts, "").replace(f".{ends}", "")
    if len(value) != 10 or not value.isalnum():
        raise InvalidFileName(detail)


async def replace_different_format(
    *,
    finding: Finding,
    evidence: FindingEvidence,
    extension: str,
    evidence_id: str,
) -> None:
    old_full_name = f"{finding.group_name}/{finding.id}/{evidence.url}"
    ends: str = old_full_name.rsplit(".", 1)[-1]
    if (
        evidence_id != "fileRecords"
        and ends != old_full_name
        and f".{ends}" != extension
    ):
        await findings_storage.remove_evidence(old_full_name)


async def update_evidence(  # pylint: disable = too-many-arguments
    loaders: Dataloaders,
    finding_id: str,
    evidence_id: str,
    file_object: UploadFile,
    description: Optional[str] = None,
    validate_name: Optional[bool] = False,
) -> None:
    finding = await get_finding(loaders, finding_id)
    await validate_evidence(
        evidence_id, file_object, loaders, finding, validate_name
    )
    mime_type = await files_utils.get_uploaded_file_mime(file_object)
    extension = get_extension(mime_type)
    filename = f"{finding.group_name}-{finding.id}-{evidence_id}{extension}"
    if evidence_id == "fileRecords":
        old_filename = (
            finding.evidences.records.url if finding.evidences.records else ""
        )
        if old_filename != "":
            old_records = await get_records_from_file(
                finding.group_name, finding.id, old_filename
            )
            if old_records:
                file_object = await finding_utils.append_records_to_file(
                    cast(list[dict[str, str]], old_records), file_object
                )

    await findings_storage.save_evidence(
        file_object, f"{finding.group_name}/{finding.id}/{filename}"
    )
    evidence: Optional[FindingEvidence] = getattr(
        finding.evidences, EVIDENCE_NAMES[evidence_id]
    )
    if evidence:
        await replace_different_format(
            finding=finding,
            evidence=evidence,
            extension=extension,
            evidence_id=evidence_id,
        )
        evidence_to_update = FindingEvidenceToUpdate(
            url=filename,
            modified_date=datetime_utils.get_utc_now(),
            description=description,
        )
        await findings_model.update_evidence(
            current_value=evidence,
            group_name=finding.group_name,
            finding_id=finding.id,
            evidence_name=FindingEvidenceName[EVIDENCE_NAMES[evidence_id]],
            evidence=evidence_to_update,
        )
    else:
        evidence = FindingEvidence(
            description=description or "",
            modified_date=datetime_utils.get_utc_now(),
            url=filename,
        )
        await findings_model.add_evidence(
            group_name=finding.group_name,
            finding_id=finding.id,
            evidence_name=FindingEvidenceName[EVIDENCE_NAMES[evidence_id]],
            evidence=evidence,
        )


async def update_evidence_description(
    loaders: Dataloaders, finding_id: str, evidence_id: str, description: str
) -> None:
    validations_utils.validate_fields([description])
    validations_utils.validate_field_length(description, 5000)
    finding = await get_finding(loaders, finding_id)
    evidence: Optional[FindingEvidence] = getattr(
        finding.evidences, EVIDENCE_NAMES[evidence_id]
    )
    if not evidence:
        raise EvidenceNotFound()

    await findings_model.update_evidence(
        current_value=evidence,
        group_name=finding.group_name,
        finding_id=finding.id,
        evidence_name=FindingEvidenceName[EVIDENCE_NAMES[evidence_id]],
        evidence=FindingEvidenceToUpdate(description=description),
    )


async def validate_evidence(
    evidence_id: str,
    file: UploadFile,
    loaders: Dataloaders,
    finding: Finding,
    validate_name: Optional[bool] = False,
) -> bool:
    mib = 1048576
    success = False
    allowed_mimes = []
    max_size = 10

    validations_utils.validate_fields([file.content_type])
    validations_utils.validate_file_name(file.filename)

    if evidence_id in ["animation", "exploitation"]:
        allowed_mimes = ["image/png", "video/webm"]
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

    if validate_name:
        await validate_filename(loaders, file.filename, finding)

    return success
