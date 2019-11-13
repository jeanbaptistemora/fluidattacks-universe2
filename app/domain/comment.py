import hashlib
from app import util
from app.dal import comment as comment_dal
from app.domain import user as user_domain


def _get_comments(comment_type, finding_id, user_role):
    comments = [fill_comment_data(user_role, comment)
                for comment in comment_dal.get_comments(comment_type, int(finding_id))]
    return comments


def get_comments(finding_id, user_role):
    comments = _get_comments('comment', finding_id, user_role)

    return comments


def fill_comment_data(user_role, data):
    return {
        'content': data['content'],
        'created': util.format_comment_date(data['created']),
        'email': data['email'],
        'fullname':
            (data['fullname']
                if user_role in ['admin', 'analyst']
                or user_domain.get_data(data['email'], 'role') == 'customer'
                else "Hacker " + hashlib.sha256(data['fullname'].encode())
                .hexdigest()[-4:].upper())
            if 'fullname' in data else data['email'],
        'id': int(data['user_id']),
        'modified': util.format_comment_date(data['modified']),
        'parent': int(data['parent'])}


def get_observations(finding_id, user_role):
    observations = _get_comments('observation', finding_id, user_role)

    return observations
