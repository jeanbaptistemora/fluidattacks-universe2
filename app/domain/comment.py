import hashlib
from app import util
from app.dal import comment as comment_dal
from app.domain import user as user_domain


def _get_comments(comment_type, finding_id, user_role):
    comments = [{
        'content': comment['content'],
        'created': util.format_comment_date(comment['created']),
        'email': comment['email'],
        'fullname': comment['fullname']
        if user_role in ['admin', 'analyst']
        or user_domain.get_data(comment['email'], 'role') == 'customer'
        else "Hacker " + hashlib.sha256(comment['fullname'].encode()).hexdigest()[-4:].upper(),
        'id': int(comment['user_id']),
        'modified': util.format_comment_date(comment['modified']),
        'parent': int(comment['parent'])
    } for comment in comment_dal.get_comments(comment_type, int(finding_id))]
    return comments


def get_comments(finding_id, user_role):
    comments = _get_comments('comment', finding_id, user_role)

    return comments


def get_observations(finding_id):
    observations = _get_comments('observation', finding_id, None)

    return observations
