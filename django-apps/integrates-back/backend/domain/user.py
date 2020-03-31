from datetime import datetime
from typing import Dict, List, Union, cast, Set
import pytz
from django.conf import settings
from backend.dal import project as project_dal, user as user_dal
from backend.typing import User as UserType
from backend.utils.validations import (
    validate_email_address, validate_alphanumeric_field, validate_phone_field
)
from backend.utils import (
    authorization as authorization_util
)
VALID_ROLES: Set[str] = {'analyst', 'customer', 'customeradmin', 'admin'}


def get_user_level_role(email: str) -> str:
    # level, subject, object, role
    rule = ['user', email, 'self']

    # List of List[level, subject, object, role]
    matching_rules: List[List[str]] = \
        settings.CASBIN_ADAPTER.get_rules('p', 'p', rule)

    if matching_rules:
        return matching_rules[0][3]
    return str()


def get_group_level_role(email: str, group: str) -> str:
    # level, subject, object, role
    rule = ['group', email, group.lower()]

    # Admins are granted access to all groups
    if get_user_level_role(email) == 'admin':
        return 'admin'

    # List of List[level, subject, object, role]
    matching_rules: List[List[str]] = \
        settings.CASBIN_ADAPTER.get_rules('p', 'p', rule)

    if matching_rules:
        return matching_rules[0][3]
    return str()


def grant_user_level_role(
        email: str,
        role: str,
        revoke_existing: bool = True,
        reload: bool = True) -> bool:
    if role not in VALID_ROLES:
        return False

    # level, subject, object, role
    rule = ['user', email, 'self']

    # Revoke previous user-level policies
    if revoke_existing:
        settings.CASBIN_ADAPTER.remove_policy('p', 'p', rule)

    rule.append(role)

    # Grant new user-level policy
    settings.CASBIN_ADAPTER.add_policy('p', 'p', rule)

    # Reload config
    if reload:
        authorization_util.revoke_cached_subject_policies(email)
        settings.ENFORCER_USER_LEVEL.load_policy()
        settings.ENFORCER_USER_LEVEL_ASYNC.load_policy()

    return True


def grant_group_level_role(
        email: str,
        group: str,
        role: str,
        revoke_existing: bool = True,
        reload: bool = True) -> bool:
    if role not in VALID_ROLES:
        return False

    # level, subject, object, role
    rule = ['group', email, group.lower()]

    # Revoke previous user-level policies
    if revoke_existing:
        settings.CASBIN_ADAPTER.remove_policy('p', 'p', rule)

    rule.append(role)

    # Grant new user-level policy
    settings.CASBIN_ADAPTER.add_policy('p', 'p', rule)

    # Reload config
    if reload:
        authorization_util.revoke_cached_subject_policies(email)
        settings.ENFORCER_GROUP_LEVEL.load_policy()
        settings.ENFORCER_GROUP_LEVEL_ASYNC.load_policy()

    return True


def revoke_user_level_role(email: str) -> bool:
    # level, subject, object, role
    rule = ['user', email, 'self']

    # Revoke previous user-level policies
    settings.CASBIN_ADAPTER.remove_policy('p', 'p', rule)

    # Reload config
    settings.ENFORCER_USER_LEVEL.load_policy()
    settings.ENFORCER_USER_LEVEL_ASYNC.load_policy()

    return True


def revoke_group_level_role(email: str, group: str) -> bool:
    # level, subject, object, role
    rule = ['group', email, group.lower()]

    # Revoke previous group-level policies
    settings.CASBIN_ADAPTER.remove_policy('p', 'p', rule)

    # Reload config
    authorization_util.revoke_cached_subject_policies(email)
    settings.ENFORCER_GROUP_LEVEL.load_policy()
    settings.ENFORCER_GROUP_LEVEL_ASYNC.load_policy()

    return True


def revoke_all_levels_roles(email: str, reload: bool = True) -> bool:
    # level, subject, object, role
    group_level_rule = ['group', email]
    user_level_rule = ['user', email]

    # Revoke policies
    settings.CASBIN_ADAPTER.remove_policy('p', 'p', group_level_rule)
    settings.CASBIN_ADAPTER.remove_policy('p', 'p', user_level_rule)

    # Reload config
    if reload:
        authorization_util.revoke_cached_subject_policies(email)
        settings.ENFORCER_USER_LEVEL.load_policy()
        settings.ENFORCER_USER_LEVEL_ASYNC.load_policy()
        settings.ENFORCER_GROUP_LEVEL.load_policy()
        settings.ENFORCER_GROUP_LEVEL_ASYNC.load_policy()

    return True


def add_phone_to_user(email: str, phone: str) -> bool:
    """ Update user phone number. """
    return user_dal.update(email, {'phone': phone})


def assign_role(email: str, role: str, group: str = None) -> bool:
    if role not in ('analyst', 'customer', 'admin', 'customeradmin'):
        return False

    if group:
        return grant_group_level_role(email, group, role)
    return grant_user_level_role(email, role)


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
    if data_attr and attr in data_attr:
        return cast(UserType, data_attr[attr])
    return str()


def get_projects(user_email: str, active: bool = True) -> List[str]:
    projects = user_dal.get_projects(user_email, active)
    projects = [project for project in projects
                if project_dal.is_request_deletion_user(project, user_email)]
    return projects


def get_group_access(email: str, group: str) -> bool:
    group_level_role = get_group_level_role(email, group)
    return bool(group_level_role)


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
    email: str = str(user_data.get('email', '')).lower()
    organization: str = str(user_data.get('organization', ''))
    phone_number: str = str(user_data.get('phone_number', ''))
    role: str = str(user_data.get('role', ''))

    success = False

    if validate_alphanumeric_field([organization]) \
            and validate_phone_field(phone_number) \
            and validate_email_address(email):

        new_user_data: UserType = {}
        new_user_data['email'] = email
        new_user_data['registered'] = True
        new_user_data['organization'] = organization
        new_user_data['phone'] = phone_number

        success = grant_user_level_role(email, role)
        success = success and create(email, new_user_data)

    return success
