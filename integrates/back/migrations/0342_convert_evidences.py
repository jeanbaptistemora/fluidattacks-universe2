# pylint: disable=invalid-name
"""
try to convert evidences in S3 from gif to webm
First Execution Time:      2022-12-28 at 05:38:17 UTC
First Finalization Time:   2022-12-28 at 07:56:51 UTC
Second Execution Time:     2022-12-28 at 22:53:18 UTC
Second Finalization Time:  2022-12-29 at 07:50:13 UTC
Third Execution Time:      2022-12-30 at 15:05:22 UTC
Third Finalization Time:   2022-12-30 at 23:40:54 UTC
Fourth Execution Time:     2022-12-31 at 00:45:54 UTC
Fourth Finalization Time:  2022-12-31 at 09:38:27 UTC
Fifth Execution Time:      2022-12-31 at 17:35:04 UTC
Fifth Finalization Time:   2022-12-31 at 20:29:51 UTC

"""
from aioextensions import (
    collect,
    run,
)
import aiohttp
import asyncio
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidFileSize,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.events import (
    update_evidence as update_model_evidence,
)
from db_model.events.enums import (
    EventEvidenceId,
)
from db_model.events.types import (
    EventEvidence,
    EventEvidences,
    GroupEventsRequest,
)
from db_model.findings import (
    update_evidence as update_modal_evidence,
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
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    retry_on_exceptions,
)
from events import (
    domain as events_domain,
)
from events.domain import (
    replace_different_format as replace_event_different_format,
    save_evidence as save_event_evidence,
)
from findings.domain.evidence import (
    replace_different_format,
    validate_evidence,
)
from findings.storage import (
    save_evidence,
)
import logging
import logging.config
import magic
from newutils.files import (
    get_uploaded_file_mime,
)
from newutils.reports import (
    get_extension,
)
from newutils.validations import (
    validate_sanitized_csv_input,
)
from organizations import (
    domain as orgs_domain,
)
import os
from s3.operations import (
    download_file,
    list_files,
)
from settings import (
    LOGGING,
)
from starlette.datastructures import (
    UploadFile,
)
import time
from typing import (
    Optional,
)
import uuid

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)

download_evidence_file = retry_on_exceptions(
    exceptions=(
        aiohttp.ClientError,
        aiohttp.ClientPayloadError,
    ),
    max_attempts=5,
    sleep_seconds=float("1.1"),
)(download_file)


async def _update_event_evidence(
    loaders: Dataloaders,
    event_id: str,
    evidence_id: EventEvidenceId,
    file: UploadFile,
    update_date: datetime,
) -> None:
    validate_sanitized_csv_input(event_id)
    event = await events_domain.get_event(loaders, event_id)

    extension = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf",
        "application/zip": ".zip",
        "text/csv": ".csv",
        "text/plain": ".txt",
        "video/webm": ".webm",
    }.get(file.content_type, "")
    group_name = event.group_name
    file_name = (
        f"{group_name}_{event_id}_evidence_"
        f"{str(evidence_id.value).lower()}{extension}"
    )
    full_name = f"{group_name}/{event_id}/{file_name}"
    validate_sanitized_csv_input(file.filename, file.content_type, full_name)

    await collect(
        (
            save_event_evidence(file, full_name),
            update_model_evidence(
                event_id=event_id,
                group_name=group_name,
                evidence_info=EventEvidence(
                    file_name=file_name,
                    modified_date=update_date,
                ),
                evidence_id=evidence_id,
            ),
        )
    )

    await replace_event_different_format(
        event=event, evidence_id=evidence_id, extension=extension
    )


async def _update_finding_evidence(
    *,
    loaders: Dataloaders,
    finding_id: str,
    evidence_id: str,
    file_object: UploadFile,
    modified_date: datetime,
    description: Optional[str] = None,
    validate_name: Optional[bool] = False,
) -> None:
    finding: Finding = await loaders.finding.load(finding_id)  # type:ignore
    await validate_evidence(
        evidence_id, file_object, loaders, finding, validate_name
    )
    mime_type = await get_uploaded_file_mime(file_object)
    extension = get_extension(mime_type)
    filename = f"{finding.group_name}-{finding.id}-{evidence_id}{extension}"

    await save_evidence(
        file_object, f"{finding.group_name}/{finding.id}/{filename}"
    )
    evidence: Optional[FindingEvidence] = getattr(
        finding.evidences, evidence_id
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
            modified_date=modified_date,
            description=description,
        )
        await update_modal_evidence(
            current_value=evidence,
            group_name=finding.group_name,
            finding_id=finding.id,
            evidence_name=FindingEvidenceName[evidence_id],
            evidence=evidence_to_update,
        )


async def update_finding_evidence(
    *,
    loaders: Dataloaders,
    full_path: str,
    group_name: str,
    finding_id: str,
    evidence_id: str,
    organization_name: str,
    modified_date: datetime,
) -> None:
    filename = (
        f"{organization_name}-{group_name}"
        f'-{str(uuid.uuid4()).replace("-", "")[:10]}.webm'
    )
    new_file_path = f"evidences/{group_name.lower()}/{finding_id}/{filename}"
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-i",
        os.path.join(os.getcwd(), full_path),
        "-c",
        "vp9",
        "-b:v",
        "0",
        "-crf",
        "20",
        os.path.join(os.getcwd(), new_file_path),
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        LOGGER.info(
            "Updating converted finding evidence",
            extra={
                "extra": {
                    "group_name": group_name,
                    "finding_id": finding_id,
                    "full_path": full_path,
                    "stdout": stdout,
                }
            },
        )
        with open(new_file_path, "rb") as webm_file:
            uploaded_file = UploadFile(filename, webm_file, "video/webm")
            try:
                await _update_finding_evidence(
                    loaders=loaders,
                    finding_id=finding_id,
                    evidence_id=evidence_id,
                    modified_date=modified_date,
                    file_object=uploaded_file,
                    validate_name=True,
                )
            except InvalidFileSize as exc:
                LOGGER.error(
                    "Error saving finding evidence",
                    extra={
                        "extra": {
                            "error": exc,
                            "group_name": group_name,
                            "finding_id": finding_id,
                            "full_path": full_path,
                        }
                    },
                )
        return

    LOGGER.error(
        "Error converting finding evidence",
        extra={
            "extra": {
                "error": stderr.decode(),
                "group_name": group_name,
                "finding_id": finding_id,
                "full_path": full_path,
            }
        },
    )


async def update_event_evidence(
    *,
    loaders: Dataloaders,
    full_path: str,
    group_name: str,
    event_id: str,
    evidence_id: str,
    organization_name: str,
    modified_date: datetime,
) -> None:
    filename = (
        f"{organization_name}-{group_name}"
        f'-{str(uuid.uuid4()).replace("-", "")[:10]}.webm'
    )
    new_file_path = f"evidences/{group_name.lower()}/{event_id}/{filename}"
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-i",
        os.path.join(os.getcwd(), full_path),
        "-c",
        "vp9",
        "-b:v",
        "0",
        "-crf",
        "20",
        os.path.join(os.getcwd(), new_file_path),
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        LOGGER.info(
            "Updating converted event evidence",
            extra={
                "extra": {
                    "group_name": group_name,
                    "event_id": event_id,
                    "full_path": full_path,
                    "stdout": stdout,
                }
            },
        )
        with open(new_file_path, "rb") as webm_file:
            uploaded_file = UploadFile(filename, webm_file, "video/webm")
            try:
                await _update_event_evidence(
                    loaders=loaders,
                    event_id=event_id,
                    evidence_id=EventEvidenceId[evidence_id],
                    file=uploaded_file,
                    update_date=modified_date,
                )
            except InvalidFileSize as exc:
                LOGGER.error(
                    "Error saving event evidence",
                    extra={
                        "extra": {
                            "error": exc,
                            "group_name": group_name,
                            "event_id": event_id,
                            "full_path": full_path,
                        }
                    },
                )
        return

    LOGGER.error(
        "Error converting event evidence",
        extra={
            "extra": {
                "error": stderr.decode(),
                "group_name": group_name,
                "event_id": event_id,
                "full_path": full_path,
            }
        },
    )


async def update_finding_evidences(
    *,
    loaders: Dataloaders,
    group_name: str,
    finding_id: str,
    url: str,
    evidence_id: str,
    organization_name: str,
    modified_date: datetime,
) -> None:
    evidences_path: str = f"evidences/{group_name.lower()}/{finding_id}/{url}"
    evidences = list(await list_files(evidences_path))
    if evidences:
        for evidence in evidences:
            with suppress(OSError):
                os.makedirs(
                    os.path.join(os.getcwd(), evidences_path.rsplit("/", 1)[0])
                )
            try:
                await download_evidence_file(
                    evidence,
                    evidences_path,
                )
            except (
                aiohttp.ClientError,
                aiohttp.ClientPayloadError,
            ) as exc:
                LOGGER.error(
                    "Error downloading finding evidence",
                    extra={
                        "extra": {
                            "error": exc,
                            "group_name": group_name,
                            "finding_id": finding_id,
                            "full_path": evidences_path,
                        }
                    },
                )
                return

            mime_type = magic.from_file(evidences_path, mime=True)
            if mime_type == "image/gif":
                await update_finding_evidence(
                    loaders=loaders,
                    full_path=evidences_path,
                    group_name=group_name,
                    finding_id=finding_id,
                    evidence_id=evidence_id,
                    organization_name=organization_name,
                    modified_date=modified_date,
                )


async def _update_event_evidences(
    *,
    loaders: Dataloaders,
    group_name: str,
    event_id: str,
    url: str,
    evidence_id: str,
    organization_name: str,
    modified_date: datetime,
) -> None:
    evidences_path: str = f"evidences/{group_name.lower()}/{event_id}/{url}"
    evidences = list(await list_files(evidences_path))
    if evidences:
        for evidence in evidences:
            with suppress(OSError):
                os.makedirs(
                    os.path.join(os.getcwd(), evidences_path.rsplit("/", 1)[0])
                )
            try:
                await download_evidence_file(
                    evidence,
                    evidences_path,
                )
            except (
                aiohttp.ClientError,
                aiohttp.ClientPayloadError,
            ) as exc:
                LOGGER.error(
                    "Error downloading event evidence",
                    extra={
                        "extra": {
                            "error": exc,
                            "group_name": group_name,
                            "event_id": event_id,
                            "full_path": evidences_path,
                        }
                    },
                )
                return

            mime_type = magic.from_file(evidences_path, mime=True)
            if mime_type == "image/gif":
                await update_event_evidence(
                    loaders=loaders,
                    full_path=evidences_path,
                    group_name=group_name,
                    event_id=event_id,
                    evidence_id=evidence_id,
                    organization_name=organization_name,
                    modified_date=modified_date,
                )


async def update_event_evidences(
    *,
    loaders: Dataloaders,
    group_name: str,
    event_id: str,
    evidences: EventEvidences,
    organization_name: str,
) -> None:
    if (
        evidences.image_1 is not None
        and evidences.image_1.file_name.lower().endswith(".gif")
    ):
        await _update_event_evidences(
            loaders=loaders,
            group_name=group_name,
            event_id=event_id,
            url=evidences.image_1.file_name,
            evidence_id="IMAGE_1",
            organization_name=organization_name,
            modified_date=evidences.image_1.modified_date,
        )
    if (
        evidences.image_2 is not None
        and evidences.image_2.file_name.lower().endswith(".gif")
    ):
        await _update_event_evidences(
            loaders=loaders,
            group_name=group_name,
            event_id=event_id,
            url=evidences.image_2.file_name,
            evidence_id="IMAGE_2",
            organization_name=organization_name,
            modified_date=evidences.image_2.modified_date,
        )
    if (
        evidences.image_3 is not None
        and evidences.image_3.file_name.lower().endswith(".gif")
    ):
        await _update_event_evidences(
            loaders=loaders,
            group_name=group_name,
            event_id=event_id,
            url=evidences.image_3.file_name,
            evidence_id="IMAGE_3",
            organization_name=organization_name,
            modified_date=evidences.image_3.modified_date,
        )
    if (
        evidences.image_4 is not None
        and evidences.image_4.file_name.lower().endswith(".gif")
    ):
        await _update_event_evidences(
            loaders=loaders,
            group_name=group_name,
            event_id=event_id,
            url=evidences.image_4.file_name,
            evidence_id="IMAGE_4",
            organization_name=organization_name,
            modified_date=evidences.image_4.modified_date,
        )
    if (
        evidences.image_5 is not None
        and evidences.image_5.file_name.lower().endswith(".gif")
    ):
        await _update_event_evidences(
            loaders=loaders,
            group_name=group_name,
            event_id=event_id,
            url=evidences.image_5.file_name,
            evidence_id="IMAGE_5",
            organization_name=organization_name,
            modified_date=evidences.image_5.modified_date,
        )
    if (
        evidences.image_6 is not None
        and evidences.image_6.file_name.lower().endswith(".gif")
    ):
        await _update_event_evidences(
            loaders=loaders,
            group_name=group_name,
            event_id=event_id,
            url=evidences.image_6.file_name,
            evidence_id="IMAGE_6",
            organization_name=organization_name,
            modified_date=evidences.image_6.modified_date,
        )


async def process_group(
    *,
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group: Group = await loaders.group.load(group_name)
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    group_findings = await loaders.group_drafts_and_findings.load(group_name)

    await collect(
        tuple(
            update_finding_evidences(
                loaders=loaders,
                group_name=finding.group_name,
                finding_id=finding.id,
                url=finding.evidences.animation.url,
                evidence_id="animation",
                organization_name=organization.name,
                modified_date=finding.evidences.animation.modified_date,
            )
            for finding in group_findings
            if finding.evidences.animation is not None
            and not (
                finding.evidences.animation.url.lower().endswith(".png")
                or finding.evidences.animation.url.lower().endswith(".webm")
                or finding.evidences.animation.url.lower().endswith(".jpg")
            )
        ),
        workers=1,
    )
    await collect(
        tuple(
            update_finding_evidences(
                loaders=loaders,
                group_name=finding.group_name,
                finding_id=finding.id,
                url=finding.evidences.exploitation.url,
                evidence_id="exploitation",
                organization_name=organization.name,
                modified_date=finding.evidences.exploitation.modified_date,
            )
            for finding in group_findings
            if finding.evidences.exploitation is not None
            and not (
                finding.evidences.exploitation.url.lower().endswith(".png")
                or finding.evidences.exploitation.url.lower().endswith(".webm")
                or finding.evidences.exploitation.url.lower().endswith(".jpg")
            )
        ),
        workers=1,
    )

    group_events = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    await collect(
        tuple(
            update_event_evidences(
                loaders=loaders,
                group_name=event.group_name,
                event_id=event.id,
                evidences=event.evidences,
                organization_name=organization.name,
            )
            for event in group_events
            if event.evidences is not None
        ),
        workers=1,
    )

    LOGGER.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "len": len(group_findings),
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    LOGGER.info(
        "All groups",
        extra={"extra": {"groups_len": len(group_names)}},
    )

    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / len(group_names),
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=1,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
