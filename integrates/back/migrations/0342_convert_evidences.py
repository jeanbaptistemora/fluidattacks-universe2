# pylint: disable=invalid-name
"""
try to convert evidences in S3 from gif to webm
"""
from aioextensions import (
    collect,
    run,
)
import asyncio
from contextlib import (
    suppress,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from findings.domain.evidence import (
    update_evidence,
)
import logging
import logging.config
import magic
from organizations import (
    domain as orgs_domain,
)
import os
from s3 import (
    operations as s3_ops,
)
from settings import (
    LOGGING,
)
from starlette.datastructures import (
    UploadFile,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
DIR_PATH = os.path.dirname(os.path.abspath(__file__))


async def update_finding_evidence(
    *,
    loaders: Dataloaders,
    full_path: str,
    group_name: str,
    finding_id: str,
    evidence_id: str,
    organization_name: str,
) -> None:
    filename = f"{organization_name}-{group_name}-1111111111.webm"
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
        "10",
        os.path.join(os.getcwd(), new_file_path),
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        LOGGER.info(
            "Updating converted evidence",
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
            await update_evidence(
                loaders=loaders,
                finding_id=finding_id,
                evidence_id=evidence_id,
                file_object=uploaded_file,
                validate_name=True,
            )
        return

    LOGGER.error(
        "Error getting data over repository",
        extra={
            "extra": {
                "error": stderr.decode(),
                "group_name": group_name,
                "finding_id": finding_id,
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
) -> None:
    evidences_path: str = f"evidences/{group_name.lower()}/{finding_id}/{url}"
    evidences = list(await s3_ops.list_files(evidences_path))
    if evidences:
        for evidence in evidences:
            with suppress(OSError):
                os.makedirs(
                    os.path.join(os.getcwd(), evidences_path.rsplit("/", 1)[0])
                )
            await s3_ops.download_file(
                evidence,
                evidences_path,
            )
            mime_type = magic.from_file(evidences_path, mime=True)
            if mime_type == "image/gif":
                await update_finding_evidence(
                    loaders=loaders,
                    full_path=evidences_path,
                    group_name=group_name,
                    finding_id=finding_id,
                    evidence_id=evidence_id,
                    organization_name=organization_name,
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
    group_findings: tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)

    await collect(
        tuple(
            update_finding_evidences(
                loaders=loaders,
                group_name=finding.group_name,
                finding_id=finding.id,
                url=finding.evidences.animation.url,
                evidence_id="animation",
                organization_name=organization.name,
            )
            for finding in group_findings
            if finding.evidences.animation is not None
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
            )
            for finding in group_findings
            if finding.evidences.exploitation is not None
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
