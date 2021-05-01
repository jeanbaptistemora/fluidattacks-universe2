# Standard library
import json
import logging
from typing import (
    cast,
    Any,
    Dict,
    List,
    Union,
)

# Third party libraries
from aioextensions import (
    collect,
    in_thread,
    schedule,
)
import mandrill
from jinja2 import (
    Environment,
    FileSystemLoader,
)

# Local libraries
from back import settings
from backend import authz
from backend.typing import (
    Comment as CommentType,
    Finding as FindingType,
    MailContent as MailContentType,
    Project as ProjectType
)
from group_access import domain as group_access_domain
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
)
from organizations import domain as orgs_domain
from users import domain as users_domain
from __init__ import (
    BASE_URL,
    FI_MAIL_REVIEWERS,
    FI_MANDRILL_API_KEY,
    FI_TEST_PROJECTS,
    SQS_QUEUE_URL,
)

logging.config.dictConfig(settings.LOGGING)

# Constants
API_KEY = FI_MANDRILL_API_KEY
COMMENTS_TAG = ['comments']
DIGEST_TAG = ['digest']
GENERAL_TAG = ['general']
LOGGER = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger('transactional')
VERIFY_TAG = ['verify']
QUEUE_URL = SQS_QUEUE_URL
TEMPLATES = Environment(
    loader=FileSystemLoader(
        './back/packages/integrates-back/'
        'backend/email_templates'
    ),
    autoescape=True
)


def _get_content(template_name: str, context: MailContentType) -> str:
    template = TEMPLATES.get_template(f'{template_name}.html')
    return template.render(context)


async def _send_mail_async_new(
    email_to: str,
    context: MailContentType,
    tags: List[str],
    subject: str,
    template_name: str
) -> None:
    mandrill_client = mandrill.Mandrill(API_KEY)
    first_name = await get_recipient_first_name(email_to)
    year = datetime_utils.get_as_str(
        datetime_utils.get_now(), '%Y'
    )
    context['name'] = first_name
    context['year'] = year
    content = _get_content(template_name, context)
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


async def _send_mails_async_new(
    email_to: List[str],
    context: MailContentType,
    tags: List[str],
    subject: str,
    template_name: str
) -> None:
    test_proj_list = FI_TEST_PROJECTS.split(',')
    await collect([
        _send_mail_async_new(
            email,
            context,
            tags,
            subject,
            template_name
        )
        for email in email_to
        if context.get('project', '').lower() not in test_proj_list
    ])


async def get_recipient_first_name(email: str) -> str:
    first_name = email.split('@')[0]
    user_attr = await users_domain.get_attributes(email, ['first_name'])
    if user_attr and user_attr.get('first_name'):
        first_name = user_attr['first_name']
    return str(first_name)


async def send_comment_mail(  # pylint: disable=too-many-locals
        comment_data: CommentType,
        entity_name: str,
        user_mail: str,
        comment_type: str = '',
        entity: Union[
            str,
            Dict[str, FindingType],
            ProjectType
        ] = '') -> None:
    email_context: MailContentType = {
        'user_email': user_mail,
        'comment': comment_data['content'],
        'comment_type': comment_type,
        'parent': str(comment_data['parent']),
    }
    if entity_name == 'finding':
        finding: Dict[str, FindingType] = cast(Dict[str, FindingType], entity)
        project_name = str(finding.get('project_name', ''))
        recipients = await get_email_recipients(project_name, comment_type)
        org_id = await orgs_domain.get_id_for_group(project_name)
        org_name = await orgs_domain.get_name_by_id(org_id)

        email_context['finding_id'] = str(finding.get('id', ''))
        email_context['finding_name'] = str(finding.get('finding', ''))
        is_finding_released = findings_utils.is_released(finding)
        comment_url = (
            BASE_URL +
            f'/orgs/{org_name}/groups/{project_name}/' +
            ('vulns' if is_finding_released else 'drafts') +
            '/' + str(finding.get('id', '')) + '/' +
            ('consulting' if comment_type == 'comment' else 'observations')
        )

    email_context['comment_url'] = comment_url
    email_context['project'] = project_name

    # Mask Fluid Attacks' staff
    recipients_not_masked = [
        recipient
        for recipient in recipients
        if ('@fluidattacks.com' in recipient)
        or ('@fluidattacks.com' not in user_mail)
    ]
    recipients_masked = [
        recipient
        for recipient in recipients
        if not (('@fluidattacks.com' in recipient)
                or ('@fluidattacks.com' not in user_mail))
    ]
    email_context_masked = email_context.copy()
    if '@fluidattacks.com' in user_mail:
        email_context_masked['user_email'] = f'Hacker at Fluid Attacks'

    schedule(
        send_mail_comment(
            [recipients_not_masked, recipients_masked],
            [email_context, email_context_masked]
        )
    )


async def get_email_recipients(
        group: str, comment_type: Union[str, bool]) -> List[str]:
    project_users = await group_access_domain.get_users_to_notify(group)
    recipients: List[str] = []

    approvers = FI_MAIL_REVIEWERS.split(',')
    recipients += approvers

    if comment_type == 'observation':
        analysts = [
            email
            for email in project_users
            if await authz.get_group_level_role(
                email, group
            ) == 'analyst'
        ]
        recipients += analysts
    else:
        recipients += project_users

    return recipients


async def send_mail_comment(
        email_to: List[List[str]],
        context: List[MailContentType]) -> None:
    context[0]["comment"] = f'"{context[0]["comment"]}"'.splitlines()
    await _send_mails_async_new(
        email_to[0],
        context[0],
        COMMENTS_TAG,
        f'New ' +
        ('observation' if context[0]["comment_type"] == 'observation'
         else 'comment') +
        f' in [{context[0]["project"]}]',
        'new_comment'
    )
    context[1]["comment"] = f'"{context[1]["comment"]}"'.splitlines()
    await _send_mails_async_new(
        email_to[1],
        context[1],
        COMMENTS_TAG,
        f'New ' +
        ('observation' if context[1]["comment_type"] == 'observation'
         else 'comment') +
        f' in [{context[1]["project"]}]',
        'new_comment'
    )


async def send_mail_updated_treatment(
        email_to: List[str],
        context: MailContentType) -> None:
    context["vulnerabilities"] = f'"{context["vulnerabilities"]}"'.splitlines()
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'A vulnerability treatment has changed to {context["treatment"]} ' +
        f'in [{context["project"]}]',
        'updated_treatment'
    )


async def send_mail_resources(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Changes in resources for [{context["project"]}]',
        'resources_changes'
    )


async def send_mail_org_deletion(
    email_to: List[str],
    context: MailContentType
) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Organization deletion [{context["org_name"]}]',
        'organization_deletion'
    )


async def log(msg: str, **kwargs: Any) -> None:
    await in_thread(LOGGER_TRANSACTIONAL.info, msg, **kwargs)
