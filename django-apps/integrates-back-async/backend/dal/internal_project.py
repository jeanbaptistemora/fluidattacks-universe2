from typing import List
import rollbar
from botocore.exceptions import ClientError
from backend.dal.helpers import dynamodb

TABLE = 'fi_project_names'
DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore


def remove_project_name(project_name: str) -> bool:
    table = DYNAMODB_RESOURCE.Table(TABLE)
    primary_keys = {'project_name': project_name.lower()}
    resp = False
    try:
        item = table.get_item(Key=primary_keys)
        if item.get('Item'):
            response = table.delete_item(Key=primary_keys)
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt remove project name',
                               'error', extra_data=ex, payload_data=locals())
    return resp


def get_all_project_names() -> List[str]:
    table = DYNAMODB_RESOURCE.Table(TABLE)
    response = table.scan()
    projects = response['Items']
    while response.get('LastEvaluatedKey'):
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        projects += response['Items']
    names = [project['project_name'] for project in projects]
    return names
