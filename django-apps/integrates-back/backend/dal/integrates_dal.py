
from typing import Dict, List
from botocore.exceptions import ClientError
import rollbar

from backend.dal.helpers import dynamodb

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore


def add_finding_comment_dynamo(finding_id: str, email: str, comment_data: Dict[str, str]) -> bool:
    """ Add a comment in a finding. """
    table = DYNAMODB_RESOURCE.Table('FI_comments')
    resp = False
    try:
        payload = {
            'finding_id': finding_id,
            'email': email
        }
        payload.update(comment_data)
        response = table.put_item(
            Item=payload
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


def weekly_report_dynamo(init_date: str, finish_date: str, registered_users: List[str],
                         logged_users: List[str], companies: List[str]) -> bool:
    """ Save the number of registered and logged users weekly. """
    table = DYNAMODB_RESOURCE.Table('FI_weekly_report')
    resp = False
    try:
        response = table.put_item(
            Item={
                'init_date': init_date,
                'finish_date': finish_date,
                'registered_users': registered_users,
                'logged_users': logged_users,
                'companies': companies,
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp
