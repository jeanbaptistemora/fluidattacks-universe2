from PIL import (
    Image,
    ImageFile,
)
from botocore.exceptions import (
    ClientError,
)
import cv2
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityVerificationStatus,
)
from decimal import (
    Decimal,
)
from findings import (
    storage as findings_storage,
)
import logging
import logging.config
import magic
from newutils.findings import (
    get_formatted_evidence,
)
from reports.it_report import (
    ITReport,
)
from reports.pdf import (
    CreatorPdf,
)
from reports.secure_pdf import (
    SecurePDF,
)
from settings import (
    LOGGING,
)
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def _get_extension(mime_type: str) -> str:
    try:
        return {
            "image/gif": ".gif",
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "application/x-empty": ".exp",
            "text/x-python": ".exp",
            "application/csv": ".csv",
            "text/csv": ".csv",
            "text/plain": ".txt",
            "video/webm": ".webm",
        }[mime_type]
    except KeyError:
        return ""


def convert_webm_to_png(webm_path: str, img_path: str) -> None:
    cam = cv2.VideoCapture(webm_path)
    current_frame = 0
    while current_frame < 1:
        ret, frame = cam.read()
        if ret:
            cv2.imwrite(f"{img_path}-temp.png", frame)
            img = Image.open(f"{img_path}-temp.png")
            img.save(img_path, "png", optimize=True)
            img.close()
            current_frame += 30
            cam.set(1, current_frame)
        else:
            break
    cam.release()


def convert_evidences_to_png(
    findings: tuple[Finding, ...],
    finding_evidences_set: dict[str, list[dict[str, str]]],
    tempdir: str,
) -> None:
    """
    Standardize all evidences to png, converting evidences
    like .gif, .jpg and evidences without extension.
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    for finding in findings:
        for evidence in finding_evidences_set[finding.id]:
            try:
                img_id = evidence["id"].split("/")[-1]
                new_name = img_id.split(".")[0]
                evidence["id"] = new_name
                evidence["name"] = f"image::{tempdir}/{new_name}[align=center]"
                old_img_path = f"{tempdir}/{img_id}"
                new_img_path = f"{tempdir}/{new_name}"
                mime_type = magic.from_file(old_img_path, mime=True)
                if _get_extension(mime_type) == ".webm":
                    convert_webm_to_png(old_img_path, new_img_path)
                else:
                    img = Image.open(old_img_path)
                    img.save(new_img_path, "png", optimize=True)
                    img.close()
            except OSError as exc:
                LOGGER.exception(
                    exc,
                    extra=dict(
                        extra=dict(
                            evidence_id=evidence["id"],
                            finding_id=finding.id,
                            group_name=finding.group_name,
                        )
                    ),
                )


async def download_evidences_for_pdf(
    findings: tuple[Finding, ...], tempdir: str
) -> dict[str, list[dict[str, str]]]:
    finding_evidences_set = {}
    for finding in findings:
        folder_name = f"{finding.group_name}/{finding.id}"
        evidences = get_formatted_evidence(finding)
        evidences_s3: set[str] = set(
            await findings_storage.search_evidence(folder_name)
        )
        evidence_set = [
            {
                "id": f'{folder_name}/{value["url"]}',
                "explanation": str(value["description"]).capitalize(),
            }
            for _, value in evidences.items()
            if (
                value["url"]
                and f'evidences/{folder_name}/{value["url"]}' in evidences_s3
            )
        ]
        finding_evidences_set[finding.id] = evidence_set

        if evidence_set:
            for evidence in evidence_set:
                evidence_id_2 = str(evidence["id"]).split("/")[2]
                try:
                    await findings_storage.download_evidence(
                        evidence["id"],
                        f"{tempdir}/{evidence_id_2}",
                    )
                except ClientError as ex:
                    LOGGER.exception(
                        ex,
                        extra={
                            "extra": {
                                "evidence_id": evidence["id"],
                                "group_name": finding.group_name,
                            }
                        },
                    )
                evidence["name"] = (
                    f"image::../images/{evidence_id_2}" '[align="center"]'
                )
    return finding_evidences_set


async def generate_pdf_file(
    *,
    loaders: Dataloaders,
    description: str,
    findings_ord: tuple[Finding, ...],
    group_name: str,
    lang: str,
    user_email: str,
) -> str:
    secure_pdf = SecurePDF()
    report_filename = ""
    with TemporaryDirectory() as tempdir:
        pdf_maker = CreatorPdf(lang, "tech", tempdir, group_name, user_email)
        finding_evidences_set = await download_evidences_for_pdf(
            findings_ord, tempdir
        )
        convert_evidences_to_png(findings_ord, finding_evidences_set, tempdir)
        await pdf_maker.tech(
            findings_ord,
            finding_evidences_set,
            description,
            loaders,
        )
    report_filename = await secure_pdf.create_full(
        loaders, user_email, pdf_maker.out_name, group_name
    )
    return report_filename


async def generate_xls_file(  # NOSONAR # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    findings_ord: tuple[Finding, ...],
    group_name: str,
    states: set[VulnerabilityStateStatus],
    treatments: set[VulnerabilityTreatmentStatus],
    verifications: set[VulnerabilityVerificationStatus],
    closing_date: Optional[datetime],
    finding_title: str,
    age: Optional[int],
    min_severity: Optional[Decimal],
    max_severity: Optional[Decimal],
    last_report: Optional[int],
    min_release_date: Optional[datetime],
    max_release_date: Optional[datetime],
    location: str,
) -> str:
    it_report = ITReport(
        data=findings_ord,
        group_name=group_name,
        treatments=treatments,
        states=states,
        loaders=loaders,
        verifications=verifications,
        closing_date=closing_date,
        finding_title=finding_title,
        age=age,
        min_severity=min_severity,
        max_severity=max_severity,
        last_report=last_report,
        min_release_date=min_release_date,
        max_release_date=max_release_date,
        location=location,
    )
    await it_report.generate_file()
    filepath = it_report.result_filename

    return filepath
