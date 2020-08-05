# Standard library
from datetime import datetime
from typing import cast, Dict, List, Union
import html
import threading

# Third party imports
from asgiref.sync import async_to_sync
from exponent_server_sdk import DeviceNotRegisteredError

# Local imports
from backend import mailer
from backend.dal import (
    notifications as notifications_dal,
)
from backend.domain import (
    user as user_domain
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
    translations: Dict[Union[str, bool], str] = {
        'continuous': 'Continuous Hacking',
        'oneshot': 'One-Shot Hacking',
        True: 'Active',
        False: 'Inactive',
    }

    return cast(
        bool,
        await aio.ensure_io_bound(
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
    translations: Dict[Union[str, bool], str] = {
        'continuous': 'Continuous Hacking',
        'oneshot': 'One-Shot Hacking',
        True: 'Active',
        False: 'Inactive',
    }

    return cast(
        bool,
        await aio.ensure_io_bound(
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
    )


@async_to_sync
async def send_push_notification(
    user_email: str,
    title: str,
    message: str
) -> None:
    user_attrs: dict = await user_domain.get_attributes(
        user_email, ['push_tokens'])
    tokens: List[str] = user_attrs.get('push_tokens', [])

    for token in tokens:
        try:
            notifications_dal.send_push_notification(token, title, message)
        except DeviceNotRegisteredError:
            user_domain.remove_push_token(user_email, token)


def new_password_protected_report(
    user_email: str,
    project_name: str,
    passphrase: str,
    file_type: str,
    file_link: str = '',
) -> None:
    send_push_notification(user_email, 'Report passphrase', passphrase)

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
