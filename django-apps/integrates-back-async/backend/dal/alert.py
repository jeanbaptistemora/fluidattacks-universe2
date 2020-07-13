"""DAL functions for alerts."""

from typing import Dict, List
from boto3.dynamodb.conditions import Key

from backend.dal.helpers import dynamodb

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('FI_alerts_by_company')


def get(company: str, project_name: str) -> List[Dict[str, str]]:
    """ Get alerts of a company. """
    company_name = company.lower() if company else ' '
    project_name = project_name.lower()
    filter_key = 'company_name'
    filter_sort = 'project_name'
    if project_name == 'all':
        filtering_exp: object = Key(filter_key).eq(company_name)
        response = TABLE.query(
            KeyConditionExpression=filtering_exp)
    else:
        filtering_exp = (Key(filter_key).eq(company_name) &
                         Key(filter_sort).eq(project_name))
        response = TABLE.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        response = TABLE.query(
            KeyConditionExpression=filtering_exp,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']
    return items
