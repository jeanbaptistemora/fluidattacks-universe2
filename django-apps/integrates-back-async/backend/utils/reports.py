import os
import threading
from typing import Tuple
from datetime import datetime
from django.core.files.base import ContentFile
from backend.dal.helpers import s3
from backend.mailer import send_mail_project_report
from __init__ import FI_AWS_S3_REPORTS_BUCKET


def set_xlsx_passphrase(filepath: str, passphrase: str):
    cmd = 'cat {filepath} | secure-spreadsheet '
    cmd += '--password "{passphrase}" '
    cmd += '--input-format xlsx '
    cmd += '> {filepath}-pwd'
    cmd = cmd.format(filepath=filepath, passphrase=passphrase)

    os.system(cmd)
    os.unlink(filepath)
    os.rename('{filepath}-pwd'.format(filepath=filepath), filepath)


def send_project_report_email(
        user_email: str, project_name: str, passphrase: str, file_type: str, file_link: str = ''):
    report_date = datetime.today().strftime('%Y-%m-%d_%H:%M')
    email_send_thread = threading.Thread(
        name='Report passphrase email thread',
        target=send_mail_project_report,
        args=([user_email], {
            'filetype': file_type,
            'date': report_date.split('_')[0],
            'time': report_date.split('_')[1],
            'projectname': project_name,
            'passphrase': passphrase,
            'filelink': file_link
        }))

    email_send_thread.start()


def upload_report(path: str) -> Tuple[bool, str]:
    with open(path, 'rb') as file:
        report = ContentFile(file.read(), name=path)

        return upload_report_from_file_descriptor(report)


def upload_report_from_file_descriptor(report) -> Tuple[bool, str]:
    file_path = report.name
    file_name = file_path.split('_')[-1]

    # Mypy false positive
    result = \
        s3.upload_memory_file(FI_AWS_S3_REPORTS_BUCKET, report, file_name)  # type: ignore

    return bool(result), file_name
