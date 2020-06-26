# Standard library
import os
from typing import (
    cast,
    Dict,
    List,
)

# Local libraries
from backend.dal import (
    finding as finding_dal,
)
from backend.domain import (
    notifications as notifications_domain
)
from backend.typing import Finding as FindingType
from backend.utils import reports as reports_utils
from backend.utils.passphrase import get_passphrase
from app.documentator.pdf import CreatorPDF
from app.documentator.secure_pdf import SecurePDF
from app.techdoc.it_report import ITReport


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
    path: str = (
        '/usr/src/app/app/documentator/images'
        if os.path.exists('/usr/src/app/app/documentator/images')
        else os.path.join(os.getcwd(), 'app', 'documentator', 'images')
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
                finding_dal.download_evidence(
                    evidence['id'],
                    f'{path}/{evidence_id_2}'
                )
                evidence['name'] = (
                    f'image::../images/{evidence_id_2}'
                    '[align="center"]'
                )
