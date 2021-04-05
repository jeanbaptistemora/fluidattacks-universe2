# Standard library
import os
import json
import logging
from html import escape
from typing import (
    cast,
    Any,
    Dict,
    List,
    Optional,
    Union,
)

# Third party libraries
import aioboto3
from aioextensions import (
    collect,
    in_thread,
    schedule,
)
import botocore
import mandrill
from jinja2 import (
    Environment,
    FileSystemLoader,
)

# Local libraries
from back import settings
from backend import authz
from backend.domain import project as project_domain
from backend.filters import finding as finding_filters
from backend.typing import (
    Event as EventType,
    Finding as FindingType,
    MailContent as MailContentType,
    Project as ProjectType
)
from comments.domain import CommentType
from newutils import datetime as datetime_utils
from organizations import domain as orgs_domain
from users import domain as users_domain
from __init__ import (
    BASE_URL,
    FI_MAIL_REVIEWERS,
    FI_MANDRILL_API_KEY,
    FI_TEST_PROJECTS,
    FI_AWS_DYNAMODB_ACCESS_KEY,
    FI_AWS_DYNAMODB_SECRET_KEY,
    SQS_QUEUE_URL,
)

logging.config.dictConfig(settings.LOGGING)

# Constants
API_KEY = FI_MANDRILL_API_KEY
COMMENTS_TAG = ['comments']
GENERAL_TAG = ['general']
LOGGER = logging.getLogger(__name__)
LOGGER_TRANSACTIONAL = logging.getLogger('transactional')
VERIFY_TAG = ['verify']
VULNERABILITIES_TAG = ['vulnerabilities']
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


def _escape_context(context: Dict[str, Union[str, int]]) -> \
        Dict[str, Union[str, int]]:
    attr_to_esc = [
        'solution_description',
        'description',
        'resource_list',
        'justification',
        'updated_vuln_description',
        'comment'
    ]
    for attr in attr_to_esc:
        if attr in context:
            value = context[attr]
            if isinstance(value, list):
                if all(isinstance(item, dict) for item in value):
                    context[attr] = [
                        {key: escape(item[key]) for key in item}
                        for item in value
                    ]
                else:
                    context[attr] = [escape(str(item)) for item in value]
            else:
                context[attr] = escape(str(value))
    return context


def _remove_test_projects(
        context: Dict[str, Union[str, int]],
        test_proj_list: List[str]) -> Dict[str, Union[str, int]]:
    findings = context.get('findings')
    if findings and isinstance(findings, list):
        new_findings = list()
        for fin in findings:
            fin_proj = fin.get('project', '').lower()
            if fin_proj not in test_proj_list:
                new_findings.append(fin)
        context['total'] = len(new_findings)
        context['findings'] = new_findings
    return context


async def _get_sqs_email_message_async(
    context: MailContentType,
    email_to: List[str],
    tags: List[str],
) -> Optional[Dict[str, List[Union[str, Dict[str, object]]]]]:
    project = str(context.get('project', '')).lower()
    test_proj_list = FI_TEST_PROJECTS.split(',')
    no_test_context = _remove_test_projects(
        cast(Dict[str, Union[str, int]], context),
        test_proj_list)
    new_context = _escape_context(no_test_context)
    message: Optional[Dict[str, List[Union[str, Dict[str, object]]]]] = None

    if project not in test_proj_list:
        message = {
            'to': [],
            'global_merge_vars': [],
            'merge_vars': []
        }
        for email in email_to:
            fname_mail = await get_recipient_first_name(email)
            merge_var = {
                'rcpt': email,
                'vars': [{'name': 'fname', 'content': fname_mail}]
            }
            message['to'].append({'email': email})
            message['merge_vars'].append(merge_var)
        for key, value in list(new_context.items()):
            message['global_merge_vars'].append(
                {'name': key, 'content': value}
            )
        message['tags'] = cast(List[Union[Dict[str, object], str]], tags)

    return message


async def _send_mail_async(
    template_name: str,
    email_to: List[str],
    context: MailContentType,
    tags: List[str],
) -> None:
    message = await _get_sqs_email_message_async(
        context=context,
        email_to=email_to,
        tags=tags,
    )

    if message:
        sqs_message = {
            'api_key': API_KEY,
            'message': message,
        }

        try:
            resource_options = dict(
                service_name='sqs',
                aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
                aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
                aws_session_token=os.environ.get('AWS_SESSION_TOKEN'),
                region_name='us-east-1'
            )
            async with aioboto3.client(**resource_options) as sqs:
                await log(
                    '[mailer]: sending to SQS',
                    extra={
                        'extra': {
                            'message': json.dumps(message),
                            'MessageGroupId': template_name,
                        }
                    })
                await sqs.send_message(
                    QueueUrl=QUEUE_URL,
                    MessageBody=json.dumps(sqs_message),
                    MessageGroupId=template_name
                )
                await log(
                    '[mailer]: mail sent',
                    extra={
                        'extra': {
                            'message': json.dumps(sqs_message["message"]),
                            'MessageGroupId': template_name,
                        }
                    })
        except (botocore.vendored.requests.exceptions.ConnectionError,
                botocore.exceptions.ClientError) as exc:
            LOGGER.exception(exc, extra=dict(extra=locals()))
    else:
        # Mail should not be sent if is a test project
        pass


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
                'message': json.dumps(message),
                'MessageGroupId': template_name,
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


async def _send_mail_immediately(
    context: MailContentType,
    email_to: List[str],
    tags: List[str],
    template_name: str,
) -> bool:
    await log('[mailer]: _send_mail_immediately', extra={'extra': {
        'context': context,
        'email_to': email_to,
        'template_name': template_name,
    }})

    result: List[Dict[str, str]] = []
    success: bool = False
    message = await _get_sqs_email_message_async(
        context=context,
        email_to=email_to,
        tags=tags,
    )

    if message:
        try:
            result = mandrill.Mandrill(API_KEY).messages.send_template(
                message=message,
                template_content=[],
                template_name=template_name,
            )
        except mandrill.InvalidKeyError as exc:
            LOGGER.exception(exc, extra=dict(extra=locals()))
            success = False
        else:
            success = True
    else:
        # Mail should not be sent if is a test project
        success = True

    await log('[mailer]: _send_mail_immediately', extra={'extra': {
        'email_to': email_to,
        'result': result,
        'success': success,
        'template_name': template_name,
    }})

    return success


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
        'comment': str(comment_data['content']).replace('\n', ' '),
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
        is_finding_released = finding_filters.is_released(finding)
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
        recipients = await project_domain.get_users_to_notify(
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
    project_users = await project_domain.get_users_to_notify(group)
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
    await _send_mail_async(
        'new-draft', email_to, context=context, tags=GENERAL_TAG)


async def send_mail_analytics(*email_to: str, **context: str) -> None:
    await log(
        ':'.join([*list(email_to), '[mailer]: send_mail_analytics']),
        extra={
            'extra': {
                'context': context,
                'to': email_to,
            }
        })

    await _send_mail_immediately(
        template_name='charts-report',
        email_to=list(email_to),
        context=cast(MailContentType, context),
        tags=GENERAL_TAG,
    )


async def send_mail_new_vulnerabilities(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'newvulnerabilitiesintegrates',
        email_to,
        context=context,
        tags=VULNERABILITIES_TAG
    )


async def send_mail_new_user(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'userfindingintegrates', email_to, context=context, tags=GENERAL_TAG
    )


async def send_mail_delete_finding(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'deletefindingintegrates',
        email_to,
        context=context,
        tags=GENERAL_TAG
    )


async def send_mail_remediate_finding(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'remediate-finding', email_to, context=context, tags=VERIFY_TAG
    )


async def send_mail_comment(
        email_to: List[List[str]],
        context: List[MailContentType]) -> None:
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
    await _send_mail_async(
        'project-report', email_to, context=context, tags=GENERAL_TAG)


async def send_mail_verified_finding(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'verified-finding', email_to, context=context, tags=VERIFY_TAG)


async def send_mail_updated_treatment(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'treatment-vulnerabilities',
        email_to,
        context=context,
        tags=GENERAL_TAG
    )


async def send_mail_new_remediated(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'newremediatefindingintegrates',
        email_to,
        context=context,
        tags=GENERAL_TAG
    )


async def send_mail_reject_draft(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'unsubmitted_draft', email_to, context=context, tags=GENERAL_TAG
    )


async def send_mail_new_releases(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'newreleasesintegrates', email_to, context=context, tags=GENERAL_TAG
    )


async def send_mail_access_granted(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'accessgrantedintegrates', email_to, context=context, tags=GENERAL_TAG
    )


async def send_mail_resources(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'resources-changes', email_to, context=context, tags=GENERAL_TAG
    )


async def send_mail_unsolved_events(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'unsolvedevents', email_to, context=context, tags=GENERAL_TAG
    )


async def send_mail_accepted_finding(
        email_to: List[str],
        context: MailContentType) -> None:
    await _send_mail_async(
        'acceptedfinding', email_to, context=context, tags=GENERAL_TAG
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


async def log(msg: str, **kwargs: Any) -> None:
    await in_thread(LOGGER_TRANSACTIONAL.info, msg, **kwargs)
