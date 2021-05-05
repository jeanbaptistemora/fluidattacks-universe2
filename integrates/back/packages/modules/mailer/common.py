# Standard libraries
import json
import logging
import logging.config
from typing import (
    Any,
    List,
    Union,
)

# Third-party libraries
import mandrill
from aioextensions import (
    collect,
    in_thread,
)
from jinja2 import (
    Environment,
    FileSystemLoader,
)

# Local libraries
import authz
from back.settings import LOGGING
from backend.typing import MailContent as MailContentType
from group_access import domain as group_access_domain
from newutils import datetime as datetime_utils
from users import domain as users_domain
from __init__ import (
    FI_MAIL_REVIEWERS,
    FI_MANDRILL_API_KEY,
    FI_TEST_PROJECTS,
)


logging.config.dictConfig(LOGGING)


# Constants
COMMENTS_TAG: List[str] = ['comments']
DIGEST_TAG = ['digest']
GENERAL_TAG: List[str] = ['general']
LOGGER_TRANSACTIONAL = logging.getLogger('transactional')
TEMPLATES = Environment(
    loader=FileSystemLoader('./back/packages/modules/mailer/email_templates'),
    autoescape=True
)
VERIFY_TAG: List[str] = ['verify']


def get_content(template_name: str, context: MailContentType) -> str:
    template = TEMPLATES.get_template(f'{template_name}.html')
    return template.render(context)


async def get_email_recipients(
    group: str,
    comment_type: Union[str, bool]
) -> List[str]:
    recipients: List[str] = []
    group_users = await group_access_domain.get_users_to_notify(group)
    approvers = FI_MAIL_REVIEWERS.split(',')
    recipients.extend(approvers)

    if comment_type == 'observation':
        analysts = [
            email
            for email in group_users
            if await authz.get_group_level_role(email, group) == 'analyst'
        ]
        recipients.extend(analysts)
    else:
        recipients.extend(group_users)
    return recipients


async def get_recipient_first_name(email: str) -> str:
    first_name = email.split('@')[0]
    user_attr = await users_domain.get_attributes(email, ['first_name'])
    if user_attr and user_attr.get('first_name'):
        first_name = user_attr['first_name']
    return str(first_name)


async def log(msg: str, **kwargs: Any) -> None:
    await in_thread(LOGGER_TRANSACTIONAL.info, msg, **kwargs)


async def send_mail_async_new(
    email_to: str,
    context: MailContentType,
    tags: List[str],
    subject: str,
    template_name: str
) -> None:
    mandrill_client = mandrill.Mandrill(FI_MANDRILL_API_KEY)
    first_name = await get_recipient_first_name(email_to)
    year = datetime_utils.get_as_str(datetime_utils.get_now(), '%Y')
    context['name'] = first_name
    context['year'] = year
    content = get_content(template_name, context)
    message = {
        'from_email': 'noreply@fluidattacks.com',
        'from_name': 'Fluid Attacks',
        'html': content,
        'subject': subject,
        'tags': tags,
        'to': [{
            'email': email_to,
            'name': first_name,
            'type': 'to'
        }],
    }
    mandrill_client.messages.send(message=message)
    await log(
        '[mailer]: mail sent',
        extra={
            'extra': {
                'email_to': email_to,
                'template': template_name,
                'subject': subject,
                'tags': json.dumps(tags),
            }
        }
    )


async def send_mails_async_new(
    email_to: List[str],
    context: MailContentType,
    tags: List[str],
    subject: str,
    template_name: str
) -> None:
    test_group_list = FI_TEST_PROJECTS.split(',')
    await collect([
        send_mail_async_new(
            email,
            context,
            tags,
            subject,
            template_name
        )
        for email in email_to
        if context.get('project', '').lower() not in test_group_list
    ])
