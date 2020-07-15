import os
import json
import threading
from html import escape
from typing import Dict, List, Union, cast

import boto3
import botocore
import rollbar
from asgiref.sync import async_to_sync

from backend import authz
from backend.domain import (
    project as project_domain,
    user as user_domain
)
from backend.dal.comment import CommentType
from backend.typing import (
    Event as EventType,
    Finding as FindingType,
    Project as ProjectType
)
from backend.utils import aio
from backend.utils.logging import log

from __init__ import (
    BASE_URL,
    FI_MAIL_REVIEWERS,
    FI_MANDRILL_API_KEY,
    FI_TEST_PROJECTS,
    FI_AWS_DYNAMODB_ACCESS_KEY,
    FI_AWS_DYNAMODB_SECRET_KEY,
    SQS_QUEUE_URL
)


API_KEY = FI_MANDRILL_API_KEY
VERIFY_TAG = ['verify']
COMMENTS_TAG = ['comments']
VULNERABILITIES_TAG = ['vulnerabilities']
GENERAL_TAG = ['general']
QUEUE_URL = SQS_QUEUE_URL


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


def _get_recipient_first_name(email: str) -> str:
    first_name = user_domain.get_data(email, 'first_name')
    if not first_name:
        first_name = email.split('@')[0]
    else:
        # First name exists in database
        pass
    return str(first_name)


# pylint: disable=too-many-locals
def _send_mail(
        template_name: str,
        email_to: List[str],
        context: Dict[str, Union[str, int]],
        tags: List[str]):
    project = str(context.get('project', '')).lower()
    test_proj_list = FI_TEST_PROJECTS.split(',')
    sqs = boto3.client(  # type: ignore
        'sqs',
        aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
        aws_session_token=os.environ.get('AWS_SESSION_TOKEN'),
        region_name='us-east-1'
    )
    no_test_context = _remove_test_projects(context, test_proj_list)
    new_context = _escape_context(no_test_context)
    if project not in test_proj_list:
        message: Dict[str, List[Union[str, Dict[str, object]]]] = {
            'to': [],
            'global_merge_vars': [],
            'merge_vars': []
        }
        for email in email_to:
            fname_mail = _get_recipient_first_name(email)
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
        try:
            sqs_message = {
                'message': message,
                'api_key': API_KEY
            }
            rollbar.report_message(
                (f'sending mail: {json.dumps(sqs_message["message"])}'
                 f'MessageGroupId={template_name}'),
                'debug'
            )
            sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=json.dumps(sqs_message),
                MessageGroupId=template_name
            )
            rollbar.report_message(
                (f'mail sent: {json.dumps(sqs_message["message"])}'
                 f'MessageGroupId={template_name}'),
                'debug'
            )
        except (botocore.vendored.requests.exceptions.ConnectionError,
                botocore.exceptions.ClientError) as exc:
            rollbar.report_message(exc)
    else:
        # Mail should not be sent if is a test project
        pass


def send_comment_mail(
        comment_data: CommentType,
        entity_name: str,
        user_mail: str,
        comment_type: str = '',
        entity: Union[
            str,
            Dict[str, FindingType],
            EventType,
            ProjectType
        ] = ''):
    parent = comment_data['parent']
    email_context = {
        'user_email': user_mail,
        'comment': str(comment_data['content']).replace('\n', ' '),
        'comment_type': comment_type,
        'parent': parent,
    }
    if entity_name == 'finding':
        finding: Dict[str, FindingType] = cast(Dict[str, FindingType], entity)
        project_name = str(finding.get('projectName', ''))
        recipients = get_email_recipients(project_name, comment_type)

        is_draft = 'releaseDate' in finding
        email_context['finding_id'] = str(finding.get('findingId', ''))
        email_context['finding_name'] = str(finding.get('finding', ''))
        comment_url = (
            BASE_URL +
            f'/groups/{project_name}/' +
            ('findings' if is_draft else 'drafts') +
            '/' + finding.get('findingId') +
            f'/{comment_type}s'
        )

    elif entity_name == 'event':
        event = cast(EventType, entity)
        event_id = str(event.get('event_id', ''))
        project_name = str(event.get('project_name', ''))
        recipients = async_to_sync(project_domain.get_users_to_notify)(
            project_name, True
        )
        email_context['finding_id'] = event_id
        email_context['finding_name'] = f'Event #{event_id}'
        comment_url = (
            f'{BASE_URL}/groups/{project_name}/events/{event_id}/comments'
        )

    elif entity_name == 'project':
        project_name = str(entity)
        recipients = get_email_recipients(project_name, True)
        comment_url = f'{BASE_URL}/groups/{project_name}/comments'

    email_context['comment_url'] = comment_url
    email_context['project'] = project_name

    recipients_customers = [
        recipient
        for recipient in recipients
        if authz.get_group_level_role(
            recipient, project_name) in ['customer', 'customeradmin']
    ]
    recipients_not_customers = [
        recipient
        for recipient in recipients
        if authz.get_group_level_role(
            recipient, project_name) not in ['customer', 'customeradmin']
    ]

    email_context_customers = email_context.copy()
    if authz.get_group_level_role(
            user_mail, project_name) not in ['customer', 'customeradmin']:
        email_context_customers['user_email'] = f'Hacker at FluidIntegrates'
    email_send_thread = threading.Thread(
        name='New {} email thread'.format(entity_name),
        target=send_mail_comment,
        args=(
            [recipients_not_customers, recipients_customers],
            [email_context, email_context_customers]
        )
    )
    email_send_thread.start()


def get_email_recipients(group: str, comment_type: Union[str, bool]) -> \
        List[str]:
    project_users = async_to_sync(project_domain.get_users_to_notify)(group)
    recipients: List[str] = []

    approvers = FI_MAIL_REVIEWERS.split(',')
    recipients += approvers

    if comment_type == 'observation':
        analysts = [
            email
            for email in project_users
            if authz.get_group_level_role(email, group) == 'analyst'
        ]
        recipients += analysts
    else:
        recipients += project_users

    return recipients


def send_mail_new_draft(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail('new-draft', email_to, context=context, tags=GENERAL_TAG)


async def send_mail_charts(*email_to: str, **context: str) -> None:
    await log(f'send_mail_charts(email_to={email_to}, context={context})',
              level='info')

    await aio.ensure_io_bound(
        function=_send_mail,
        template_name='charts-report',
        email_to=email_to,
        context=context,
        tags=GENERAL_TAG,
    )


def send_mail_new_vulnerabilities(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'newvulnerabilitiesintegrates',
        email_to,
        context=context,
        tags=VULNERABILITIES_TAG
    )


def send_mail_new_user(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'userfindingintegrates', email_to, context=context, tags=GENERAL_TAG
    )


def send_mail_delete_finding(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'deletefindingintegrates',
        email_to,
        context=context,
        tags=GENERAL_TAG
    )


def send_mail_remediate_finding(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'remediate-finding', email_to, context=context, tags=VERIFY_TAG
    )


def send_mail_comment(
        email_to: List[List[str]],
        context: List[Dict[str, Union[str, int]]]):
    _send_mail(
        'new-comment', email_to[0], context=context[0], tags=COMMENTS_TAG
    )
    _send_mail(
        'new-comment', email_to[1], context=context[1], tags=COMMENTS_TAG
    )


def send_mail_project_report(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail('project-report', email_to, context=context, tags=GENERAL_TAG)


def send_mail_verified_finding(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail('verified-finding', email_to, context=context, tags=VERIFY_TAG)


def send_mail_updated_manager(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail('manager-updated', email_to, context=context, tags=GENERAL_TAG)


def send_mail_new_remediated(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'newremediatefindingintegrates',
        email_to,
        context=context,
        tags=GENERAL_TAG
    )


def send_mail_reject_draft(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'unsubmitted_draft', email_to, context=context, tags=GENERAL_TAG
    )


def send_mail_new_releases(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'newreleasesintegrates', email_to, context=context, tags=GENERAL_TAG
    )


def send_mail_access_granted(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'accessgrantedintegrates', email_to, context=context, tags=GENERAL_TAG
    )


def send_mail_resources(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'resources-changes', email_to, context=context, tags=GENERAL_TAG
    )


def send_mail_unsolved_events(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'unsolvedevents', email_to, context=context, tags=GENERAL_TAG
    )


def send_mail_accepted_finding(
        email_to: List[str],
        context: Dict[str, Union[str, int]]):
    _send_mail(
        'acceptedfinding', email_to, context=context, tags=GENERAL_TAG
    )


def send_mail_new_event(
        email_to: List[List[str]],
        context: List[Dict[str, Union[str, int]]]):
    _send_mail('new-event', email_to[0], context=context[0], tags=GENERAL_TAG)
    _send_mail('new-event', email_to[1], context=context[1], tags=GENERAL_TAG)
