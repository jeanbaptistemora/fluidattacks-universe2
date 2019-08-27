from __future__ import absolute_import
from django.db import connections
from app.dal import integrates_dal


TABLE = 'FI_users'


def get_role(email):
    """ Get the role of a user. """
    with connections['integrates'].cursor() as cursor:
        query = 'SELECT role FROM users WHERE email = %s'
        cursor.execute(query, (email,))
        row = cursor.fetchone()
    if row is None:
        return "None"
    return row[0]


def get_user_attributes(email, data):
    primary_key = {'email': email}
    return integrates_dal.get_table_attributes_dynamo(
        TABLE, primary_key, data)


def remove_user_attribute(email, name_attribute):
    primary_key = {'email': email}
    return integrates_dal.remove_attr_dynamo(
        TABLE, primary_key, name_attribute)


def update_user_attribute(email, data_attribute, name_attribute):
    primary_key = ['email', email]
    return integrates_dal.add_attribute_dynamo(
        TABLE, primary_key, name_attribute, data_attribute)
