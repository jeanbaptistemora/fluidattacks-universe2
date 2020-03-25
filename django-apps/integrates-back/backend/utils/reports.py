import os
import threading
from datetime import datetime
from backend.mailer import send_mail_pdf_password


def set_xlsx_password(filepath: str, password: str):
    cmd = 'cat {filepath} | secure-spreadsheet '
    cmd += '--password {password} '
    cmd += '--input-format xlsx '
    cmd += '> {filepath}-pwd'
    cmd = cmd.format(filepath=filepath, password=password)

    os.system(cmd)
    os.unlink(filepath)
    os.rename('{filepath}-pwd'.format(filepath=filepath), filepath)


def send_pdf_password_email(user_info, project_name, password):
    user_name = user_info[1]
    user_email = user_info[0]
    report_date = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
    email_send_thread = threading.Thread(
        name='PDF password email thread',
        target=send_mail_pdf_password,
        args=([user_email], {
            'date': report_date.split('_')[0],
            'time': report_date.split('_')[1],
            'project': project_name,
            'username': user_name,
            'password': password
        }))

    email_send_thread.start()
