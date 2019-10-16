from __future__ import absolute_import
from app.dal import integrates_dal


TABLE = 'FI_users'


def get_project_access(email, project_name):
    return integrates_dal.get_project_access_dynamo(email, project_name)


def get_user_attributes(email, data):
    primary_key = {'email': email.lower()}
    return integrates_dal.get_table_attributes_dynamo(
        TABLE, primary_key, data)


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
