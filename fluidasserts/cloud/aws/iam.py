# -*- coding: utf-8 -*-

"""AWS cloud checks (IAM)."""

# standard imports
from datetime import datetime, timedelta
import pytz

# 3rd party imports
from dateutil import parser

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import track, level, notify
from fluidasserts.helper import aws


def _any_to_list(_input):
    """Convert anything to list."""
    if isinstance(_input, str):
        res = [_input]
    else:
        res = list(_input)
    return res


@notify
@level('high')
@track
def has_mfa_disabled(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Search users with password enabled and without MFA.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        users = aws.get_credentials_report(key_id, secret, retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    for user in users:
        if user[3] == 'true':
            if user[7] == 'false':
                show_open('User has password enabled without MFA',
                          details=dict(user=user[0]))
                result = True
            else:
                show_close('User has password enabled with MFA',
                           details=dict(user=user[0]))
        else:
            show_close('User does not have password enabled',
                       details=dict(user=user[0]))
    return result


@notify
@level('medium')
@track
def have_old_creds_enabled(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Find password not used in the last 90 days.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        users = aws.get_credentials_report(key_id, secret, retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    for user in users:
        if user[3] == 'true':
            client = aws.get_aws_client('iam', key_id, secret)
            user_info = client.get_user(UserName=user[0])
            pass_last_used = user_info['User']['PasswordLastUsed']
            now_minus_90 = datetime.now() - timedelta(days=90)
            if pass_last_used < now_minus_90.replace(tzinfo=pytz.UTC):
                show_open('User has not used the password in more than \
90 days and it\'s still active',
                          details=dict(user=user[0],
                                       password_last_used=pass_last_used))
                result = True
            else:
                show_close('User has used the password in the last 90 days',
                           details=dict(user=user[0],
                                        password_last_used=pass_last_used))
    return result


@notify
@level('medium')
@track
def have_old_access_keys(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Find access keys not rotated in the last 90 days.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        users = aws.get_credentials_report(key_id, secret, retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    for user in users:
        if user[8] == 'true':
            ak_last_change = parser.parse(user[9]).replace(tzinfo=pytz.UTC)
            now_plus_90 = datetime.now() - timedelta(days=90)
            if ak_last_change < now_plus_90.replace(tzinfo=pytz.UTC):
                show_open('User\'s access key have not been rotated in \
the last 90 days',
                          details=dict(user=user[0],
                                       last_rotated=ak_last_change,
                                       expected_rotation_time=now_plus_90))
                result = True
            else:
                show_close('User\'s access key has been rotated in the last \
90 days', details=dict(user=user[0],
                       last_rotated=ak_last_change,
                       expected_rotation_time=now_plus_90))
        else:
            show_close('User does not have access keys enabled',
                       details=dict(user=user[0]))
    return result


@notify
@level('high')
@track
def root_has_access_keys(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if root account has access keys.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        users = aws.get_credentials_report(key_id, secret, retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    root_user = next(users)
    if root_user[8] == 'true' or root_user[13] == 'true':
        show_open('Root user has access keys', details=dict(user=root_user))
        result = True
    else:
        show_close('Root user does not have access keys',
                   details=dict(user=root_user))
        result = False
    return result


@notify
@level('high')
@track
def not_requires_uppercase(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if password policy requires uppercase letters.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        policy = aws.run_boto3_func(key_id, secret, 'iam',
                                    'get_account_password_policy',
                                    param='PasswordPolicy',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if policy['RequireUppercaseCharacters']:
        show_close('Password policy requires uppercase letters',
                   details=dict(policy=policy))
        result = False
    else:
        show_open('Password policy does not require uppercase letters',
                  details=dict(policy=policy))
        result = True
    return result


@notify
@level('high')
@track
def not_requires_lowercase(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if password policy requires lowercase letters.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        policy = aws.run_boto3_func(key_id, secret, 'iam',
                                    'get_account_password_policy',
                                    param='PasswordPolicy',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if policy['RequireLowercaseCharacters']:
        show_close('Password policy requires lowercase letters',
                   details=dict(policy=policy))
        result = False
    else:
        show_open('Password policy does not require lowercase letters',
                  details=dict(policy=policy))
        result = True
    return result


@notify
@level('high')
@track
def not_requires_symbols(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if password policy requires symbols.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        policy = aws.run_boto3_func(key_id, secret, 'iam',
                                    'get_account_password_policy',
                                    param='PasswordPolicy',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if policy['RequireSymbols']:
        show_close('Password policy requires symbols',
                   details=dict(policy=policy))
        result = False
    else:
        show_open('Password policy does not require symbols',
                  details=dict(policy=policy))
        result = True
    return result


@notify
@level('high')
@track
def not_requires_numbers(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if password policy requires numbers.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        policy = aws.run_boto3_func(key_id, secret, 'iam',
                                    'get_account_password_policy',
                                    param='PasswordPolicy',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if policy['RequireNumbers']:
        show_close('Password policy requires numbers',
                   details=dict(policy=policy))
        result = False
    else:
        show_open('Password policy does not require numbers',
                  details=dict(policy=policy))
        result = True
    return result


@notify
@level('high')
@track
def min_password_len_unsafe(
        key_id: str, secret: str, min_len=14, retry: bool = True) -> bool:
    """
    Check if password policy requires passwords greater than 14 chars.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param min_len: Mininum length required. Default 14
    """
    result = False
    try:
        policy = aws.run_boto3_func(key_id, secret, 'iam',
                                    'get_account_password_policy',
                                    param='PasswordPolicy',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if policy['MinimumPasswordLength'] >= min_len:
        show_close('Password policy requires long passwords',
                   details=dict(min_length=min_len, policy=policy))
        result = False
    else:
        show_open('Password policy does not require long passwords',
                  details=dict(min_length=min_len, policy=policy))
        result = True
    return result


@notify
@level('medium')
@track
def password_reuse_unsafe(
        key_id: str, secret: str, min_reuse=24, retry: bool = True) -> bool:
    """
    Check if password policy avoids reuse of the last 24 passwords.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param min_len: Mininum reuse required. Default 24
    """
    result = False
    try:
        policy = aws.run_boto3_func(key_id, secret, 'iam',
                                    'get_account_password_policy',
                                    param='PasswordPolicy',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if 'PasswordReusePrevention' in policy:
        if policy['PasswordReusePrevention'] >= min_reuse:
            show_close('Password policy avoid reusing passwords',
                       details=dict(min_reuse=min_reuse, policy=policy))
            result = False
        else:
            show_open('Password policy allows reusing passwords',
                      details=dict(min_reuse=min_reuse, policy=policy))
            result = True
    else:
        show_open('Password policy not contains reuse clause',
                  details=dict(policy=policy))
        result = True
    return result


@notify
@level('medium')
@track
def password_expiration_unsafe(
        key_id: str, secret: str, max_days=90, retry: bool = True) -> bool:
    """
    Check if password policy expires the passwords within 90 days or less.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param max_days: Max expiration days. Default 90
    """
    result = False
    try:
        policy = aws.run_boto3_func(key_id, secret, 'iam',
                                    'get_account_password_policy',
                                    param='PasswordPolicy',
                                    retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if 'MaxPasswordAge' in policy:
        if policy['MaxPasswordAge'] <= max_days:
            show_close('Password expiration policy is safe',
                       details=dict(max_days=max_days, policy=policy))
            result = False
        else:
            show_open('Password expiration policy is not safe',
                      details=dict(max_days=max_days, policy=policy))
            result = True
    else:
        show_open('Password policy not contains expiration clause',
                  details=dict(policy=policy))
        result = True
    return result


@notify
@level('high')
@track
def root_without_mfa(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if root account does not have MFA.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        summary = aws.run_boto3_func(key_id, secret, 'iam',
                                     'get_account_summary',
                                     param='SummaryMap',
                                     retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if summary['AccountMFAEnabled'] == 1:
        show_close('Root password has MFA enabled',
                   details=dict(account_summary=summary))
        result = False
    else:
        show_open('Root password has MFA disabled',
                  details=dict(account_summary=summary))
        result = True
    return result


@notify
@level('low')
@track
def policies_attached_to_users(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if there are policies attached to users.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        users = aws.run_boto3_func(key_id, secret, 'iam',
                                   'list_users',
                                   param='Users',
                                   retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    for user in users:
        user_pol = aws.run_boto3_func(key_id, secret, 'iam',
                                      'list_attached_user_policies',
                                      param='AttachedPolicies',
                                      retry=retry,
                                      UserName=user['UserName'])
        if user_pol:
            show_open('User has policies directly attached',
                      details=(dict(user=user['UserName'],
                                    user_policy=user_pol)))
            result = True
        else:
            show_close('User does not have policies attached',
                       details=(dict(user=user['UserName'])))
    return result


@notify
@level('medium')
@track
def have_full_access_policies(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if there are policies that allow full administrative privileges.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        policies = aws.run_boto3_func(key_id, secret, 'iam',
                                      'list_policies',
                                      param='Policies',
                                      retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    for policy in policies:
        pol_ver = aws.run_boto3_func(key_id, secret, 'iam',
                                     'get_policy_version',
                                     param='PolicyVersion',
                                     retry=retry,
                                     PolicyArn=policy['Arn'],
                                     VersionId=policy['DefaultVersionId'])
        pol_ver = list(pol_ver['Document']['Statement'])
        try:
            count = sum(x['Effect'] == 'Allow' and
                        '*' in _any_to_list(x['Action']) and
                        '*' in _any_to_list(x['Resource']) for x in pol_ver)
        except TypeError:
            count = 0
        if count:
            show_open('Policy allows full admin access',
                      details=(dict(policy=policy['PolicyName'],
                                    access=pol_ver)))
            result = True
        else:
            show_close('Policy avoid full admin access',
                       details=(dict(policy=policy['PolicyName'])))
    return result


@notify
@level('low')
@track
def has_not_support_role(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if there are a support role.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    result = False
    try:
        policies = aws.run_boto3_func(key_id, secret, 'iam',
                                      'list_policies',
                                      param='Policies',
                                      retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    policies = list(filter(lambda x: x['PolicyName'] == 'AWSSupportAccess',
                           policies))
    if not policies:
        show_open('There is not a AWSSupportAccess policy')
        return True

    for policy in policies:
        entities = aws.run_boto3_func(key_id, secret, 'iam',
                                      'list_entities_for_policy',
                                      retry=retry,
                                      PolicyArn=policy['Arn'])
        attached_users = len(list(filter(None, entities['PolicyUsers'])))
        attached_groups = len(list(filter(None, entities['PolicyGroups'])))
        attached_roles = len(list(filter(None, entities['PolicyRoles'])))

        total = attached_groups + attached_roles + attached_users

        if total:
            show_close('There are entities attached to support policy',
                       details=dict(policy=policy['PolicyName'],
                                    entities=entities))
        else:
            show_open('There are not entities attached to support policy',
                      details=dict(policy=policy['PolicyName'],
                                   entities=entities))
    return result
