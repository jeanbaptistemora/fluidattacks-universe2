from datetime import datetime
import pytz
from django.conf import settings
from app.dal import user as user_dal


def add_phone_to_user(email, phone):
    """ Update user phone number. """
    return user_dal.update_user_attribute(email, phone, 'phone')


def get_current_date():
    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    return today


def get_data(email, attr):
    data_attr = get_user_attributes(email, [attr])
    data = ''
    if data_attr and data_attr.get(attr):
        data = data_attr.get(attr)
    else:
        # User not found or without attribute
        pass
    return data


def get_role(email):
    """ Get the role of a user. """
    return user_dal.get_role(email)


def get_user_attributes(email, data):
    """ Get attributes of a user. """
    return user_dal.get_user_attributes(email, data)


def is_registered(email):
    is_registered_attr = get_user_attributes(email, ['registered'])
    registered = False
    if is_registered_attr and is_registered_attr.get('registered'):
        registered = True
    else:
        # User not found or registered attr is False
        pass
    return registered


def register(email):
    return user_dal.update_user_attribute(email, True, 'registered')


def remove_access_token(email):
    """ Remove access token attribute """
    return user_dal.remove_user_attribute(email, 'access_token')


def update_legal_remember(email, remember):
    """ Remember legal notice acceptance """
    return user_dal.update_user_attribute(email, remember, 'legal_remember')


def update_access_token(email, token_data):
    """ Update access token """
    access_token = {
        'jti': token_data['jti_hashed'],
        'salt': token_data['salt']
    }
    return user_dal.update_user_attribute(email, access_token, 'access_token')


def update_last_login(email):
    return update_user_attribute(str(email), get_current_date(), 'last_login')


def update_multiple_user_attributes(email, data_dict):
    return user_dal.update_multiple_user_attributes(email, data_dict)


def update_user_attribute(email, data_attr, name_attr):
    return user_dal.update_user_attribute(email, data_attr, name_attr)
