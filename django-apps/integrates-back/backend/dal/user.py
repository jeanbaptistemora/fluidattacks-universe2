
from typing import Dict, List
import rollbar
from boto3.dynamodb.conditions import Attr, Key, Not
from botocore.exceptions import ClientError
from backend.dal.helpers import dynamodb
from backend.typing import User as UserType

from __init__ import FI_TEST_PROJECTS

TABLE = 'FI_users'

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
ACCESS_TABLE = DYNAMODB_RESOURCE.Table('FI_project_access')


def get_all_companies() -> List[str]:
    filter_exp = Attr('company').exists()
    users = get_all(filter_exp)
    companies = [user.get('company', '').strip().upper() for user in users]
    return list(set(companies))


def get_all_inactive_users(final_date: str) -> List[str]:
    filtering_exp = Attr('registered').exists() & \
        Attr('registered').eq(False) & \
        (Attr('last_login').not_exists() |
         (Attr('last_login').exists() & Attr('last_login').lte(final_date)))
    users = get_all(filtering_exp)
    return [user.get('email', '') for user in users]


def get_all_users(company_name: str) -> int:
    filter_exp = Attr('company').exists() & \
        Attr('company').eq(company_name) & Attr('registered').exists() & \
        Attr('registered').eq(True)
    users = get_all(filter_exp)
    return len(users)


def get_all_users_report(company_name: str, finish_date: str) -> int:
    company_name = company_name.lower()
    project_access = get_platform_users()
    project_users = {user.get('user_email') for user in project_access}
    filter_exp = Attr('date_joined').lte(finish_date) & \
        Attr('registered').eq(True) & Attr('company').ne(company_name)
    attribute = 'email'
    users = get_all(filter_exp, data_attr=attribute)
    users_mails = [user.get('email', '') for user in users]
    users_filtered = project_users.intersection(users_mails)
    return len(users_filtered)


def get_all(filter_exp: object, data_attr: str = '') -> List[Dict[str, str]]:
    table = DYNAMODB_RESOURCE.Table(TABLE)
    scan_attrs = {}
    scan_attrs['FilterExpression'] = filter_exp
    if data_attr:
        scan_attrs['ProjectionExpression'] = data_attr
    response = table.scan(**scan_attrs)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        scan_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = table.scan(**scan_attrs)
        items += response['Items']

    return items


def get_attributes(email: str, attributes: List[str]) -> UserType:
    table = DYNAMODB_RESOURCE.Table(TABLE)
    items = {}
    try:
        response = table.get_item(
            Key={'email': email},
            AttributesToGet=attributes
        )
        items = response.get('Item', {})
    except ClientError as ex:
        rollbar.report_message('Error: Unable to get user attributes',
                               'error', extra_data=ex, payload_data=locals())
    return items


def logging_users_report(company_name: str, init_date: str, finish_date: str) -> int:
    filter_exp = Attr('last_login').exists() & \
        Attr('last_login').lte(finish_date) & \
        Attr('last_login').gte(init_date) & \
        Attr('registered').exists() & Attr('registered').eq(True) & \
        Attr('company').exists() & Attr('company').ne(company_name.lower())
    users = get_all(filter_exp)
    return len(users)


def remove_attribute(email: str, name_attribute: str) -> bool:
    return update(email.lower(), {name_attribute: None})


def create(email: str, data: UserType) -> bool:
    resp = False
    table = DYNAMODB_RESOURCE.Table(TABLE)
    try:
        data.update({'email': email})
        response = table.put_item(Item=data)
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


def update(email: str, data: UserType) -> bool:
    success = False
    primary_key = {'email': email.lower()}
    table = DYNAMODB_RESOURCE.Table(TABLE)
    try:
        attrs_to_remove = [attr for attr in data if data[attr] is None]
        for attr in attrs_to_remove:
            response = table.update_item(
                Key=primary_key,
                UpdateExpression='REMOVE #attr',
                ExpressionAttributeNames={'#attr': attr}
            )
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
            del data[attr]

        if data:
            for attr in data:
                response = table.update_item(
                    Key=primary_key,
                    UpdateExpression='SET #attrName = :val1',
                    ExpressionAttributeNames={
                        '#attrName': attr
                    },
                    ExpressionAttributeValues={
                        ':val1': data[attr]
                    }
                )
                success = response['ResponseMetadata']['HTTPStatusCode'] == 200
                if not success:
                    break
    except ClientError as ex:
        rollbar.report_message('Error: Unable to update user',
                               'error', extra_data=ex, payload_data=locals())

    return success


def get(email: str) -> UserType:
    table = DYNAMODB_RESOURCE.Table(TABLE)
    response = table.get_item(Key={'email': email.lower()})
    return response.get('Item', {})


def delete(email: str) -> bool:
    table = DYNAMODB_RESOURCE.Table(TABLE)
    primary_keys = {'email': email.lower()}
    resp = False
    try:
        item = table.get_item(Key=primary_keys)
        if item.get('Item'):
            response = table.delete_item(Key=primary_keys)
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError as ex:
        rollbar.report_message('Error: Unable to delete user',
                               'error', extra_data=ex, payload_data=locals())
    return resp


def get_projects(user_email: str, active: bool) -> List[str]:
    """ Get projects of a user """
    filtering_exp = Key('user_email').eq(user_email.lower())
    response = ACCESS_TABLE.query(KeyConditionExpression=filtering_exp)
    projects = response['Items']
    while response.get('LastEvaluatedKey'):
        response = ACCESS_TABLE.query(
            KeyConditionExpression=filtering_exp,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        projects += response['Items']
    if active:
        projects_filtered = [project.get('project_name')
                             for project in projects
                             if project.get('has_access', '')]
    else:
        projects_filtered = [project.get('project_name')
                             for project in projects
                             if not project.get('has_access', '')]
    return projects_filtered


def get_platform_users() -> List[Dict[str, UserType]]:
    filter_exp = Attr('has_access').eq(True) \
        & Not(Attr('user_email').contains('@fluidattacks.com')) \
        & Not(Attr('project_name').is_in(FI_TEST_PROJECTS.split(',')))

    response = ACCESS_TABLE.scan(FilterExpression=filter_exp)
    users = response['Items']
    while response.get('LastEvaluatedKey'):
        response = ACCESS_TABLE.scan(
            FilterExpression=filter_exp,
            ExclusiveStartKey=response['LastEvaluatedKey'])
        users += response['Items']

    return users
