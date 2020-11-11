# Standard library
from typing import cast, Dict, List, Union
import html

# Third party imports
from aioextensions import (
    collect,
    in_thread,
)
from exponent_server_sdk import DeviceNotRegisteredError

# Local imports
from backend import mailer
from backend.dal import (
    notifications as notifications_dal,
)
from backend.domain import (
    user as user_domain
)
from backend.utils import (
    datetime as datetime_utils,
)


async def _get_recipient_first_name_async(email: str) -> str:
    first_name = await user_domain.get_data(email, 'first_name')
    if not first_name:
        first_name = email.split('@')[0]
    else:
        # First name exists in database
        pass
    return str(first_name)


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
        await in_thread(
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
        await in_thread(
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
            notifications_dal.send_push_notification(
                user_email, token, title, message)
        except DeviceNotRegisteredError:
            user_domain.remove_push_token(user_email, token)


async def new_password_protected_report(
    user_email: str,
    project_name: str,
    passphrase: str,
    file_type: str,
    file_link: str = '',
) -> None:
    today = datetime_utils.get_now()
    fname = await _get_recipient_first_name_async(user_email)
    subject = f'{file_type} Report for [{project_name}]'
    await collect((
        send_push_notification(
            user_email,
            f'{file_type} report passphrase',
            passphrase),
        mailer.send_mail_project_report(
            [user_email],
            {
                'filetype': file_type,
                'fname': fname,
                'date': datetime_utils.get_as_str(today, '%Y-%m-%d'),
                'year': datetime_utils.get_as_str(today, '%Y'),
                'time': datetime_utils.get_as_str(today, '%H:%M'),
                'projectname': project_name,
                'subject': subject,
                'filelink': file_link
            }
        )
    ))
