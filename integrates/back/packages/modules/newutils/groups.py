# Standard libraries
import logging
import logging.config
import secrets
from typing import (
    cast,
    List,
    Set
)

# Third-party libraries
from aioextensions import schedule

# Local libraries
from back.settings import LOGGING
from backend import mailer
from backend.domain import project as group_domain
from backend.typing import (
    Historic as HistoricType,
    MailContent as MailContentType,
    Project as ProjectType,
)
from newutils import datetime as datetime_utils
from newutils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
    validate_fluidattacks_staff_on_group,
    validate_phone_field,
)
from __init__ import BASE_URL


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def has_integrates_services(group: ProjectType) -> bool:
    historic_configuration: HistoricType = (
        group.get('historic_configuration', [{}])
    )
    last_config_info = historic_configuration[-1]
    group_has_integrates_services: bool = (
        last_config_info['has_drills']
        or last_config_info['has_forces']
    )

    return group_has_integrates_services


async def invite_to_group(
    email: str,
    responsibility: str,
    role: str,
    phone_number: str,
    group_name: str,
) -> bool:
    success = False
    if (
        validate_field_length(responsibility, 50) and
        validate_alphanumeric_field(responsibility) and
        validate_phone_field(phone_number) and
        validate_email_address(email) and
        await validate_fluidattacks_staff_on_group(group_name, email, role)
    ):
        expiration_time = datetime_utils.get_as_epoch(
            datetime_utils.get_now_plus_delta(weeks=1)
        )
        url_token = secrets.token_urlsafe(64)
        success = await group_domain.update_access(
            email,
            group_name,
            {
                'expiration_time': expiration_time,
                'has_access': False,
                'invitation': {
                    'is_used': False,
                    'phone_number': phone_number,
                    'responsibility': responsibility,
                    'role': role,
                    'url_token': url_token,
                },

            }
        )
        description = await group_domain.get_description(group_name.lower())
        project_url = f'{BASE_URL}/confirm_access/{url_token}'
        mail_to = [email]
        email_context: MailContentType = {
            'admin': email,
            'project': group_name,
            'project_description': description,
            'project_url': project_url,
        }
        schedule(mailer.send_mail_access_granted(mail_to, email_context))
    return success


async def update_tags(
    project_name: str,
    project_tags: ProjectType,
    tags: List[str]
) -> bool:
    if not project_tags['tag']:
        project_tags = {'tag': set(tags)}
    else:
        cast(Set[str], project_tags.get('tag')).update(tags)
    tags_added = await group_domain.update(project_name, project_tags)
    if tags_added:
        success = True
    else:
        LOGGER.error('Couldn\'t add tags', extra={'extra': locals()})
        success = False

    return success
