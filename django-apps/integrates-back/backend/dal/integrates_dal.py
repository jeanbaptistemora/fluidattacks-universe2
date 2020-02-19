
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import rollbar

from backend.dal.helpers import dynamodb

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE


def add_finding_comment_dynamo(finding_id, email, comment_data):
    """ Add a comment in a finding. """
    table = DYNAMODB_RESOURCE.Table('FI_comments')
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
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def remove_role_to_project_dynamo(project_name, user_email, role):
    """Remove user role in a project."""
    table = DYNAMODB_RESOURCE.Table('FI_projects')
    try:
        response = table.update_item(
            Key={
                'project_name': project_name.lower(),
            },
            UpdateExpression='DELETE #rol :val1',
            ExpressionAttributeNames={
                '#rol': role
            },
            ExpressionAttributeValues={
                ':val1': set([user_email])
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def weekly_report_dynamo(
        init_date, finish_date, registered_users, logged_users, companies):
    """ Save the number of registered and logged users weekly. """
    table = DYNAMODB_RESOURCE.Table('FI_weekly_report')
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
        return resp
    except ClientError:
        rollbar.report_exc_info()
        return False


def get_data_dynamo(table_name, primary_name_key, primary_key):
    """Get atributes data."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    primary_key = primary_key.lower()
    filter_key = primary_name_key
    filtering_exp = Key(filter_key).eq(primary_key)
    response = table.query(KeyConditionExpression=filtering_exp)
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                KeyConditionExpression=filtering_exp,
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items


def get_data_dynamo_filter(table_name, filter_exp='', data_attr=''):
    """Get atributes data."""
    table = DYNAMODB_RESOURCE.Table(table_name)
    scan_attrs = {}
    if data_attr:
        scan_attrs['ProjectionExpression'] = data_attr
    else:
        # ProjectionExpression not especified
        pass
    if filter_exp:
        scan_attrs['FilterExpression'] = filter_exp

    response = table.scan(**scan_attrs)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        scan_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = table.scan(**scan_attrs)
        items += response['Items']

    return items
