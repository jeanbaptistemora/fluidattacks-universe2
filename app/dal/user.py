from __future__ import absolute_import
from app.dal import integrates_dal


TABLE = 'FI_users'


def get_user_attributes(email, data):
    primary_key = {'email': email}
    return integrates_dal.get_table_attributes_dynamo(
        TABLE, primary_key, data)


def update_user_attribute(email, data_attribute, name_attribute):
    primary_key = ['email', email]
    return integrates_dal.add_attribute_dynamo(
        TABLE, primary_key, name_attribute, data_attribute)
