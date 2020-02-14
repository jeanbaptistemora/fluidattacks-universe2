import rollbar
from botocore.exceptions import ClientError
from backend.dal import integrates_dal
from backend.dal.helpers import dynamodb

TABLE = 'fi_project_names'
DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE


def exists(project_name):
    primary_key = {'project_name': project_name.lower()}
    return integrates_dal.attribute_exists(
        TABLE, primary_key, ['project_name'])


def remove_project_name(project_name):
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


def get_all_project_names():
    names = [project['project_name']
             for project in integrates_dal.get_data_dynamo_filter(TABLE)]
    return names
