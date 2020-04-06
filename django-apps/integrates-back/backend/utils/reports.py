import os
import threading
from datetime import datetime
from django.core.files.base import ContentFile
from backend.mailer import send_mail_pdf_password
from backend.dal.helpers import s3
from __init__ import FI_AWS_S3_REPORTS_BUCKET


def set_xlsx_password(filepath: str, password: str):
    cmd = 'cat {filepath} | secure-spreadsheet '
    cmd += '--password "{password}" '
    cmd += '--input-format xlsx '
    cmd += '> {filepath}-pwd'
    cmd = cmd.format(filepath=filepath, password=password)

    os.system(cmd)
    os.unlink(filepath)
    os.rename('{filepath}-pwd'.format(filepath=filepath), filepath)


def send_report_password_email(user_email: str, project_name: str, password: str, file_type: str):
    report_date = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
    email_send_thread = threading.Thread(
        name='PDF password email thread',
        target=send_mail_pdf_password,
        args=([user_email], {
            'filetype': file_type,
            'date': report_date.split('_')[0],
            'time': report_date.split('_')[1],
            'projectname': project_name,
            'password': password
        }))

    email_send_thread.start()


def upload_report(file_path: str) -> bool:
    file_content = open(file_path, 'rb')
    my_obj = ContentFile(file_content.read())
    return s3.upload_memory_file(  # type: ignore
        FI_AWS_S3_REPORTS_BUCKET, my_obj, file_path.split('/')[-1])
