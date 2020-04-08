# Standard library
import contextlib
from typing import Dict, List, NamedTuple

# Third party libraries
import rollbar
from boto3.dynamodb.conditions import Attr, Key, Not
from botocore.exceptions import ClientError
from backend.dal.helpers import dynamodb
from backend.typing import User as UserType

# Local libraries
from __init__ import FI_TEST_PROJECTS

# Shared resources
DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
ACCESS_TABLE = DYNAMODB_RESOURCE.Table('FI_project_access')
AUTHZ_TABLE = DYNAMODB_RESOURCE.Table('fi_authz')
USERS_TABLE = DYNAMODB_RESOURCE.Table('FI_users')

# Typing
SUBJECT_POLICY = NamedTuple('SUBJECT_POLICY', [
    # interface for a row in fi_authz
    ('level', str),
    ('subject', str),
    ('object', str),
    ('role', str),
])


def cast_subject_policy_into_dict(policy: SUBJECT_POLICY) -> dict:
    """Cast a subject policy into a dict, valid to be put in dynamo."""
    # pylint: disable=protected-access
    return {
        key: (
            value.lower()
            if isinstance(value, str)
            else value
        )
        for key, value in policy._asdict().items()
    }


def cast_dict_into_subject_policy(item: dict) -> SUBJECT_POLICY:
    # pylint: disable=protected-access
    field_types: dict = SUBJECT_POLICY._field_types

    # Every string as lowercase
    for field, _ in field_types.items():
        if isinstance(item.get(field), str):
            item[field] = item[field].lower()

    return SUBJECT_POLICY(**{
        field: (
            item[field]
            if field in item and isinstance(item[field], typing)
            else typing()
        )
        for field, typing in field_types.items()
    })


def get_subject_policy(subject: str, object_: str) -> SUBJECT_POLICY:
    """Return a policy for the given subject over the given object."""
    response = AUTHZ_TABLE.get_item(
        ConsistentRead=True,
        Key={
            'subject': subject.lower(),
            'object': object_.lower(),
        },
    )

    return cast_dict_into_subject_policy(response.get('Item', {}))


def get_subject_policies(subject: str) -> List[SUBJECT_POLICY]:
    """Return a list of policies for the given subject."""
    policies: List[SUBJECT_POLICY] = []
    query_params = {
        'ConsistentRead': True,
        'KeyConditionExpression': Key('subject').eq(subject.lower()),
    }

    response = AUTHZ_TABLE.query(**query_params)
    policies.extend(map(cast_dict_into_subject_policy, response['Items']))

    while 'LastEvaluatedKey' in response:
        query_params['ExclusiveStartKey'] = response['LastEvaluatedKey']

        response = AUTHZ_TABLE.query(**query_params)
        policies.extend(map(cast_dict_into_subject_policy, response['Items']))

    return policies


def put_subject_policy(policy: SUBJECT_POLICY) -> bool:
    item = cast_subject_policy_into_dict(policy)

    with contextlib.suppress(ClientError):
        response = AUTHZ_TABLE.put_item(Item=item)
        return response['ResponseMetadata']['HTTPStatusCode'] == 200

    rollbar.report_message(
        'Error in user_dal.put_subject_policy',
        level='error', payload_data=locals())

    return False


def delete_subject_policy(subject: str, object_: str) -> bool:
    with contextlib.suppress(ClientError):
        response = AUTHZ_TABLE.delete_item(Key={
            'subject': subject.lower(),
            'object': object_.lower(),
        })
        return response['ResponseMetadata']['HTTPStatusCode'] == 200

    rollbar.report_message(
        'Error in user_dal.delete_subject_policy',
        level='error', payload_data=locals())

    return False


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
    scan_attrs = {}
    scan_attrs['FilterExpression'] = filter_exp
    if data_attr:
        scan_attrs['ProjectionExpression'] = data_attr
    response = USERS_TABLE.scan(**scan_attrs)
    items = response['Items']
    while response.get('LastEvaluatedKey'):
        scan_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        response = USERS_TABLE.scan(**scan_attrs)
        items += response['Items']

    return items


def get_attributes(email: str, attributes: List[str]) -> UserType:
    items = {}
    try:
        response = USERS_TABLE.get_item(
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
    try:
        data.update({'email': email})
        response = USERS_TABLE.put_item(Item=data)
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


def update(email: str, data: UserType) -> bool:
    success = False
    primary_key = {'email': email.lower()}
    try:
        attrs_to_remove = [attr for attr in data if data[attr] is None]
        for attr in attrs_to_remove:
            response = USERS_TABLE.update_item(
                Key=primary_key,
                UpdateExpression='REMOVE #attr',
                ExpressionAttributeNames={'#attr': attr}
            )
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
            del data[attr]

        if data:
            for attr in data:
                response = USERS_TABLE.update_item(
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
    response = USERS_TABLE.get_item(Key={'email': email.lower()})
    return response.get('Item', {})


def delete(email: str) -> bool:
    primary_keys = {'email': email.lower()}
    resp = False
    try:
        item = USERS_TABLE.get_item(Key=primary_keys)
        if item.get('Item'):
            response = USERS_TABLE.delete_item(Key=primary_keys)
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
