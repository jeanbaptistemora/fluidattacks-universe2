# Standard library
from datetime import datetime
import html
import threading

# Local imports
from backend import mailer
from backend.dal import (
    notifications as notifications_dal,
)
from backend.utils import aio


async def new_group(
    *,
    description: str,
    group_name: str,
    has_drills: bool,
    has_forces: bool,
    requester_email: str,
    subscription: str,
) -> bool:
    translations: dict = {
        'continuous': 'Continuous Hacking',
        'oneshot': 'One-Shot Hacking',
        True: 'Active',
        False: 'Inactive',
    }

    return await aio.ensure_io_bound(
        notifications_dal.create_ticket,
        subject=f'[Integrates] Group created: {group_name}',
        description=f"""
            You are receiving this email because you have created a group
            through Integrates by Fluid Attacks.

            Here are the details of the group:
            - Name: {group_name}
            - Description: {description}
            - Type: {translations.get(subscription, subscription)}
            - Drills: {translations[has_drills]}
            - Forces: {translations[has_forces]}

            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=requester_email,
    )


async def edit_group(
    *,
    comments: str,
    group_name: str,
    had_drills: bool,
    had_forces: bool,
    had_integrates: bool,
    has_drills: bool,
    has_forces: bool,
    has_integrates: bool,
    reason: str,
    requester_email: str,
    subscription: str,
) -> bool:
    translations: dict = {
        'continuous': 'Continuous Hacking',
        'oneshot': 'One-Shot Hacking',
        True: 'Active',
        False: 'Inactive',
    }

    return await aio.ensure_io_bound(
        notifications_dal.create_ticket,
        subject=f'[Integrates] Group edited: {group_name}',
        description=f"""
            You are receiving this email because you have edited a group
            through Integrates by Fluid Attacks.

            Here are the details of the group:
            - Name: {group_name}
            - Type: {translations.get(subscription, subscription)}
            - Integrates:
                from: {translations[had_integrates]}
                to: {translations[has_integrates]}
            - Drills:
                from: {translations[had_drills]}
                to: {translations[has_drills]}
            - Forces:
                from: {translations[had_forces]}
                to: {translations[has_forces]}
            - Comments: {html.escape(comments, quote=True)}
            - Reason: {reason}

            If you require any further information,
            do not hesitate to contact us.
        """,
        requester_email=requester_email,
    )


def new_password_protected_report(
    user_email: str,
    project_name: str,
    passphrase: str,
    file_type: str,
    file_link: str = '',
):
    email_send_thread = threading.Thread(
        name='Report passphrase email thread',
        target=mailer.send_mail_project_report,
        args=([user_email], {
            'filetype': file_type,
            'date': datetime.today().strftime('%Y-%m-%d'),
            'time': datetime.today().strftime('%H:%M'),
            'projectname': project_name,
            'passphrase': passphrase,
            'filelink': file_link
        }))

    email_send_thread.start()
