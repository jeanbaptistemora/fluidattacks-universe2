# Standard library
import logging
import os
from typing import (
    cast,
    Dict,
    List,
    Any,
)

# Third party libraries
from tempfile import TemporaryDirectory
from botocore.exceptions import ClientError
from PIL import Image

# Local libraries
from backend.dal import (
    finding as finding_dal,
)
from backend.domain import (
    notifications as notifications_domain
)
from backend.exceptions import ErrorUploadingFileS3
from backend.reports.it_report import ITReport
from backend.reports.pdf import CreatorPDF
from backend.reports.secure_pdf import SecurePDF
from backend.typing import Finding as FindingType
from backend.utils import reports as reports_utils
from backend.utils.passphrase import get_passphrase
from fluidintegrates.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
STARDIR = os.environ['STARTDIR']

LOGGER = logging.getLogger(__name__)


def convert_evidences_to_png(
    findings: List[Dict[str, FindingType]],
    tempdir: str
) -> None:
    """
    Standardize all evidences to png, converting evidences
    like .gif, .jpg and evidences without extension.
    """
    for finding in findings:
        for evidence in cast(List[Any], finding.get('evidence_set', [])):
            img_id = evidence['id'].split('/')[-1]
            new_name = img_id.split('.')[0]
            evidence['id'] = new_name
            evidence['name'] = f'image::{tempdir}/{new_name}[align="center"]'
            img = Image.open(f'{tempdir}/{img_id}')
            img.save(f'{tempdir}/{new_name}', 'png', optimize=True)
            img.close()


async def generate_pdf_file(
    *,
    description: str,
    findings_ord: List[Dict[str, FindingType]],
    group_name: str,
    lang: str,
    passphrase: str,
    user_email: str,
) -> str:
    secure_pdf = SecurePDF(passphrase)
    report_filename = ''
    with TemporaryDirectory() as tempdir:
        pdf_maker = CreatorPDF(lang, 'tech', tempdir)
        await download_evidences_for_pdf(findings_ord, tempdir)
        convert_evidences_to_png(findings_ord, tempdir)
        pdf_maker.tech(findings_ord, group_name, description, user_email)
    report_filename = await secure_pdf.create_full(
        user_email, pdf_maker.out_name, group_name
    )

    return report_filename


async def generate_pdf(
    *,
    description: str,
    findings_ord: List[Dict[str, FindingType]],
    group_name: str,
    lang: str,
    user_email: str
) -> None:
    passphrase = get_passphrase(4)

    report_filename = await generate_pdf_file(
        description=description,
        findings_ord=findings_ord,
        group_name=group_name,
        lang=lang,
        passphrase=passphrase,
        user_email=user_email,
    )

    try:
        uploaded_file_name = await reports_utils.upload_report(
            report_filename
        )
    except ErrorUploadingFileS3 as ex:
        LOGGER.error(
            ex,
            extra={
                'extra': {
                    'group_name': group_name,
                    'user_email': user_email,
                }
            }
        )
    else:
        await notifications_domain.new_password_protected_report(
            user_email,
            group_name,
            passphrase,
            'Executive',
            await reports_utils.sign_url(uploaded_file_name),
        )


async def generate_xls_file(
    findings_ord: List[Dict[str, FindingType]],
    passphrase: str,
) -> str:
    it_report = ITReport(data=findings_ord)
    await it_report.create()
    filepath = it_report.result_filename

    cmd = (
        f'cat {filepath} | secure-spreadsheet '
        f'--password "{passphrase}" '
        '--input-format xlsx '
        f'> {filepath}-pwd'
    )

    os.system(cmd)
    os.unlink(filepath)
    os.rename(f'{filepath}-pwd', filepath)

    return filepath


async def generate_xls(
    findings_ord: List[Dict[str, FindingType]],
    group_name: str,
    user_email: str,
) -> None:
    passphrase = get_passphrase(4)

    report_filename = await generate_xls_file(
        findings_ord=findings_ord,
        passphrase=passphrase,
    )

    try:
        uploaded_file_name = await reports_utils.upload_report(
            report_filename
        )
    except ErrorUploadingFileS3 as ex:
        LOGGER.error(
            ex,
            extra={
                'extra': {
                    'group_name': group_name,
                    'user_email': user_email,
                }
            }
        )
    else:
        await notifications_domain.new_password_protected_report(
            user_email,
            group_name,
            passphrase,
            'Technical',
            await reports_utils.sign_url(uploaded_file_name),
        )


async def download_evidences_for_pdf(
    findings: List[Dict[str, FindingType]],
    tempdir: str
) -> None:
    for finding in findings:
        folder_name = f'{finding["projectName"]}/{finding["findingId"]}'
        evidences = cast(Dict[str, Dict[str, str]], finding['evidence'])
        evidence_set: List[Dict[str, str]] = [
            {
                'id': f'{folder_name}/{evidences[ev_item]["url"]}',
                'explanation': evidences[ev_item]['description'].capitalize()
            }
            for ev_item in evidences
            if evidences[ev_item]['url']
        ]

        if evidence_set:
            finding['evidence_set'] = evidence_set
            for evidence in evidence_set:
                evidence_id_2 = str(evidence['id']).split('/')[2]
                try:
                    await finding_dal.download_evidence(
                        evidence['id'],
                        f'{tempdir}/{evidence_id_2}',
                    )
                except ClientError as ex:
                    LOGGER.exception(
                        ex,
                        extra={
                            'extra': {
                                'evidence_id': evidence["id"],
                                'project_name': finding["projectName"]
                            }
                        })
                evidence['name'] = (
                    f'image::../images/{evidence_id_2}'
                    '[align="center"]'
                )
