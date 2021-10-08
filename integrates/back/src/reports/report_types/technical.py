from PIL import (
    Image,
    ImageFile,
)
from botocore.exceptions import (
    ClientError,
)
from custom_types import (
    Finding as FindingType,
)
from db_model.findings.types import (
    Finding,
)
from findings import (
    dal as findings_dal,
)
import logging
import logging.config
from newutils.findings import (
    get_formatted_evidence,
)
from newutils.utils import (
    get_key_or_fallback,
)
import os
from reports.it_report import (
    ITReport,
    ITReportNew,
)
from reports.pdf import (
    CreatorPDF,
    CreatorPdfNew,
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
    Any,
    cast,
    Dict,
    List,
    Set,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def convert_evidences_to_png(
    findings: List[Dict[str, FindingType]], tempdir: str, group_name: str
) -> None:
    """
    Standardize all evidences to png, converting evidences
    like .gif, .jpg and evidences without extension.
    """
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    for finding in findings:
        for evidence in cast(List[Any], finding.get("evidence_set", [])):
            try:
                img_id = evidence["id"].split("/")[-1]
                new_name = img_id.split(".")[0]
                evidence["id"] = new_name
                evidence["name"] = f"image::{tempdir}/{new_name}[align=center]"
                img = Image.open(f"{tempdir}/{img_id}")
                img.save(f"{tempdir}/{new_name}", "png", optimize=True)
                img.close()
            except OSError as exc:
                LOGGER.exception(
                    exc,
                    extra=dict(
                        extra=dict(
                            evidence_id=evidence["id"],
                            finding_id=finding["findingId"],
                            group_name=group_name,
                        )
                    ),
                )


def convert_evidences_to_png_new(
    findings: Tuple[Finding, ...],
    finding_evidences_set: Dict[str, List[Dict[str, str]]],
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
                img = Image.open(f"{tempdir}/{img_id}")
                img.save(f"{tempdir}/{new_name}", "png", optimize=True)
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
    findings: List[Dict[str, FindingType]], tempdir: str
) -> None:
    for finding in findings:
        folder_name = f'{finding["projectName"]}/{finding["findingId"]}'
        evidences = cast(Dict[str, Dict[str, str]], finding["evidence"])
        evidences_s3: Set[str] = set(
            await findings_dal.search_evidence(folder_name)
        )
        evidence_set: List[Dict[str, str]] = [
            {
                "id": f'{folder_name}/{evidences[ev_item]["url"]}',
                "explanation": evidences[ev_item]["description"].capitalize(),
            }
            for ev_item in evidences
            if (
                evidences[ev_item]["url"]
                and f'{folder_name}/{evidences[ev_item]["url"]}'
                in evidences_s3
            )
        ]

        if evidence_set:
            finding["evidence_set"] = evidence_set
            for evidence in evidence_set:
                evidence_id_2 = str(evidence["id"]).split("/")[2]
                try:
                    await findings_dal.download_evidence(
                        evidence["id"],
                        f"{tempdir}/{evidence_id_2}",
                    )
                except ClientError as ex:
                    LOGGER.exception(
                        ex,
                        extra={
                            "extra": {
                                "evidence_id": evidence["id"],
                                "group_name": get_key_or_fallback(finding),
                            }
                        },
                    )
                evidence["name"] = (
                    f"image::../images/{evidence_id_2}" '[align="center"]'
                )


async def download_evidences_for_pdf_new(
    findings: Tuple[Finding, ...], tempdir: str
) -> Dict[str, List[Dict[str, str]]]:
    finding_evidences_set = {}
    for finding in findings:
        folder_name = f"{finding.group_name}/{finding.id}"
        evidences = get_formatted_evidence(finding)
        evidences_s3: Set[str] = set(
            await findings_dal.search_evidence(folder_name)
        )
        evidence_set = [
            {
                "id": f'{folder_name}/{value["url"]}',
                "explanation": value["description"].capitalize(),
            }
            for _, value in evidences.items()
            if (
                value["url"]
                and f'{folder_name}/{value["url"]}' in evidences_s3
            )
        ]
        finding_evidences_set[finding.id] = evidence_set

        if evidence_set:
            for evidence in evidence_set:
                evidence_id_2 = str(evidence["id"]).split("/")[2]
                try:
                    await findings_dal.download_evidence(
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
    loaders: Any,
    description: str,
    findings_ord: List[Dict[str, FindingType]],
    group_name: str,
    lang: str,
    passphrase: str,
    user_email: str,
) -> str:
    secure_pdf = SecurePDF(passphrase)
    report_filename = ""
    with TemporaryDirectory() as tempdir:
        pdf_maker = CreatorPDF(lang, "tech", tempdir)
        await download_evidences_for_pdf(findings_ord, tempdir)
        convert_evidences_to_png(findings_ord, tempdir, group_name)
        await pdf_maker.tech(
            findings_ord, group_name, description, user_email, loaders
        )
    report_filename = await secure_pdf.create_full(
        user_email, pdf_maker.out_name, group_name
    )
    return report_filename


async def generate_pdf_file_new(
    *,
    loaders: Any,
    description: str,
    findings_ord: Tuple[Finding, ...],
    group_name: str,
    lang: str,
    passphrase: str,
    user_email: str,
) -> str:
    secure_pdf = SecurePDF(passphrase)
    report_filename = ""
    with TemporaryDirectory() as tempdir:
        pdf_maker = CreatorPdfNew(lang, "tech", tempdir)
        finding_evidences_set = await download_evidences_for_pdf_new(
            findings_ord, tempdir
        )
        convert_evidences_to_png_new(
            findings_ord, finding_evidences_set, tempdir
        )
        await pdf_maker.tech(
            findings_ord,
            finding_evidences_set,
            group_name,
            description,
            user_email,
            loaders,
        )
    report_filename = await secure_pdf.create_full(
        user_email, pdf_maker.out_name, group_name
    )
    return report_filename


async def generate_xls_file(
    loaders: Any,
    findings_ord: List[Dict[str, FindingType]],
    group_name: str,
    passphrase: str,
) -> str:
    it_report = ITReport(
        data=findings_ord, group_name=group_name, loaders=loaders
    )
    await it_report.create()
    filepath = it_report.result_filename

    cmd = (
        f"cat {filepath} | secure-spreadsheet "
        f'--password "{passphrase}" '
        "--input-format xlsx "
        f"> {filepath}-pwd"
    )

    os.system(cmd)  # nosec
    os.unlink(filepath)
    os.rename(f"{filepath}-pwd", filepath)
    return filepath


async def generate_xls_file_new(
    loaders: Any,
    findings_ord: Tuple[Finding, ...],
    group_name: str,
    passphrase: str,
) -> str:
    it_report = ITReportNew(
        data=findings_ord, group_name=group_name, loaders=loaders
    )
    await it_report.create()
    filepath = it_report.result_filename

    cmd = (
        f"cat {filepath} | secure-spreadsheet "
        f'--password "{passphrase}" '
        "--input-format xlsx "
        f"> {filepath}-pwd"
    )

    os.system(cmd)  # nosec
    os.unlink(filepath)
    os.rename(f"{filepath}-pwd", filepath)
    return filepath
