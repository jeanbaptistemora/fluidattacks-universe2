from app import util
from app.dal import comment as comment_dal


def _get_comments(comment_type, finding_id):
    comments = [{
        'content': comment['content'],
        'created': util.format_comment_date(comment['created']),
        'email': comment['email'],
        'fullname': comment['fullname'],
        'id': int(comment['user_id']),
        'modified': util.format_comment_date(comment['modified']),
        'parent': int(comment['parent'])
    } for comment in comment_dal.get_comments(comment_type, int(finding_id))]

    return comments


def get_comments(finding_id):
    comments = _get_comments('comment', finding_id)

    return comments


def get_observations(finding_id):
    observations = _get_comments('observation', finding_id)

    return observations
