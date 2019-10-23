
from boto3.dynamodb.conditions import Attr
from app.dal import integrates_dal


TABLE = 'FI_users'


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


def get_project_access(email, project_name):
    return integrates_dal.get_project_access_dynamo(email, project_name)


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


def update_multiple_user_attributes(email, data_dict):
    primary_key = ['email', email.lower()]
    return integrates_dal.add_multiple_attributes_dynamo(
        TABLE, primary_key, data_dict)


def update_project_access(email, project_name, access):
    return integrates_dal.add_project_access_dynamo(
        email, project_name, 'has_access', access)


def update_user_attribute(email, data_attribute, name_attribute):
    primary_key = ['email', email.lower()]
    return integrates_dal.add_attribute_dynamo(
        TABLE, primary_key, name_attribute, data_attribute)


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
