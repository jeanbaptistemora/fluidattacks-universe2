#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Send notification email."""

import os
import git
import time
import mandrill

MANDRILL_APIKEY = os.environ['MANDRILL_APIKEY']
MANDRILL_EMAIL_TO = os.environ['MANDRILL_EMAIL_TO'].split(',')
PROJECT = os.environ['CI_PROJECT_NAME'].capitalize()
CI_COMMIT_SHA = os.environ['CI_COMMIT_SHA']
CI_COMMIT_BEFORE_SHA = os.environ['CI_COMMIT_BEFORE_SHA']

def _get_message() -> str:
    """Get Summary and Author Name of commits."""
    repo = git.Repo(os.getcwd())
    message: str = repo.git.log(
        CI_COMMIT_BEFORE_SHA + '...' + CI_COMMIT_SHA,
        '--pretty=format:<b>%s</b>%n%bCommitted by: %aN%n')
    return message.replace('\n', '<br/>\n')


def _get_version_date() -> str:
    """Get version of last deploy."""
    cur_time = time.localtime()
    min_month = (cur_time.tm_mday - 1) * 1440 + cur_time.tm_hour * 60 + \
        cur_time.tm_min
    return time.strftime('%y.%m.{}').format(min_month)


def send_mail(template_name: str, email_to, context, tags) -> None:
    """Send notification email."""
    mandrill_client = mandrill.Mandrill(MANDRILL_APIKEY)
    message = {
        'to': [
            {'email': email} for email in email_to
        ],
        'global_merge_vars': [
            {'name': key, 'content': value} for key, value in context.items()
        ],
        'tags': tags,
    }
    mandrill_client.messages.send_template(template_name, [], message)
