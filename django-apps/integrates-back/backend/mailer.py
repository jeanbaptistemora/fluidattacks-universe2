from html import escape
import json
import threading

import boto3
import botocore
import rollbar

from backend.domain import user as user_domain
from backend.dal import project as project_dal

from __init__ import (FI_MAIL_REPLYERS, FI_MAIL_REVIEWERS, FI_MANDRILL_API_KEY,
                      FI_TEST_PROJECTS, FI_AWS_DYNAMODB_ACCESS_KEY, FI_AWS_DYNAMODB_SECRET_KEY,
                      SQS_QUEUE_URL)


API_KEY = FI_MANDRILL_API_KEY
VERIFY_TAG = ['verify']
COMMENTS_TAG = ['comments']
VULNERABILITIES_TAG = ['vulnerabilities']
GENERAL_TAG = ['general']
QUEUE_URL = SQS_QUEUE_URL


def _escape_context(context):
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
                    context[attr] = [{key: escape(item[key]) for key in item}
                                     for item in value]
                else:
                    context[attr] = [escape(str(item)) for item in value]
            else:
                context[attr] = escape(value)
    return context


def _remove_test_projects(context, test_proj_list):
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


def _get_recipient_first_name(email):
    first_name = user_domain.get_data(email, 'first_name')
    if not first_name:
        first_name = email.split('@')[0]
    else:
        # First name exists in database
        pass
    return first_name


# pylint: disable=too-many-locals
def _send_mail(template_name, email_to, context, tags):
    project = context.get('project', '').lower()
    test_proj_list = FI_TEST_PROJECTS.split(',')
    sqs = boto3.client('sqs', aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
                       aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
                       region_name='us-east-1')
    no_test_context = _remove_test_projects(context, test_proj_list)
    new_context = _escape_context(no_test_context)
    if project not in test_proj_list:
        message = {
            'to': [],
            'global_merge_vars': [],
            'merge_vars': []
        }
        for email in email_to:
            fname_mail = _get_recipient_first_name(email)
            merge_var = {'rcpt': email,
                         'vars': [{'name': 'fname',
                                   'content': fname_mail}]}
            message['to'].append({'email': email})
            message['merge_vars'].append(merge_var)
        for key, value in list(new_context.items()):
            message['global_merge_vars'].append(
                {'name': key, 'content': value}
            )
        message['tags'] = tags
        try:
            sqs_message = {
                'message': message,
                'api_key': API_KEY
            }
            rollbar.report_message(
                (f'sending mail: {json.dumps(sqs_message["message"])}'
                 f'MessageGroupId={template_name}'),
                'debug')
            sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=json.dumps(sqs_message),
                MessageGroupId=template_name
            )
            rollbar.report_message(
                (f'mail sent: {json.dumps(sqs_message["message"])}'
                 f'MessageGroupId={template_name}'),
                'debug')
        except (botocore.vendored.requests.exceptions.ConnectionError,
                botocore.exceptions.ClientError) as exc:
            rollbar.report_message(exc.message)
    else:
        # Mail should not be sent if is a test project
        pass


def send_comment_mail(comment_data, entity_name, user_mail, comment_type='', entity=''):
    parent = comment_data['parent']
    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    email_context = {
        'user_email': user_mail,
        'comment': comment_data['content'].replace('\n', ' '),
        'comment_type': comment_type,
        'parent': parent,
    }
    if entity_name == 'finding':
        finding = entity
        project_name = finding.get('projectName')
        recipients = get_email_recipients(finding.get('projectName'), comment_type)

        is_draft = 'releaseDate' in finding
        email_context['finding_id'] = finding.get('id')
        email_context['finding_name'] = finding.get('finding')
        comment_url = (
            base_url +
            '/project/{project}/{finding_type}/{id}/{comment_type}s'.format(
                comment_type=comment_type,
                finding_type='findings' if is_draft else 'drafts',
                id=entity.get('id'),
                project=project_name))

    elif entity_name == 'event':
        event = entity
        event_id = event.get('event_id')
        project_name = event.get('project_name')
        recipients = project_dal.get_users(project_name, True)
        email_context['finding_id'] = event_id
        email_context['finding_name'] = f'Event #{event_id}'
        comment_url = (
            'https://fluidattacks.com/integrates/dashboard#!/'
            f'project/{project_name}/events/{event_id}/comments')

    elif entity_name == 'project':
        project_name = entity
        recipients = get_email_recipients(project_name, True)
        comment_url = (
            base_url + '/project/{project!s}/comments'.format(project=project_name))

    email_context['comment_url'] = comment_url
    email_context['project'] = project_name

    recipients_customers = [
        recipient for recipient in recipients
        if user_domain.get_data(recipient, 'role') in ['customer', 'customeradmin']]
    recipients_not_customers = [
        recipient for recipient in recipients
        if user_domain.get_data(recipient, 'role') not in ['customer', 'customeradmin']]

    email_context_customers = email_context.copy()
    email_context_customers['user_email'] = \
        'Hacker at ' + user_domain.get_data(user_mail, 'company').capitalize()

    email_send_thread = threading.Thread(
        name='New {} email thread'.format(entity_name),
        target=send_mail_comment,
        args=([recipients_not_customers, recipients_customers],
              [email_context, email_context_customers]))
    email_send_thread.start()


def get_email_recipients(project_name, comment_type):
    project_users = project_dal.get_users(project_name)
    recipients = []

    if comment_type == 'observation':
        approvers = FI_MAIL_REVIEWERS.split(',')
        analysts = [user for user in project_users
                    if user_domain.get_data(user, 'role') == 'analyst']

        recipients += approvers
        recipients += analysts
    else:
        recipients = project_users
        replyers = FI_MAIL_REPLYERS.split(',')
        recipients += replyers

    return recipients


def send_mail_new_draft(email_to, context):
    _send_mail('new-draft', email_to, context=context, tags=GENERAL_TAG)


def send_mail_new_vulnerabilities(email_to, context):
    _send_mail('newvulnerabilitiesintegrates', email_to, context=context, tags=VULNERABILITIES_TAG)


def send_mail_new_user(email_to, context):
    _send_mail('userfindingintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_delete_finding(email_to, context):
    _send_mail('deletefindingintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_remediate_finding(email_to, context):
    _send_mail('remediate-finding',
               email_to,
               context=context,
               tags=VERIFY_TAG)


def send_mail_comment(email_to, context):
    _send_mail('new-comment',
               email_to[0],
               context=context[0],
               tags=COMMENTS_TAG)
    _send_mail('new-comment',
               email_to[1],
               context=context[1],
               tags=COMMENTS_TAG)


def send_mail_verified_finding(email_to, context):
    _send_mail('verified-finding', email_to, context=context, tags=VERIFY_TAG)


def send_mail_new_remediated(email_to, context):
    _send_mail('newremediatefindingintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_reject_draft(email_to, context):
    _send_mail('unsubmitted_draft', email_to, context=context, tags=GENERAL_TAG)


def send_mail_new_releases(email_to, context):
    _send_mail('newreleasesintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_access_granted(email_to, context):
    _send_mail('accessgrantedintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_new_version(email_to, context):
    _send_mail('new_version', email_to, context=context, tags=GENERAL_TAG)


def send_mail_resources(email_to, context):
    _send_mail('resources-changes',
               email_to,
               context=context,
               tags=GENERAL_TAG)


def send_mail_unsolved_events(email_to, context):
    _send_mail('unsolvedevents', email_to, context=context, tags=GENERAL_TAG)


def send_mail_accepted_finding(email_to, context):
    _send_mail('acceptedfinding', email_to, context=context, tags=GENERAL_TAG)


def send_mail_updated_vulns(email_to, context):
    _send_mail('updated-vulns', email_to, context=context, tags=GENERAL_TAG)


def send_mail_project_deletion(email_to, context):
    _send_mail('projectdeletion', email_to, context=context, tags=GENERAL_TAG)


def send_mail_new_event(email_to, context):
    _send_mail('new-event', email_to, context=context, tags=GENERAL_TAG)
