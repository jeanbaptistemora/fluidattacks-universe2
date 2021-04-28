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
    Event as EventType,
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
            EventType,
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

    elif entity_name == 'event':
        event = cast(EventType, entity)
        event_id = str(event.get('id', ''))
        project_name = str(event.get('project_name', ''))
        org_id = await orgs_domain.get_id_for_group(project_name)
        org_name = await orgs_domain.get_name_by_id(org_id)
        recipients = await group_access_domain.get_users_to_notify(
            project_name, True
        )
        email_context['finding_id'] = event_id
        email_context['finding_name'] = f'Event #{event_id}'
        comment_url = (
            f'{BASE_URL}/orgs/{org_name}/groups/{project_name}'
            f'/events/{event_id}/comments'
        )

    elif entity_name == 'project':
        project_name = str(entity)
        org_id = await orgs_domain.get_id_for_group(project_name)
        org_name = await orgs_domain.get_name_by_id(org_id)
        recipients = await get_email_recipients(project_name, True)
        comment_url = f'{BASE_URL}/orgs/{org_name}/groups/' \
                      f'{project_name}/consulting'

    email_context['comment_url'] = comment_url
    email_context['project'] = project_name

    recipients_customers = [
        recipient
        for recipient in recipients
        if await authz.get_group_level_role(
            recipient, project_name) in ['customer', 'customeradmin']
    ]
    recipients_not_customers = [
        recipient
        for recipient in recipients
        if await authz.get_group_level_role(
            recipient, project_name) not in ['customer', 'customeradmin']
    ]

    email_context_customers = email_context.copy()
    if await authz.get_group_level_role(
            user_mail, project_name) not in ['customer', 'customeradmin']:
        email_context_customers['user_email'] = f'Hacker at FluidIntegrates'
    schedule(
        send_mail_comment(
            [recipients_not_customers, recipients_customers],
            [email_context, email_context_customers]
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


async def send_mail_new_draft(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'New draft submitted in [{context["project"]}] - ' +
        f'[Finding#{context["finding_id"]}]',
        'new_draft'
    )


async def send_mail_analytics(
        *email_to: str,
        **context: str) -> None:
    context = cast(MailContentType, context)
    context["live_report_url"] = (
        f'{BASE_URL}/{context["report_entity_percent"]}s/' +
        f'{context["report_subject_percent"]}')
    await _send_mails_async_new(
        list(email_to),
        context,
        GENERAL_TAG,
        f'Analytics for [{context["report_subject_title"]}] ' +
        f'({context["frequency_title"]}: {context["date"]})',
        'charts_report'
    )


async def send_mail_new_user(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'New access request by {context["mail_user"]} for FLUIDIntegrates',
        'new_user'
    )


async def send_mail_delete_finding(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Finding #{context["finding_id"]} in [{context["project"]}] ' +
        f'was removed',
        'delete_finding'
    )


async def send_mail_remediate_finding(
        email_to: List[str],
        context: MailContentType) -> None:
    context[
        "solution_description"
    ] = f'"{context["solution_description"]}"'.splitlines()
    await _send_mails_async_new(
        email_to,
        context,
        VERIFY_TAG,
        f'New remediation in [{context["project"]}] - ' +
        f'[Finding#{context["finding_id"]}]',
        'remediate_finding'
    )


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


async def send_mail_project_report(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'{context["filetype"]} report for [{context["projectname"]}]',
        'project_report'
    )


async def send_mail_verified_finding(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        VERIFY_TAG,
        f'Finding verified in [{context["project"]}] - ' +
        f'[Finding#{context["finding_id"]}]',
        'verified_finding'
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


async def send_mail_new_remediated(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Findings to verify ({context["total"]}) ' +
        f'in [{context["project"]}]',
        'new_remediated'
    )


async def send_mail_reject_draft(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Draft unsubmitted in [{context["project"]}] -' +
        f' #{context["finding_id"]}',
        'unsubmitted_draft'
    )


async def send_mail_new_releases(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Findings to release ({context["total_unreleased"]})' +
        f'({context["total_unsubmitted"]})',
        'new_releases'
    )


async def send_mail_access_granted(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Access Granted to group {context["project"]} ' +
        f'in Integrates by Fluid Attacks',
        'access_granted'
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


async def send_mail_unsolved_events(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Unsolved events in [{context["project"]}]',
        'unsolved_events'
    )


async def send_mail_accepted_finding(
        email_to: List[str],
        context: MailContentType) -> None:
    context["finding_url"] = (
        f'{BASE_URL}/orgs/{context["organization"]}/groups/' +
        f'{context["project"]}/vulns/{context["finding_id"]}')
    context["justification"] = f'"{context["justification"]}"'.splitlines()
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'A finding treatment has changed to {context["treatment"]} ' +
        f'in [{context["project"]}]',
        'accepted_finding'
    )


async def send_mail_new_event(
        email_to: List[List[str]],
        context: List[MailContentType]) -> None:
    await _send_mails_async_new(
        email_to[0],
        context[0],
        GENERAL_TAG,
        f'New event in [{context[0]["project"]}] - ' +
        f'[Event#{context[0]["event_id"]}]',
        'new_event'
    )
    await _send_mails_async_new(
        email_to[1],
        context[1],
        GENERAL_TAG,
        f'New event in [{context[1]["project"]}] - ' +
        f'[Event#{context[1]["event_id"]}]',
        'new_event'
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


async def send_mail_group_deletion(
    email_to: List[str],
    context: MailContentType
) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        GENERAL_TAG,
        f'Group deletion [{context["group_name"]}]',
        'group_deletion'
    )


async def send_mail_daily_digest(
    email_to: List[str],
    context: MailContentType
) -> None:
    await _send_mails_async_new(
        email_to,
        context,
        DIGEST_TAG,
        f'Daily Digest for [{context["project"]}]',
        'daily_digest'
    )


async def log(msg: str, **kwargs: Any) -> None:
    await in_thread(LOGGER_TRANSACTIONAL.info, msg, **kwargs)
