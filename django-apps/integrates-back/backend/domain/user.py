from datetime import datetime
import pytz
from django.conf import settings
from backend.dal import project as project_dal, user as user_dal
from backend.utils.user import validate_email_address, validate_field, validate_phone_field


def add_phone_to_user(email, phone):
    """ Update user phone number. """
    return user_dal.update(email, {'phone': phone})


def assign_role(email, role):
    if role not in ('analyst', 'customer', 'admin', 'customeradmin'):
        resp = False
    else:
        resp = user_dal.update(email, {'role': role})
    return resp


def get_admins():
    return user_dal.get_admins()


def get_all_companies():
    return user_dal.get_all_companies()


def get_all_inactive_users(final_date):
    return user_dal.get_all_inactive_users(final_date)


def get_all_users(company_name):
    return user_dal.get_all_users(company_name.lower())


def get_all_users_report(company_name, finish_date):
    return user_dal.get_all_users_report(company_name.lower(), finish_date)


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


def get_projects(user_email, active=True):
    projects = user_dal.get_projects(user_email, active)
    projects = [project for project in projects
                if project_dal.is_request_deletion_user(project, user_email)]
    return projects


def get_project_access(email, project_name):
    has_access_attr = project_dal.get_user_access(email, project_name)
    resp = False
    if has_access_attr and has_access_attr[0].get('has_access'):
        resp = True
    else:
        # User without project access
        pass
    return resp


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


def logging_users_report(company_name, init_date, finish_date):
    return user_dal.logging_users_report(company_name, init_date, finish_date)


def register(email):
    return user_dal.update(email, {'registered': True})


def remove_access_token(email):
    """ Remove access token attribute """
    return user_dal.remove_user_attribute(email, 'access_token')


def remove_user(email):
    return user_dal.delete(email.lower())


def update_legal_remember(email, remember):
    """ Remember legal notice acceptance """
    return user_dal.update(email, {'legal_remember': remember})


def update_access_token(email, token_data):
    """ Update access token """
    access_token = {
        'iat': int(datetime.utcnow().timestamp()),
        'jti': token_data['jti_hashed'],
        'salt': token_data['salt']
    }
    return user_dal.update(email, {'access_token': access_token})


def update_last_login(email):
    return user_dal.update(str(email), {'last_login': get_current_date()})


def update_project_access(email, project_name, access):
    return project_dal.add_access(email, project_name, 'has_access', access)


def update_multiple_user_attributes(email, data_dict):
    return user_dal.update(email, data_dict)


def create(email, data):
    return user_dal.create(email, data)


def update(email, data_attr, name_attr):
    return user_dal.update(email, {name_attr: data_attr})


def create_without_project(user_data):
    phone_number = ''
    success = False
    if (
        validate_field(user_data.get('organization')) and
        validate_phone_field(user_data.get('phone_number', '')) and
        validate_email_address(user_data['email'])
    ):
        if not get_data(user_data['email'], 'email'):
            user_data.update({'registered': True})
            if user_data.get('phone_number'):
                phone_number = user_data.get('phone_number')
                del user_data['phone_number']
            success = create(
                user_data['email'].lower(), user_data)
    if success:
        if phone_number and phone_number[1:].isdigit():
            add_phone_to_user(user_data['email'].lower(), phone_number)

    return success
