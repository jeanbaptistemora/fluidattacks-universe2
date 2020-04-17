import os
import threading
from typing import Tuple
from datetime import datetime
from django.core.files.base import ContentFile
from backend.mailer import send_mail_project_report
from backend.dal.helpers import s3
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
    report_date = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
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


def upload_report(file_path: str) -> Tuple[bool, str]:
    file_content = open(file_path, 'rb')
    report = ContentFile(file_content.read())
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = str(timestamp) + '_' + '_'.join(file_path.split('/')[-1].split('_')[-2:])
    return s3.upload_memory_file(  # type: ignore
        FI_AWS_S3_REPORTS_BUCKET, report, file_name), file_name
