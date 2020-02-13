
import rollbar
from boto3.dynamodb.conditions import Attr, Not
from botocore.exceptions import ClientError
from backend.dal import integrates_dal
from backend.dal.helpers import dynamodb

from __init__ import FI_TEST_PROJECTS

TABLE = 'FI_users'
DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE
ACCESS_TABLE = DYNAMODB_RESOURCE.Table('FI_project_access')


def get_admins():
    filter_exp = Attr('role').exists() & Attr('role').eq('admin')
    admins = integrates_dal.get_data_dynamo_filter(TABLE, filter_exp)
    return [user.get('email') for user in admins]


def get_all_companies():
    filter_exp = Attr('company').exists()
    users = integrates_dal.get_data_dynamo_filter(TABLE, filter_exp)
    companies = [user.get('company').strip().upper() for user in users]
    return list(set(companies))


def get_all_inactive_users(final_date):
    filtering_exp = Attr('registered').exists() & \
        Attr('registered').eq(False) & \
        (Attr('last_login').not_exists() |
         (Attr('last_login').exists() & Attr('last_login').lte(final_date)))
    users = integrates_dal.get_data_dynamo_filter(TABLE, filtering_exp)
    users_data = [user.get('email') for user in users]
    return users_data


def get_all_users(company_name):
    filter_exp = Attr('company').exists() & \
        Attr('company').eq(company_name) & Attr('registered').exists() & \
        Attr('registered').eq(True)
    users = integrates_dal.get_data_dynamo_filter(TABLE, filter_exp)
    return len(users)


def get_all_users_report(company_name, finish_date):
    filter_exp = Attr('has_access').exists() & Attr('has_access').eq(True)
    attribute = 'user_email'
    project_access = integrates_dal.get_data_dynamo_filter(
        'FI_project_access', filter_exp, data_attr=attribute)
    project_users = {user.get('user_email') for user in project_access}
    filter_exp = Attr('date_joined').lte(finish_date) & \
        Attr('registered').eq(True) & Attr('company').ne(company_name)
    attribute = 'email'
    users = integrates_dal.get_data_dynamo_filter(
        TABLE, filter_exp, data_attr=attribute)
    users = [user.get('email') for user in users]
    users_filtered = project_users.intersection(users)
    return len(users_filtered)


def get_user_attributes(email, data):
    primary_key = {'email': email.lower()}
    return integrates_dal.get_table_attributes_dynamo(
        TABLE, primary_key, data)


def logging_users_report(company_name, init_date, finish_date):
    filter_exp = Attr('last_login').exists() & \
        Attr('last_login').lte(finish_date) & \
        Attr('last_login').gte(init_date) & \
        Attr('registered').exists() & Attr('registered').eq(True) & \
        Attr('company').exists() & Attr('company').ne(company_name.lower())
    users = integrates_dal.get_data_dynamo_filter(TABLE, filter_exp)
    return len(users)


def remove_user(email):
    primary_keys = {'email': email.lower()}
    return integrates_dal.delete_item(TABLE, primary_keys)


def remove_user_attribute(email, name_attribute):
    primary_key = {'email': email.lower()}
    return integrates_dal.remove_attr_dynamo(
        TABLE, primary_key, name_attribute)


def create(email, data):
    resp = False
    table = DYNAMODB_RESOURCE.Table(TABLE)
    try:
        data.update({'email': email})
        response = table.put_item(Item=data)
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_exc_info()
    return resp


def update(email, data):
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
        rollbar.report_message('Error: Couldn\'nt update user',
                               'error', extra_data=ex, payload_data=locals())

    return success


def get_projects(user_email, active):
    """ Get projects of a user """
    projects = integrates_dal.get_data_dynamo(
        'FI_project_access', 'user_email', user_email.lower())
    if active:
        projects_filtered = [project.get('project_name')
                             for project in projects
                             if project.get('has_access', '')]
    else:
        projects_filtered = [project.get('project_name')
                             for project in projects
                             if not project.get('has_access', '')]
    return projects_filtered


def get_platform_users():
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
