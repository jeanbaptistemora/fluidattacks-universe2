# Standard library
import os
from typing import (
    cast,
    Dict,
    List,
)

# Third party libraries
from asgiref.sync import async_to_sync
from botocore.exceptions import ClientError
import rollbar

# Local libraries
from backend.dal import (
    finding as finding_dal,
)
from backend.domain import (
    notifications as notifications_domain
)
from backend.reports.it_report import ITReport
from backend.reports.pdf import CreatorPDF
from backend.reports.secure_pdf import SecurePDF
from backend.typing import Finding as FindingType
from backend.utils import reports as reports_utils
from backend.utils.passphrase import get_passphrase


def generate_pdf_file(
    *,
    description: str,
    findings_ord: List[Dict[str, FindingType]],
    group_name: str,
    lang: str,
    passphrase: str,
    user_email: str,
) -> str:
    pdf_maker = CreatorPDF(lang, 'tech')
    secure_pdf = SecurePDF(passphrase)
    download_evidences_for_pdf(findings_ord)
    report_filename = ''
    pdf_maker.tech(findings_ord, group_name, description, user_email)
    report_filename = secure_pdf.create_full(
        user_email, pdf_maker.out_name, group_name
    )

    return report_filename


def generate_pdf(
        *,
        description: str,
        findings_ord: List[Dict[str, FindingType]],
        group_name: str,
        lang: str,
        user_email: str):
    passphrase = get_passphrase(4)

    report_filename = generate_pdf_file(
        description=description,
        findings_ord=findings_ord,
        group_name=group_name,
        lang=lang,
        passphrase=passphrase,
        user_email=user_email,
    )

    uploaded_file_name = reports_utils.upload_report(report_filename)

    notifications_domain.new_password_protected_report(
        user_email,
        group_name,
        passphrase, 'PDF',
        reports_utils.sign_url(uploaded_file_name),
    )


def generate_xls_file(
    findings_ord: List[Dict[str, FindingType]],
    passphrase: str,
):
    it_report = ITReport(data=findings_ord)
    filepath = it_report.result_filename

    cmd = (
        f'cat {filepath} | secure-spreadsheet '
        f'--password "{passphrase}" '
        '--input-format xlsx '
        f'> {filepath}-pwd'
    )

    os.system(cmd)
    os.unlink(filepath)
    os.rename('{filepath}-pwd'.format(filepath=filepath), filepath)

    return filepath


def generate_xls(
    findings_ord: List[Dict[str, FindingType]],
    group_name: str,
    user_email: str,
):
    passphrase = get_passphrase(4)

    report_filename = generate_xls_file(
        findings_ord=findings_ord,
        passphrase=passphrase,
    )

    uploaded_file_name = reports_utils.upload_report(report_filename)

    notifications_domain.new_password_protected_report(
        user_email,
        group_name,
        passphrase,
        'XLS',
        reports_utils.sign_url(uploaded_file_name),
    )


def download_evidences_for_pdf(findings: List[Dict[str, FindingType]]):
    images_path = (
        '/usr/src/app/django-apps/integrates-back-async/backend/reports/images'
    )
    path: str = (
        images_path
        if os.path.exists(images_path)
        else os.path.join(
            os.getcwd(),
            'django-apps',
            'integrates-back-async',
            'backend',
            'reports',
            'images')
    )

    for finding in findings:
        folder_name = (
            str(finding['projectName']) + '/' +
            str(finding['findingId'])
        )
        evidences = cast(Dict[str, Dict[str, str]], finding['evidence'])
        evidence_set: List[Dict[str, str]] = [
            {
                'id': f'{folder_name}/{evidences[ev_item]["url"]}',
                'explanation': evidences[ev_item]['description'].capitalize()
            }
            for ev_item in evidences
            if evidences[ev_item]['url'].endswith('.png')
        ]

        if evidence_set:
            finding['evidence_set'] = evidence_set
            for evidence in evidence_set:
                evidence_id_2 = str(evidence['id']).split('/')[2]
                try:
                    async_to_sync(finding_dal.download_evidence)(
                        evidence['id'],
                        f'{path}/{evidence_id_2}',
                    )
                except ClientError as download_evidence_error:
                    msg = (
                        f'Error: Missing evidences in group'
                        f'{finding["projectName"]}'
                        f'for evidence with id {evidence["id"]}'
                        f'while generating report.\n'
                        f'{download_evidence_error}'
                    )
                    rollbar.report_message(msg, 'error')
                evidence['name'] = (
                    f'image::../images/{evidence_id_2}'
                    '[align="center"]'
                )
