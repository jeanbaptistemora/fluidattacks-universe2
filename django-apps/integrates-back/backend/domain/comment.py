import hashlib
from datetime import datetime
from time import time

import pytz
from django.conf import settings

from backend.domain import user as user_domain

from app import util
from app.dal import comment as comment_dal


def _get_comments(comment_type, finding_id, user_role):
    comments = [fill_comment_data(user_role, comment)
                for comment in comment_dal.get_comments(comment_type, int(finding_id))]
    return comments


def get_comments(finding_id, user_role):
    comments = _get_comments('comment', finding_id, user_role)

    return comments


def get_event_comments(finding_id, user_role):
    comments = _get_comments('event', finding_id, user_role)

    return comments


def get_fullname(user_role, data):
    if 'fullname' not in data:

        return data['email']

    return (data['fullname']
            if user_role in ['admin', 'analyst']
            or user_domain.get_data(data['email'], 'role') == 'customer'
            else 'Hacker ' + hashlib.sha256(data['fullname'].encode())
            .hexdigest()[-4:].upper())


def fill_comment_data(user_role, data):
    fullname = get_fullname(user_role, data)
    return {
        'content': data['content'],
        'created': util.format_comment_date(data['created']),
        'email': data['email'],
        'fullname': fullname,
        'id': int(data['user_id']),
        'modified': util.format_comment_date(data['modified']),
        'parent': int(data['parent'])}


def get_observations(finding_id, user_role):
    observations = _get_comments('observation', finding_id, user_role)

    return observations


def create(comment_type, content, element_id, parent, user_info):
    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    comment_id = int(round(time() * 1000))
    comment_attributes = {
        'comment_type': comment_type,
        'content': content,
        'created': today,
        'email': user_info['user_email'],
        'finding_id': int(element_id),
        'fullname': str.join(
            ' ', [user_info['first_name'], user_info['last_name']]),
        'modified': today,
        'parent': int(parent)
    }
    success = comment_dal.create(comment_id, comment_attributes)

    return (comment_id if success else None, success)
