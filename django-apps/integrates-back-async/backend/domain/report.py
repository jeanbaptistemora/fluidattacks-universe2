# Standard library
import os
import tempfile
from typing import (
    cast,
    Dict,
    List,
)
from uuid import uuid4
from zipfile import ZipFile

# Local libraries
from backend import util
from backend.typing import Finding as FindingType
from backend.dal.helpers.s3 import CLIENT as S3_CLIENT  # type: ignore
from backend.utils import reports
from backend.dal import (
    finding as finding_dal,
    report as report_dal,
)
from backend.utils.passphrase import get_passphrase
from app.documentator.pdf import CreatorPDF
from app.documentator.secure_pdf import SecurePDF
from app.techdoc.it_report import ITReport
from __init__ import (
    FI_AWS_S3_BUCKET as EVIDENCES_BUCKET,
)


def _generate_pdf_report_file(
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
    findings = pdf_evidences(findings_ord)
    report_filename = ''
    pdf_maker.tech(findings, group_name, description, user_email)
    report_filename = secure_pdf.create_full(user_email,
                                             pdf_maker.out_name,
                                             group_name)

    return report_filename


def generate_pdf_report(
    *,
    description: str,
    findings_ord: List[Dict[str, FindingType]],
    group_name: str,
    lang: str,
    user_email: str,
):
    passphrase = get_passphrase(4)

    report_filename = _generate_pdf_report_file(
        description=description,
        findings_ord=findings_ord,
        group_name=group_name,
        lang=lang,
        passphrase=passphrase,
        user_email=user_email,
    )

    uploaded_file_name = report_dal.upload_report(report_filename)
    signed_url = report_dal.sign_url(uploaded_file_name)
    reports.send_project_report_email(user_email,
                                      group_name,
                                      passphrase, 'PDF',
                                      signed_url)


def _generate_xls_report(
    findings_ord: List[Dict[str, FindingType]],
    passphrase: str,
):
    it_report = ITReport(data=findings_ord)
    filepath = it_report.result_filename
    reports.set_xlsx_passphrase(filepath, passphrase)

    return filepath


def generate_xls_report(
    findings_ord: List[Dict[str, FindingType]],
    group_name: str,
    user_email: str,
):
    passphrase = get_passphrase(4)

    report_filename = _generate_xls_report(
        findings_ord=findings_ord,
        passphrase=passphrase,
    )

    uploaded_file_name = report_dal.upload_report(report_filename)
    signed_url = report_dal.sign_url(uploaded_file_name)
    reports.send_project_report_email(user_email,
                                      group_name,
                                      passphrase, 'XLS', signed_url)


def generate_data_report(
    *,
    findings_ord: List[Dict[str, FindingType]],
    group: str,
    group_description: str,
    requester_email: str,
):
    passphrase = get_passphrase(4)

    with tempfile.NamedTemporaryFile(mode='w+b', suffix=f'_{uuid4()}.zip') as file:
        with ZipFile(file, mode='w') as data_file:
            _generate_data_report__add_pdf(
                data_file=data_file,
                findings_ord=findings_ord,
                group=group,
                group_description=group_description,
                passphrase=passphrase,
                requester_email=requester_email,
            )
            _generate_data_report__add_xls(
                data_file=data_file,
                findings_ord=findings_ord,
                passphrase=passphrase,
            )
            _generate_data_report__add_evidences(
                data_file=data_file,
                group=group,
            )

        # Reset pointer to begin of file
        file.seek(0)

        signed_url = report_dal.sign_url(
            report_dal.upload_report_from_file_descriptor(file)
        )

    reports.send_project_report_email(
        file_link=signed_url,
        file_type='Group Data',
        passphrase=passphrase,
        project_name=group,
        user_email=requester_email,
    )


def _generate_data_report__add_pdf(
    *,
    data_file: ZipFile,
    findings_ord: List[Dict[str, FindingType]],
    group: str,
    group_description: str,
    passphrase: str,
    requester_email: str,
):
    # Generate the PDF report
    report_filename = _generate_pdf_report_file(
        description=group_description,
        findings_ord=findings_ord,
        group_name=group,
        lang='en',
        passphrase=passphrase,
        user_email=requester_email,
    )
    with data_file.open('report.pdf', mode='w') as file:
        with open(report_filename, 'rb') as report:
            file.write(report.read())


def _generate_data_report__add_xls(
    data_file: ZipFile,
    findings_ord: List[Dict[str, FindingType]],
    passphrase: str,
):
    report_filename = _generate_xls_report(
        findings_ord=findings_ord,
        passphrase=passphrase,
    )
    with data_file.open('report.xls', mode='w') as file:
        with open(report_filename, 'rb') as report:
            file.write(report.read())


def _generate_data_report__add_evidences(
    *,
    data_file: ZipFile,
    group: str,
):
    target_folders: Dict[str, str] = {
        '.exp': 'exploits',
        '.gif': 'evidences',
        '.png': 'evidences',
        '.py': 'exploits',
        '.txt': 'compromised-records',
    }

    # Walk everything under the S3 evidences bucket and save relevant info
    for key in util.iterate_s3_keys(
        client=S3_CLIENT,
        bucket=EVIDENCES_BUCKET,
        prefix=group,
    ):
        _, extension = os.path.splitext(key)

        if extension in target_folders:
            target_name = \
                os.path.join(target_folders[extension], os.path.basename(key))

            with data_file.open(target_name, mode='w') as file:
                S3_CLIENT.download_fileobj(EVIDENCES_BUCKET, key, file)


def pdf_evidences(findings: List[Dict[str, FindingType]]) -> List[Dict[str, FindingType]]:
    path: str = (
        '/usr/src/app/app/documentator/images'
        if os.path.exists('/usr/src/app/app/documentator/images')
        else os.path.join(os.getcwd(), 'app', 'documentator', 'images')
    )

    for finding in findings:
        folder_name = str(finding['projectName']) + '/' + str(finding['findingId'])
        evidences = cast(Dict[str, Dict[str, str]], finding['evidence'])
        evidence_set: List[Dict[str, str]] = [{
            'id': '{}/{}'.format(folder_name, str(evidences[ev_item]['url'])),
            'explanation': evidences[ev_item]['description'].capitalize()
        } for ev_item in evidences if evidences[ev_item]['url'].endswith('.png')]

        if evidence_set:
            finding['evidence_set'] = evidence_set
            for evidence in evidence_set:
                finding_dal.download_evidence(
                    evidence['id'],
                    path + '/' +
                    str(evidence['id']).split('/')[2])
                evidence['name'] = 'image::../images/' + \
                    str(evidence['id']).split('/')[2] + '[align="center"]'

    return findings
