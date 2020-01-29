#! /usr/bin/env python3

"""Send notification email."""

import os
import git
import glob
import ntpath
import mandrill

import get_version

MANDRILL_APIKEY = os.environ['MANDRILL_APIKEY']

CI_COMMIT_SHA = os.environ['CI_COMMIT_SHA']
CI_COMMIT_BEFORE_SHA = os.environ['CI_COMMIT_BEFORE_SHA']


def _get_message() -> str:
    """Get Summary and Author Name of commits."""
    repo = git.Repo(os.getcwd())
    message: str = repo.git.log(
        CI_COMMIT_BEFORE_SHA + '...' + CI_COMMIT_SHA,
        '--pretty=format:<b>%s</b>%n%bAuthored by: %aN%n')
    return message.replace('\n', '<br/>\n')


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


send_mail(
    template_name='new_version',
    email_to=[
      'engineering@fluidattacks.com',
    ],
    context={
        'project': 'Asserts',
        'version': get_version.get_version(),
        'message': _get_message(),
        'project_url': 'https://fluidattacks.com/asserts/',
    },
    tags=[
        'general',
    ])
