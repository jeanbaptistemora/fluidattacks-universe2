from . import (
    technical as technical_report,
)
from context import (
    FI_AWS_S3_BUCKET as EVIDENCES_BUCKET,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from magic import (
    Magic,
)
import os
from s3.operations import (
    download_file,
    list_files,
)
import subprocess  # nosec
import tempfile
from typing import (
    Dict,
    List,
    Tuple,
)
from uuid import (
    uuid4,
)


async def _append_evidences(
    *,
    directory: str,
    group: str,
    findings_ord: Tuple[Finding, ...],
) -> None:
    target_folders: Dict[str, str] = {
        "": "evidences",
        ".csv": "compromised-records",
        ".gif": "evidences",
        ".jpg": "evidences",
        ".png": "evidences",
        ".txt": "compromised-records",
    }

    # Walk everything under the S3 evidences bucket and save relevant info
    for key in await list_files(EVIDENCES_BUCKET, group):
        _, extension = os.path.splitext(key)

        if extension in target_folders:
            # Determine the folder name in which to save the evidence
            finding_folder = ""
            for finding in findings_ord:
                if finding.id in key:
                    finding_folder = finding.title
            target_name = os.path.join(
                directory, target_folders[extension], finding_folder
            )
            os.makedirs(target_name, exist_ok=True)
            target_name = os.path.join(target_name, os.path.basename(key))
            if not os.path.isdir(target_name):
                await download_file(EVIDENCES_BUCKET, key, target_name)
                # Append extension in case it doesn't have one
                if extension == "":
                    mime = Magic(mime=True)
                    mime_type = mime.from_file(target_name)
                    os.rename(
                        target_name,
                        target_name + f".{mime_type.split('/')[1]}",
                    )


async def _append_pdf_report(
    *,
    loaders: Dataloaders,
    directory: str,
    findings_ord: Tuple[Finding, ...],
    group: str,
    group_description: str,
    requester_email: str,
) -> None:
    # Generate the PDF report
    report_filename = await technical_report.generate_pdf_file(
        loaders=loaders,
        description=group_description,
        findings_ord=findings_ord,
        group_name=group,
        lang="en",
        user_email=requester_email,
    )
    with open(os.path.join(directory, "report.pdf"), mode="wb") as file:
        with open(report_filename, "rb") as report:
            file.write(report.read())


async def _append_xls_report(
    *,
    loaders: Dataloaders,
    directory: str,
    findings_ord: Tuple[Finding, ...],
    group_name: str,
) -> None:
    report_filename = await technical_report.generate_xls_file(
        loaders,
        findings_ord=findings_ord,
        group_name=group_name,
        treatments=set(VulnerabilityTreatmentStatus),
    )
    with open(os.path.join(directory, "report.xls"), mode="wb") as file:
        with open(report_filename, "rb") as report:
            file.write(report.read())


def _get_zip_file(*, source_contents: List[str]) -> str:
    # If there are no source contents the current working directory is assumed
    #   by default.
    # We don't want to leave the sandbox at any point
    if not source_contents:
        raise RuntimeError("Nothing to pack into the final file")

    # Impossible to predict with this uuid4
    with tempfile.NamedTemporaryFile() as temp_file:
        target = temp_file.name + f"_{uuid4()}.7z"

    subprocess.run(  # nosec
        [
            "7z",
            "a",
            "-t7z",
            "--",
            target,
            *source_contents,
        ],
        check=True,
    )

    return target


def _get_directory_contents(directory: str) -> List[str]:
    return [
        absolute
        for relative in os.listdir(directory)
        for absolute in [os.path.join(directory, relative)]
        if (
            os.path.isfile(absolute)
            or os.path.isdir(absolute)
            and os.listdir(absolute)
        )
    ]


async def generate(
    *,
    loaders: Dataloaders,
    findings_ord: Tuple[Finding, ...],
    group: str,
    group_description: str,
    requester_email: str,
) -> str:
    with tempfile.TemporaryDirectory() as directory:
        await _append_pdf_report(
            loaders=loaders,
            directory=directory,
            findings_ord=findings_ord,
            group=group,
            group_description=group_description,
            requester_email=requester_email,
        )
        await _append_xls_report(
            loaders=loaders,
            directory=directory,
            findings_ord=findings_ord,
            group_name=group,
        )
        await _append_evidences(
            directory=directory,
            group=group,
            findings_ord=findings_ord,
        )
        return _get_zip_file(
            source_contents=_get_directory_contents(directory),
        )
