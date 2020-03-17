from datetime import datetime
from typing import Dict, List, Union, cast
import pytz
from django.conf import settings
from backend.dal import project as project_dal, user as user_dal
from backend.typing import User as UserType
from backend.utils.validations import (
    validate_email_address, validate_alphanumeric_field, validate_phone_field
)


def add_phone_to_user(email: str, phone: str) -> bool:
    """ Update user phone number. """
    return user_dal.update(email, {'phone': phone})


def assign_role(email: str, role: str) -> bool:
    if role not in ('analyst', 'customer', 'admin', 'customeradmin'):
        resp = False
    else:
        resp = user_dal.update(email, {'role': role})
    return resp


def get_admins() -> List[str]:
    return user_dal.get_admins()


def get_all_companies() -> List[str]:
    return user_dal.get_all_companies()


def get_all_inactive_users(final_date: str) -> List[str]:
    return user_dal.get_all_inactive_users(final_date)


def get_all_users(company_name: str) -> int:
    return user_dal.get_all_users(company_name.lower())


def get_all_users_report(company_name: str, finish_date: str) -> int:
    return user_dal.get_all_users_report(company_name.lower(), finish_date)


def get_current_date() -> str:
    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
    return today


def get_data(email: str, attr: str) -> Union[str, UserType]:
    data_attr = get_attributes(email, [attr])
    if data_attr and data_attr.get(attr):
        return cast(UserType, data_attr.get(attr, ''))
    return str()


def get_projects(user_email: str, active: bool = True) -> List[str]:
    projects = user_dal.get_projects(user_email, active)
    projects = [project for project in projects
                if project_dal.is_request_deletion_user(project, user_email)]
    return projects


def get_project_access(email: str, project_name: str) -> bool:
    has_access_attr = project_dal.get_user_access(email, project_name)
    resp = False
    if has_access_attr and has_access_attr[0].get('has_access'):
        resp = True
    else:
        # User without project access
        pass
    return resp


def get_attributes(email: str, data: List[str]) -> UserType:
    """ Get attributes of a user. """
    return user_dal.get_attributes(email, data)


def is_registered(email: str) -> bool:
    is_registered_attr = get_attributes(email, ['registered'])
    registered = False
    if is_registered_attr and is_registered_attr.get('registered'):
        registered = True
    else:
        # User not found or registered attr is False
        pass
    return registered


def logging_users_report(company_name: str, init_date: str, finish_date: str) -> int:
    return user_dal.logging_users_report(company_name, init_date, finish_date)


def register(email: str) -> bool:
    return user_dal.update(email, {'registered': True})


def remove_access_token(email: str) -> bool:
    """ Remove access token attribute """
    return user_dal.remove_attribute(email, 'access_token')


def remove_user(email: str) -> bool:
    return user_dal.delete(email.lower())


def update_legal_remember(email: str, remember: bool) -> bool:
    """ Remember legal notice acceptance """
    return user_dal.update(email, {'legal_remember': remember})


def update_access_token(email: str, token_data: Dict[str, str]) -> bool:
    """ Update access token """
    access_token = {
        'iat': int(datetime.utcnow().timestamp()),
        'jti': token_data['jti_hashed'],
        'salt': token_data['salt']
    }
    return user_dal.update(email, {'access_token': access_token})


def update_last_login(email: str) -> bool:
    return user_dal.update(str(email), {'last_login': get_current_date()})


def update_project_access(email: str, project_name: str, access: bool) -> bool:
    return project_dal.add_access(email, project_name, 'has_access', access)


def update_multiple_user_attributes(email: str, data_dict: UserType) -> bool:
    return user_dal.update(email, data_dict)


def create(email: str, data: UserType) -> bool:
    return user_dal.create(email, data)


def update(email: str, data_attr: str, name_attr: str) -> bool:
    return user_dal.update(email, {name_attr: data_attr})


def get(email: str) -> UserType:
    return user_dal.get(email)


def create_without_project(user_data: UserType) -> bool:
    phone_number = ''
    success = False
    if (
        validate_alphanumeric_field(cast(List[str], user_data.get('organization', ''))) and
        validate_phone_field(str(user_data.get('phone_number', ''))) and
        validate_email_address(str(user_data.get('email', '')))
    ):
        if not get_data(str(user_data.get('email', '')), 'email'):
            user_data.update({'registered': True})
            if user_data.get('phone_number'):
                phone_number = str(user_data.get('phone_number', ''))
                del user_data['phone_number']
            success = create(
                str(user_data.get('email', '')).lower(), user_data)
    if success:
        if phone_number and phone_number[1:].isdigit():
            add_phone_to_user(str(user_data.get('email', '')).lower(), phone_number)

    return success
