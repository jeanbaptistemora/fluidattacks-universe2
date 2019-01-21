from __future__ import absolute_import
import mandrill
from __init__ import FI_MANDRILL_API_KEY

API_KEY = FI_MANDRILL_API_KEY
VERIFY_TAG = ['verify']
COMMENTS_TAG = ['comments']
VULNERABILITIES_TAG = ['vulnerabilities']
AGE_TAG = ['age']
GENERAL_TAG = ['general']


def _send_mail(template_name, email_to, context, tags):
    mandrill_client = mandrill.Mandrill(API_KEY)
    message = {
        'to': [],
        'global_merge_vars': []
    }
    for em in email_to:
        message['to'].append({'email': em})

    for k, v in context.items():
        message['global_merge_vars'].append(
            {'name': k, 'content': v}
        )
    message['tags'] = tags
    mandrill_client.messages.send_template(template_name, [], message)


def send_mail_new_vulnerabilities(email_to, context):
    _send_mail('newvulnerabilitiesintegrates', email_to, context=context, tags=VULNERABILITIES_TAG)


def send_mail_change_finding(email_to, context):
    _send_mail('changefindingintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_new_user(email_to, context):
    _send_mail('userfindingintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_delete_finding(email_to, context):
    _send_mail('deletefindingintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_remediate_finding(email_to, context):
    _send_mail('remediatefindingintegrates', email_to, context=context, tags=VERIFY_TAG)


def send_mail_new_comment(email_to, context, comment_type):
    if comment_type == 'project':
        _send_mail('newprojectcommentintegrates', email_to, context=context, tags=COMMENTS_TAG)
    elif comment_type == 'observation':
        _send_mail('newobservationintegrates', email_to, context=context, tags=COMMENTS_TAG)
    else:
        _send_mail('newcommentintegrates', email_to, context=context, tags=COMMENTS_TAG)


def send_mail_reply_comment(email_to, context, comment_type):
    if comment_type == 'project':
        _send_mail('replyprojectcommentintegrates', email_to, context=context, tags=COMMENTS_TAG)
    elif comment_type == 'observation':
        _send_mail('replyobservationintegrates', email_to, context=context, tags=COMMENTS_TAG)
    else:
        _send_mail('replycommentintegrates', email_to, context=context, tags=COMMENTS_TAG)


def send_mail_verified_finding(email_to, context):
    _send_mail('verifiedfindingintegrates', email_to, context=context, tags=VERIFY_TAG)


def send_mail_new_remediated(email_to, context):
    _send_mail('newremediatefindingintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_add_access(email_to, context):
    _send_mail('addaccessintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_age_finding(email_to, context):
    _send_mail('agefindingintegrates', email_to, context=context, tags=AGE_TAG)


def send_mail_age_kb_finding(email_to, context):
    _send_mail('agekbfindingintegrates', email_to, context=context, tags=AGE_TAG)


def send_mail_delete_draft(email_to, context):
    _send_mail('deletedraftintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_new_releases(email_to, context):
    _send_mail('newreleasesintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_access_granted(email_to, context):
    _send_mail('accessgrantedintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_continuous_report(email_to, context):
    _send_mail('continuousreport', email_to, context=context, tags=GENERAL_TAG)


def send_mail_integrates_new_version(email_to, context):
    _send_mail('integratesnewversion', email_to, context=context, tags=GENERAL_TAG)


def send_mail_repositories(email_to, context):
    _send_mail('repositoriesintegrates', email_to, context=context, tags=GENERAL_TAG)


def send_mail_unsolved_events(email_to, context):
    _send_mail('unsolvedevents', email_to, context=context, tags=GENERAL_TAG)


def send_mail_accepted_finding(email_to, context):
    _send_mail('acceptedfinding', email_to, context=context, tags=GENERAL_TAG)


def send_mail_project_deletion(email_to, context):
    _send_mail('projectdeletion', email_to, context=context, tags=GENERAL_TAG)
