"""Domain functions for projects."""
# pylint: disable=F0401
# pylint: disable=relative-beyond-top-level
# Disabling this rule is necessary for importing modules beyond the top level
# directory.

import threading
import re

from app.dao import integrates_dao
from app.mailer import send_mail_comment


def comment_has_parent(comment_data):
    """Check if a comment has a parent."""
    return comment_data['parent'] != 0


def get_email_recipients(project_name):
    """Get the recipients of the comment email."""
    project_users = integrates_dao.get_project_users(project_name)
    recipients = [user[0] for user in project_users if user[1] == 1]
    return recipients


def send_comment_mail(project_name, email, comment_data):
    """Send a mail in a project."""
    parent = comment_data['parent']
    recipients = get_email_recipients(project_name)
    base_url = 'https://fluidattacks.com/integrates/dashboard#!'
    mail_context = {
        'project': project_name,
        'user_email': email,
        'comment_type': 'project',
        'parent': parent,
        'comment': comment_data['content'].replace('\n', ' '),
        'comment_url':
            base_url + '/project/{project!s}/comments'
        .format(project=project_name)
    }
    email_send_thread = threading.Thread(
        name='New project email thread',
        target=send_mail_comment,
        args=(recipients,
              mail_context))
    email_send_thread.start()


def add_comment(project_name, email, comment_data):
    """Add comment in a project."""
    send_comment_mail(project_name, email, comment_data)
    return integrates_dao.add_project_comment_dynamo(project_name,
                                                     email,
                                                     comment_data)


def validate_tags(tags):
    """Validate tags array."""
    tags_validated = []
    pattern = re.compile('^[a-z0-9]+(?:-[a-z0-9]+)*$')
    for tag in tags:
        if pattern.match(tag):
            tags_validated.append(tag)
        else:
            # Invalid tag
            pass
    return tags_validated


def validate_project(project):
    """Validate if a project exist and is not deleted."""
    project_info = integrates_dao.get_project_attributes_dynamo(
        project, ['project_name', 'deletion_date'])
    is_valid_project = False
    if project_info:
        if project_info.get('deletion_date'):
            is_valid_project = False
        else:
            is_valid_project = True
    else:
        is_valid_project = False
    return is_valid_project
