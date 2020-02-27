"""DAL functions for alerts."""

from typing import Any, Dict, List
import rollbar
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from backend.dal import project as project_dal
from backend.dal.helpers import dynamodb

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('FI_alerts_by_company')


def get(company_name: str, project_name: str) -> List[Dict[str, Any]]:
    """ Get alerts of a company. """
    company_name = company_name.lower()
    project_name = project_name.lower()
    filter_key = 'company_name'
    filter_sort = 'project_name'
    if project_name == 'all':
        filtering_exp = Key(filter_key).eq(company_name)
        response = TABLE.query(
            KeyConditionExpression=filtering_exp)
    else:
        filtering_exp = (Key(filter_key).eq(company_name) &  # type: ignore
                         Key(filter_sort).eq(project_name))
        response = TABLE.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        response = TABLE.query(
            KeyConditionExpression=filtering_exp,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']
    return items


def change_status(message: str, company_name: str, project_name: str) -> bool:
    """ Activate or deactivate the alert of a company. """
    message = message.lower()
    company_name = company_name.lower()
    project_name = project_name.lower()
    if ((project_name == 'all' and message == 'deactivate') or
            (project_name != 'all' and message == 'deactivate')):
        status = '0'
    else:
        status = '1'
    item = get(company_name, project_name)
    for _item in item:
        payload = {'company_name': _item['company_name'],
                   'project_name': _item['project_name'], }
        try:
            TABLE.update_item(
                Key=payload,
                UpdateExpression='SET status_act = :val1',
                ExpressionAttributeValues={
                    ':val1': status,
                }
            )
        except ClientError:
            rollbar.report_exc_info()
            return False
    return True


def put(message: str, company_name: str, project_name: str) -> bool:
    """ Create, update or activate an alert for a company. """
    project_name = project_name.lower()
    company_name = company_name.lower()
    project_exists = project_dal.exists(project_name)
    resp = False
    if project_name == 'all' or project_exists:
        item = get(company_name, project_name)
        if item == []:
            try:
                response = TABLE.put_item(
                    Item={
                        'company_name': company_name,
                        'project_name': project_name,
                        'message': message,
                        'status_act': '1',
                    }
                )
                resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            except ClientError:
                rollbar.report_exc_info()
        else:
            for _item in item:
                try:
                    response = TABLE.update_item(
                        Key={
                            'company_name': _item['company_name'],
                            'project_name': _item['project_name'],
                        },
                        UpdateExpression='SET message = :val1,\
                            status_act = :val2',
                        ExpressionAttributeValues={
                            ':val1': str(message),
                            ':val2': '1',
                        }
                    )
                except ClientError:
                    rollbar.report_exc_info()
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    return resp
