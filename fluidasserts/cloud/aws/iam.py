# -*- coding: utf-8 -*-

"""AWS cloud checks (IAM)."""

# standard imports
from datetime import datetime, timedelta
import pytz

# 3rd party imports
from dateutil import parser
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, LOW, MEDIUM, HIGH
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


def _any_to_list(_input):
    """Convert anything to list."""
    if isinstance(_input, str):
        res = [_input]
    else:
        res = list(_input)
    return res


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_mfa_disabled(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Search users with password enabled and without MFA.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.credentials_report(key_id=key_id,
                                   secret=secret,
                                   retry=retry)

    msg_open: str = 'Users have password enabled with MFA'
    msg_closed: str = 'Users do not have password enabled or MFA'

    vulns, safes = [], []

    for user in users:
        user_arn = user['arn']
        user_has_mfa: bool = user['mfa_active'] == 'false'
        user_has_pass: bool = user['password_enabled'] == 'true'

        (vulns if user_has_pass and not user_has_mfa else safes).append(
            (user_arn, 'Must have MFA'))

    return _get_result_as_tuple(
        service='IAM', objects='users',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def have_old_creds_enabled(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Find password not used in the last 90 days.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.credentials_report(key_id=key_id,
                                   secret=secret,
                                   retry=retry)

    msg_open: str = 'Users have unused passwords (last 90 days)'
    msg_closed: str = 'Users do not have unused passwords (last 90 days)'

    vulns, safes = [], []

    three_months_ago = datetime.now() - timedelta(days=90)
    three_months_ago = three_months_ago.replace(tzinfo=pytz.UTC)

    client = aws.get_aws_client(service='iam',
                                key_id=key_id,
                                secret=secret)

    for user in users:
        if user['password_enabled'] != 'true':
            continue

        user_pass_last_used = \
            client.get_user(UserName=user['user'])['User']['PasswordLastUsed']

        (vulns if user_pass_last_used < three_months_ago else safes).append(
            (user['arn'], 'Must not have an unused password'))

    return _get_result_as_tuple(
        service='IAM', objects='users',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def have_old_access_keys(key_id: str, secret: str,
                         retry: bool = True) -> tuple:
    """
    Find access keys not rotated in the last 90 days.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.credentials_report(key_id=key_id,
                                   secret=secret,
                                   retry=retry)

    msg_open: str = ('User access keys have not been '
                     'rotated in the last 90 days')
    msg_closed: str = 'User access keys have been rotated in the last 90 days'

    vulns, safes = [], []

    three_months_ago = datetime.now() - timedelta(days=90)
    three_months_ago = three_months_ago.replace(tzinfo=pytz.UTC)

    for user in users:
        if any((user['access_key_1_active'] != 'true',
                user['access_key_2_active'] != 'true')):
            continue

        user_arn = user['arn']

        is_vulnerable: bool = any(
            parser.parse(user[x]).replace(tzinfo=pytz.UTC) < three_months_ago
            for x in ('access_key_1_last_rotated',
                      'access_key_2_last_rotated'))

        (vulns if is_vulnerable else safes).append(
            (user_arn, 'Keys must be rotated'))

    return _get_result_as_tuple(
        service='IAM', objects='users',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def root_has_access_keys(key_id: str, secret: str,
                         retry: bool = True) -> tuple:
    """
    Check if root account has access keys.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.credentials_report(key_id=key_id,
                                   secret=secret,
                                   retry=retry)

    msg_open: str = 'Root user has access keys'
    msg_closed: str = 'Root user does not have access keys'

    vulns, safes = [], []

    # Root user is always the first retrieved
    root_user = users[0]
    root_arn = root_user['arn']

    root_has_active_keys: bool = any((
        root_user['access_key_1_active'] == 'true',
        root_user['access_key_2_active'] == 'true'))

    (vulns if root_has_active_keys else safes).append(
        (root_arn, 'Must not have access keys'))

    return _get_result_as_tuple(
        service='IAM', objects='users',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_requires_uppercase(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if password policy requires uppercase letters.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policy = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='iam',
                                func='get_account_password_policy',
                                param='PasswordPolicy',
                                retry=retry)

    msg_open: str = 'Password policy does not require uppercase letters'
    msg_closed: str = 'Password policy requires uppercase letters'

    vulns, safes = [], []

    (vulns if not policy['RequireUppercaseCharacters'] else safes).append(
        ('Account/PasswordPolicy', 'Must require uppercase chars'))

    return _get_result_as_tuple(
        service='IAM', objects='password policies',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_requires_lowercase(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if password policy requires lowercase letters.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policy = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='iam',
                                func='get_account_password_policy',
                                param='PasswordPolicy',
                                retry=retry)

    msg_open: str = 'Password policy does not require lowercase letters'
    msg_closed: str = 'Password policy requires lowercase letters'

    vulns, safes = [], []

    (vulns if not policy['RequireLowercaseCharacters'] else safes).append(
        ('Account/PasswordPolicy', 'Must require lowercase chars'))

    return _get_result_as_tuple(
        service='IAM', objects='password policies',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_requires_symbols(key_id: str, secret: str,
                         retry: bool = True) -> tuple:
    """
    Check if password policy requires symbols.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policy = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='iam',
                                func='get_account_password_policy',
                                param='PasswordPolicy',
                                retry=retry)

    msg_open: str = 'Password policy does not require symbols'
    msg_closed: str = 'Password policy requires symbols'

    vulns, safes = [], []

    (vulns if not policy['RequireSymbols'] else safes).append(
        ('Account/PasswordPolicy', 'Must require symbols chars'))

    return _get_result_as_tuple(
        service='IAM', objects='password policies',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_requires_numbers(key_id: str, secret: str,
                         retry: bool = True) -> tuple:
    """
    Check if password policy requires numbers.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policy = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='iam',
                                func='get_account_password_policy',
                                param='PasswordPolicy',
                                retry=retry)

    msg_open: str = 'Password policy does not require numbers'
    msg_closed: str = 'Password policy requires numbers'

    vulns, safes = [], []

    (vulns if not policy['RequireNumbers'] else safes).append(
        ('Account/PasswordPolicy', 'Must require numeric chars'))

    return _get_result_as_tuple(
        service='IAM', objects='password policies',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def min_password_len_unsafe(
        key_id: str, secret: str, min_len=14, retry: bool = True) -> tuple:
    """
    Check if password policy requires passwords greater than 14 chars.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param min_len: Minimum length required. Default 14
    """
    policy = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='iam',
                                func='get_account_password_policy',
                                param='PasswordPolicy',
                                retry=retry)

    msg_open: str = 'Password policy does not require long enough passwords'
    msg_closed: str = 'Password policy requires long enough passwords'

    vulns, safes = [], []

    (vulns if policy['MinimumPasswordLength'] < min_len else safes).append(
        ('Account/PasswordPolicy/MinimumPasswordLength',
         f'Must be at least {min_len} chars long'))

    return _get_result_as_tuple(
        service='IAM', objects='password policies',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def password_reuse_unsafe(
        key_id: str, secret: str, min_reuse=24, retry: bool = True) -> tuple:
    """
    Check if password policy avoids reuse of the last 24 passwords.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param min_len: Minimum reuse required. Default 24
    """
    policy = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='iam',
                                func='get_account_password_policy',
                                param='PasswordPolicy',
                                retry=retry)

    msg_open: str = 'Password policy allows reusing passwords'
    msg_closed: str = 'Password policy avoids reusing passwords'

    vulns, safes = [], []

    password_reuse: int = policy.get('PasswordReusePrevention', 0)

    (vulns if password_reuse < min_reuse else safes).append(
        ('Account/PasswordPolicy/PasswordReusePrevention',
         f'Must be at least {min_reuse}'))

    return _get_result_as_tuple(
        service='IAM', objects='password policies',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def password_expiration_unsafe(
        key_id: str, secret: str, max_days=90, retry: bool = True) -> tuple:
    """
    Check if password policy expires the passwords within 90 days or less.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param max_days: Max expiration days. Default 90
    """
    policy = aws.run_boto3_func(key_id=key_id,
                                secret=secret,
                                service='iam',
                                func='get_account_password_policy',
                                param='PasswordPolicy',
                                retry=retry)

    msg_open: str = 'Password policy allows reusing passwords'
    msg_closed: str = 'Password policy avoids reusing passwords'

    vulns, safes = [], []

    pasword_max_age: int = policy.get('MaxPasswordAge', max_days + 1)

    (vulns if pasword_max_age > max_days else safes).append(
        ('Account/PasswordPolicy/MaxPasswordAge',
         f'Must be at less than {max_days} days'))

    return _get_result_as_tuple(
        service='IAM', objects='password policies',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def root_without_mfa(key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if root account does not have MFA.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    summary = aws.run_boto3_func(key_id=key_id,
                                 secret=secret,
                                 service='iam',
                                 func='get_account_summary',
                                 param='SummaryMap',
                                 retry=retry)

    msg_open: str = 'Root password has MFA disabled'
    msg_closed: str = 'Root password has MFA enabled'

    vulns, safes = [], []

    (vulns if summary['AccountMFAEnabled'] != 1 else safes).append(
        ('User:Root-Account', 'Must have MFA'))

    return _get_result_as_tuple(
        service='IAM', objects='password policies',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def policies_attached_to_users(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if there are policies attached to users.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.run_boto3_func(key_id=key_id,
                               secret=secret,
                               service='iam',
                               func='list_users',
                               param='Users',
                               retry=retry)

    msg_open: str = 'User has policies directly attached'
    msg_closed: str = 'User does not have policies directly attached'

    vulns, safes = [], []

    for user in users:
        user_arn = user['Arn']
        user_policies = aws.run_boto3_func(key_id=key_id,
                                           secret=secret,
                                           service='iam',
                                           func='list_attached_user_policies',
                                           param='AttachedPolicies',
                                           UserName=user['UserName'],
                                           retry=retry)
        (vulns if user_policies else safes).append(
            (user_arn, 'Must not have policies directly attached'))

    return _get_result_as_tuple(
        service='IAM', objects='users',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def have_full_access_policies(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if there are policies that allow full administrative privileges.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policies = aws.run_boto3_func(key_id=key_id,
                                  secret=secret,
                                  service='iam',
                                  func='list_policies',
                                  param='Policies',
                                  retry=retry)

    msg_open: str = 'Policies allow full administrative privileges'
    msg_closed: str = 'Policies does not allow full administrative privileges'

    vulns, safes = [], []

    for policy in policies:
        pol_arn = policy['Arn']
        pol_ver = aws.run_boto3_func(key_id=key_id,
                                     secret=secret,
                                     service='iam',
                                     func='get_policy_version',
                                     param='PolicyVersion',
                                     PolicyArn=policy['Arn'],
                                     VersionId=policy['DefaultVersionId'],
                                     retry=retry)

        pol_ver = list(pol_ver['Document']['Statement'])

        try:
            count = sum(x['Effect'] == 'Allow' and
                        '*' in _any_to_list(x['Action']) and
                        '*' in _any_to_list(x['Resource']) for x in pol_ver)
        except TypeError:
            count = 0

        (vulns if count > 0 else safes).append(
            (pol_arn, 'Must not allow full privileges'))

    return _get_result_as_tuple(
        service='IAM', objects='policies',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_not_support_role(key_id: str, secret: str,
                         retry: bool = True) -> tuple:
    """
    Check if there are a support role.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policies = aws.run_boto3_func(key_id=key_id,
                                  secret=secret,
                                  service='iam',
                                  func='list_policies',
                                  param='Policies',
                                  retry=retry)

    msg_open: str = \
        'There are not entities attached to the AWSSupportAccess policy'
    msg_closed: str = \
        'There are entities attached to the AWSSupportAccess policy'

    vulns, safes = [], []

    support_policies = [
        p for p in policies if p['PolicyName'] == 'AWSSupportAccess']

    for policy in support_policies:
        policy_arn = policy['Arn']

        entities = aws.run_boto3_func(key_id=key_id,
                                      secret=secret,
                                      service='iam',
                                      func='list_entities_for_policy',
                                      PolicyArn=policy_arn,
                                      retry=retry)

        attached_times = (
            len(list(filter(None, entities['PolicyUsers']))) +
            len(list(filter(None, entities['PolicyGroups']))) +
            len(list(filter(None, entities['PolicyRoles']))))

        (vulns if attached_times == 0 else safes).append(
            (policy_arn, 'Must have entities attached'))

    (safes if support_policies else vulns).append(
        ('Policies/AWSSupportAccess', 'Must be present'))

    return _get_result_as_tuple(
        service='IAM', objects='Support Access policies',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)
