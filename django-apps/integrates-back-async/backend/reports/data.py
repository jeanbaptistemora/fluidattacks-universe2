# Standard library
import os
import tempfile
from typing import (
    Dict,
    List,
)
from uuid import uuid4
from zipfile import ZipFile

# Local libraries
from backend import util
from backend.typing import Finding as FindingType
from backend.dal.helpers.s3 import CLIENT as S3_CLIENT  # type: ignore
from backend.domain import (
    notifications as notifications_domain
)
from backend.reports import technical
from backend.utils.passphrase import get_passphrase
from backend.utils import (
    reports as reports_utils,
)
from __init__ import (
    FI_AWS_S3_BUCKET as EVIDENCES_BUCKET,
)


def generate(
    *,
    findings_ord: List[Dict[str, FindingType]],
    group: str,
    group_description: str,
    requester_email: str,
):
    passphrase = get_passphrase(4)

    with tempfile.NamedTemporaryFile(mode='w+b', suffix=f'_{uuid4()}.zip') as file:
        with ZipFile(file, mode='w') as data_file:
            _append_pdf_report(
                data_file=data_file,
                findings_ord=findings_ord,
                group=group,
                group_description=group_description,
                passphrase=passphrase,
                requester_email=requester_email,
            )
            _append_xls_report(
                data_file=data_file,
                findings_ord=findings_ord,
                passphrase=passphrase,
            )
            _append_evidences(
                data_file=data_file,
                group=group,
            )

        # Reset pointer to begin of file
        file.seek(0)

        signed_url = reports_utils.sign_url(
            reports_utils.upload_report_from_file_descriptor(file)
        )

    notifications_domain.new_password_protected_report(
        file_link=signed_url,
        file_type='Group Data',
        passphrase=passphrase,
        project_name=group,
        user_email=requester_email,
    )


def _append_pdf_report(
    *,
    data_file: ZipFile,
    findings_ord: List[Dict[str, FindingType]],
    group: str,
    group_description: str,
    passphrase: str,
    requester_email: str,
):
    # Generate the PDF report
    report_filename = technical.generate_pdf_file(
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


def _append_xls_report(
    data_file: ZipFile,
    findings_ord: List[Dict[str, FindingType]],
    passphrase: str,
):
    report_filename = technical.generate_xls_file(
        findings_ord=findings_ord,
        passphrase=passphrase,
    )
    with data_file.open('report.xls', mode='w') as file:
        with open(report_filename, 'rb') as report:
            file.write(report.read())


def _append_evidences(
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
