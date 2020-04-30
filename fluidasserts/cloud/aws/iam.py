# -*- coding: utf-8 -*-
# pylint: disable=too-many-lines
"""AWS cloud checks (IAM)."""

# standard imports
from datetime import datetime, timedelta
from contextlib import suppress
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
def has_mfa_disabled(key_id: str,
                     secret: str,
                     session_token: str = None,
                     retry: bool = True) -> tuple:
    """
    Search users with password enabled and without MFA.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.credentials_report(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
        service='IAM',
        objects='users',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def have_old_creds_enabled(key_id: str,
                           secret: str,
                           session_token: str = None,
                           retry: bool = True) -> tuple:
    """
    Find password not used in the last 90 days.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.credentials_report(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        retry=retry)

    msg_open: str = 'Users have unused passwords (last 90 days)'
    msg_closed: str = 'Users do not have unused passwords (last 90 days)'

    vulns, safes = [], []

    three_months_ago = datetime.now() - timedelta(days=90)
    three_months_ago = three_months_ago.replace(tzinfo=pytz.UTC)

    client = aws.get_aws_client(service='iam', key_id=key_id, secret=secret)

    for user in users:
        if user['password_enabled'] != 'true':
            continue
        try:
            user_pass_last_used = aws.client_get_user(
                client, user['user'])['User']['PasswordLastUsed']
            vulnerable = user_pass_last_used < three_months_ago
        except KeyError:
            vulnerable = False

        (vulns if vulnerable else safes).append(
            (user['arn'], 'Must not have an unused password'))

    return _get_result_as_tuple(
        service='IAM',
        objects='users',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def have_old_access_keys(key_id: str,
                         secret: str,
                         session_token: str = None,
                         retry: bool = True) -> tuple:
    """
    Find access keys not rotated in the last 90 days.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.credentials_report(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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

        (vulns if is_vulnerable else safes).append((user_arn,
                                                    'Keys must be rotated'))

    return _get_result_as_tuple(
        service='IAM',
        objects='users',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def root_has_access_keys(key_id: str,
                         secret: str,
                         session_token: str = None,
                         retry: bool = True) -> tuple:
    """
    Check if root account has access keys.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.credentials_report(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        retry=retry)

    msg_open: str = 'Root user has access keys'
    msg_closed: str = 'Root user does not have access keys'

    vulns, safes = [], []

    # Root user is always the first retrieved
    root_user = users[0]
    root_arn = root_user['arn']

    root_has_active_keys: bool = any(
        (root_user['access_key_1_active'] == 'true',
         root_user['access_key_2_active'] == 'true'))

    (vulns if root_has_active_keys else safes).append(
        (root_arn, 'Must not have access keys'))

    return _get_result_as_tuple(
        service='IAM',
        objects='users',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_requires_uppercase(key_id: str,
                           secret: str,
                           session_token: str = None,
                           retry: bool = True) -> tuple:
    """
    Check if password policy requires uppercase letters.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policy = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
        service='IAM',
        objects='password policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_requires_lowercase(key_id: str,
                           secret: str,
                           session_token: str = None,
                           retry: bool = True) -> tuple:
    """
    Check if password policy requires lowercase letters.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policy = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
        service='IAM',
        objects='password policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_requires_symbols(key_id: str,
                         secret: str,
                         session_token: str = None,
                         retry: bool = True) -> tuple:
    """
    Check if password policy requires symbols.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policy = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
        service='IAM',
        objects='password policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_requires_numbers(key_id: str,
                         secret: str,
                         session_token: str = None,
                         retry: bool = True) -> tuple:
    """
    Check if password policy requires numbers.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policy = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
        service='IAM',
        objects='password policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def min_password_len_unsafe(key_id: str,
                            secret: str,
                            session_token: str = None,
                            min_len=14,
                            retry: bool = True) -> tuple:
    """
    Check if password policy requires passwords greater than 14 chars.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param min_len: Minimum length required. Default 14
    """
    policy = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
        service='IAM',
        objects='password policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def password_reuse_unsafe(key_id: str,
                          secret: str,
                          session_token: str = None,
                          min_reuse=24,
                          retry: bool = True) -> tuple:
    """
    Check if password policy avoids reuse of the last 24 passwords.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param min_len: Minimum reuse required. Default 24
    """
    policy = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
        service='IAM',
        objects='password policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def password_expiration_unsafe(key_id: str,
                               secret: str,
                               session_token: str = None,
                               max_days=90,
                               retry: bool = True) -> tuple:
    """
    Check if password policy expires the passwords within 90 days or less.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    :param max_days: Max expiration days. Default 90
    """
    policy = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
        service='IAM',
        objects='password policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def root_without_mfa(key_id: str,
                     secret: str,
                     session_token: str = None,
                     retry: bool = True) -> tuple:
    """
    Check if root account does not have MFA.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    summary = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
        service='IAM',
        objects='password policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def policies_attached_to_users(key_id: str,
                               secret: str,
                               session_token: str = None,
                               retry: bool = True) -> tuple:
    """
    Check if there are policies attached to users.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='iam',
        func='list_users',
        param='Users',
        retry=retry)

    msg_open: str = 'User has policies directly attached'
    msg_closed: str = 'User does not have policies directly attached'

    vulns, safes = [], []

    for user in users:
        user_arn = user['Arn']
        user_policies = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='list_attached_user_policies',
            param='AttachedPolicies',
            UserName=user['UserName'],
            retry=retry)
        (vulns if user_policies else safes).append(
            (user_arn, 'Must not have policies directly attached'))

    return _get_result_as_tuple(
        service='IAM',
        objects='users',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def have_full_access_policies(key_id: str,
                              secret: str,
                              session_token: str = None,
                              retry: bool = True) -> tuple:
    """
    Check if there are policies that allow full administrative privileges.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policies = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='iam',
        func='list_policies',
        param='Policies',
        retry=retry,
        Scope='Local',
        OnlyAttached=True)

    msg_open: str = 'Policies allow full administrative privileges'
    msg_closed: str = 'Policies does not allow full administrative privileges'

    vulns, safes = [], []

    for policy in policies:
        pol_arn = policy['Arn']
        pol_ver = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='get_policy_version',
            param='PolicyVersion',
            PolicyArn=policy['Arn'],
            VersionId=policy['DefaultVersionId'],
            retry=retry)

        pol_ver = list(pol_ver['Document']['Statement'])

        try:
            count = sum(
                x['Effect'] == 'Allow' and '*' in _any_to_list(x['Action'])
                and '*' in _any_to_list(x['Resource']) for x in pol_ver)
        except TypeError:
            count = 0

        (vulns if count > 0 else safes).append(
            (pol_arn, 'Must not allow full privileges'))

    return _get_result_as_tuple(
        service='IAM',
        objects='policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_not_support_role(key_id: str,
                         secret: str,
                         session_token: str = None,
                         retry: bool = True) -> tuple:
    """
    Check if there is a support role.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policies = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
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
        p for p in policies
        if p['PolicyName'] == 'AWSSupportAccess' and p['AttachmentCount'] > 0
    ]

    for policy in support_policies:
        policy_arn = policy['Arn']

        entities = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='list_entities_for_policy',
            PolicyArn=policy_arn,
            retry=retry)

        attached_times = (len(list(filter(None, entities['PolicyUsers']))) +
                          len(list(filter(None, entities['PolicyGroups']))) +
                          len(list(filter(None, entities['PolicyRoles']))))

        (vulns if attached_times == 0 else safes).append(
            (policy_arn, 'Must have entities attached'))

    (safes if support_policies else vulns).append(('Policies/AWSSupportAccess',
                                                   'Must be present'))

    return _get_result_as_tuple(
        service='IAM',
        objects='Support Access policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(
    risk=MEDIUM,
    kind=DAST,
    standards={
        'CWE': '250',
    },
)
@unknown_if(BotoCoreError, RequestException)
def has_permissive_role_policies(key_id: str,
                                 secret: str,
                                 session_token: str = None,
                                 retry: bool = True) -> tuple:
    """
    Check if an IAM Role Policy grants wildcard privileges.

    See https://cwe.mitre.org/data/definitions/250.html

    See `IAM Best Practices <https://docs.aws.amazon.com/IAM/latest/UserGuide/
      best-practices.html#grant-least-privilege>`_

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    roles = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='iam',
        func='list_roles',
        param='Roles',
        retry=retry)

    msg_open: str = ('IAM role policies violate the '
                     'principle of least privilege')
    msg_closed: str = ('IAM role policies comply with '
                       'the principle of least privilege')

    vulns, safes = [], []

    def get_role_policies(role_name):
        return aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='list_role_policies',
            param='PolicyNames',
            retry=retry,
            RoleName=role_name,
        )

    def get_policy_role(policy_name, role_name):
        return aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='get_role_policy',
            param='PolicyDocument',
            retry=retry,
            PolicyName=policy_name,
            RoleName=role_name)

    for role in roles:
        role_policies = get_role_policies(role['RoleName'])
        for policy_name in role_policies:
            for statement in get_policy_role(policy_name,
                                             role['RoleName'])['Statement']:
                (vulns if statement['Action'] == '*'
                 and statement['Effect'] == 'Allow' else safes).append(
                     (role['Arn'], 'IAM Role Policy Too Permissive'))

    return _get_result_as_tuple(
        service='IAM',
        objects='Policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_root_active_signing_certificates(key_id: str,
                                         secret: str,
                                         session_token: str = None,
                                         retry: bool = True) -> tuple:
    """
    Check if user root has activated signing certificates.

    To comply with the best security practices, make sure that the root user
    is not using X.590 certificates to make requests through the SOAP protocol
    to AWS. Disable any x.590 certificate for the root user, since it is used
    for daily tasks it is not a recommended practice.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.credentials_report(key_id,
                                   secret,
                                   boto3_client_kwargs={
                                       'aws_session_token': session_token},
                                   retry=retry)

    msg_open: str = 'Root user has activated signing certificates'
    msg_closed: str = 'Root user does not have activated signing certificates'

    vulns, safes = [], []

    # Root user is always the first retrieved
    root_user = users[0]
    root_arn = root_user['arn']

    root_has_active_signing_certs: bool = any(
        (root_user['cert_1_active'] == 'true',
         root_user['cert_2_active'] == 'true'))

    (vulns if root_has_active_signing_certs else safes).append(
        (root_arn, 'Must not have activate signing certificates'))

    return _get_result_as_tuple(
        service='IAM',
        objects='Credentials',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def users_with_password_and_access_keys(key_id: str,
                                        secret: str,
                                        session_token: str = None,
                                        retry: bool = True) -> tuple:
    """
    Check if there are users with password and access keys activated.

    Make sure your IAM users do not access the API and console with the
    same account, in order to reduce the risk of unauthorized access in case
    the access keys or passwords are compromised.

    See https://nvd.nist.gov/800-53/Rev4/control/AC-5

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    vulns, safes = [], []

    msg_open: str = ('Users have access keys and password '
                     'assigned for authentication.')
    msg_closed: str = ('Users have only keys or password '
                       'assigned for authentication, but not both.')

    users = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='iam',
        func='list_users',
        param='Users',
        retry=retry)

    client = aws.get_aws_client('iam', key_id, secret)

    for user in users:
        access_keys = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='list_access_keys',
            param='AccessKeyMetadata',
            retry=retry,
            UserName=user['UserName'])
        access_keys_activated: bool = any(
            map(lambda x: x['Status'], access_keys))

        login_profile = None
        with suppress(client.exceptions.NoSuchEntityException):
            login_profile = aws.client_get_login_profile(
                client, user['UserName'])

        (vulns if access_keys_activated and login_profile is not None else
         safes).append(
             (user['Arn'],
              'User must have only password or access keys, but not both.'))

    return _get_result_as_tuple(
        service='IAM',
        objects='Users',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def group_with_inline_policies(key_id: str,
                               secret: str,
                               session_token: str = None,
                               retry: bool = True) -> tuple:
    """
    Check if IAM groups have any inline policies attached.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are groups with inline policies attached.
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'IAM groups with inline policies attached.'
    msg_closed: str = ' IAM groups are using managed policies.'
    vulns, safes = [], []

    groups = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='iam',
        func='list_groups',
        param='Groups',
        retry=retry)

    for group in groups:
        group_policies = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='list_group_policies',
            GroupName=group['GroupName'],
            param='PolicyNames',
            retry=retry)
        (vulns if group_policies else safes).append(
            (group['Arn'],
             'Replace any inline policies with managed policies.'))

        return _get_result_as_tuple(
            service='IAM',
            objects='Groups',
            msg_open=msg_open,
            msg_closed=msg_closed,
            vulns=vulns,
            safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def mfa_disabled_for_users_with_console_password(key_id: str,
                                                 secret: str,
                                                 session_token: str = None,
                                                 retry: bool = True) -> tuple:
    """
    Check if IAM Users with console password are not protected by MFA.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` .
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Users with console password are not protected by MFA.'
    msg_closed: str = 'Users with console password are protected by MFA.'
    vulns, safes = [], []

    users = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='iam',
        func='list_users',
        param='Users',
        retry=retry)

    for user in users:
        try:
            aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={'aws_session_token': session_token},
                service='iam',
                func='get_login_profile',
                UserName=user['UserName'],
                param='LoginProfile',
                retry=retry,
                retry_times=3)
        except aws.ClientErr:
            continue

        mfa_devices = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='list_mfa_devices',
            UserName=user['UserName'],
            param='MFADevices',
            retry=retry)
        (vulns if not mfa_devices else safes).append(
            (user['Arn'], 'Enable MFA access protection for IAM user.'))

    return _get_result_as_tuple(
        service='IAM',
        objects='Users',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_old_ssh_public_keys(key_id: str,
                            secret: str,
                            session_token: str = None,
                            retry: bool = True) -> tuple:
    """
    Find IAM users keep any outdated (older than 90 days) SSH public keys.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are users with outdated SSH public keys.
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'There are users with old SSH public keys (older than 90 days).'
    msg_closed: str = 'Users have updated SSH public keys.'
    vulns, safes = [], []

    three_months_ago = datetime.now() - timedelta(days=90)
    three_months_ago = three_months_ago.replace(tzinfo=pytz.UTC)

    users = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='iam',
        func='list_users',
        param='Users',
        retry=retry)
    for user in users:
        keys = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='list_ssh_public_keys',
            UserName=user['UserName'],
            param='SSHPublicKeys',
            retry=retry)

        vulnerable = any(
            map(lambda x: x['UploadDate'] < three_months_ago, keys))
        (vulns if vulnerable else safes).append(
            (user['Arn'], 'Update old SSH public keys.'))

    return _get_result_as_tuple(
        service='IAM',
        objects='Users',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_wildcard_resource_on_write_action(key_id: str,
                                          secret: str,
                                          session_token: str = None,
                                          retry: bool = True) -> tuple:
    """
    Check if write actions are allowed on all resources.

    Do not allow ``"Resource": "*"`` to have write actions.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are IAM polices with wildcard resource in
                write actions.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`

    """
    msg_open = 'Write actions are allowed for all resources.'
    msg_closed = 'Write actions are not allowed for all resources.'
    vulns, safes = [], []

    policies = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='iam',
        func='list_policies',
        retry=retry,
        Scope='Local',
        OnlyAttached=True)['Policies']

    for policy in policies:
        policy_version = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='get_policy_version',
            param='PolicyVersion',
            PolicyArn=policy['Arn'],
            VersionId=policy['DefaultVersionId'],
            retry=retry)
        vulnerable = aws.policy_statement_privilege(
            policy_version['Document']['Statement'], 'Allow', 'write')

        (vulns if vulnerable else safes).append(
            (policy['Arn'],
             'access to only the necessary resources should be allowed.'))

    return _get_result_as_tuple(
        service='IAM',
        objects='Policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_privileges_over_iam(key_id: str,
                            secret: str,
                            session_token: str = None,
                            retry: bool = True) -> tuple:
    """
    Check if a policy documents has privileges over iam.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if any policy documents has privileges over iam.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`

    """
    msg_open = 'Policies have privileges over iam.'
    msg_closed = 'Policies have no privileges over iam.'
    vulns, safes = [], []
    policies = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='iam',
        func='list_policies',
        Scope='Local',
        OnlyAttached=True)['Policies']

    for policy in policies:
        policy_version = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='get_policy_version',
            param='PolicyVersion',
            PolicyArn=policy['Arn'],
            VersionId=policy['DefaultVersionId'],
            retry=retry)

        vulnerable = aws.service_is_present_statement(
            policy_version['Document']['Statement'], 'Allow', 'iam')
        (vulns if vulnerable else safes).append((policy['Arn'],
                                                 'has privileges over iam.'))
    return _get_result_as_tuple(
        service='IAM',
        objects='Policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def users_with_multiple_access_keys(key_id: str,
                                    secret: str,
                                    session_token: str = None,
                                    retry: bool = True) -> tuple:
    """
    Check if there are users with multiple access keys.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are users with multiple access keys.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns, safes = [], []

    msg_open: str = 'Users have multiple access keys.'
    msg_closed: str = 'Users have only one access keys.'

    users = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='iam',
        func='list_users',
        param='Users',
        retry=retry)

    for user in users:
        access_keys = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={'aws_session_token': session_token},
            service='iam',
            func='list_access_keys',
            param='AccessKeyMetadata',
            retry=retry,
            UserName=user['UserName'])
        access_keys_activated = list(
            filter(lambda y: y == 'Active',
                   list(map(lambda x: x['Status'], access_keys))))

        (vulns if len(access_keys_activated) > 1 else safes).append(
            (user['Arn'], 'user must have only one access key.'))

    return _get_result_as_tuple(
        service='IAM',
        objects='Users',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_full_access_to_ssm(key_id: str,
                           secret: str,
                           session_token: str = None,
                           retry: bool = True,
                           **boto3_kwargs):
    """
    Check if there are policy documents that allow full access to ssm agent.

    SSM allows everyone with access to run commands as root on EC2 instances

    https://cloudonaut.io/aws-ssm-is-a-trojan-horse-fix-it-now/

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are policy documents that allow full
                access to ssm.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open = 'Policies have privileges over iam.'
    msg_closed = 'Policies have no privileges over iam.'
    vulns, safes = [], []
    policies = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={
            'aws_session_token': session_token, **boto3_kwargs},
        service='iam',
        func='list_policies',
        Scope='Local',
        OnlyAttached=True)['Policies']

    for policy in policies:
        policy_version = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={
                'aws_session_token': session_token, **boto3_kwargs},
            service='iam',
            func='get_policy_version',
            param='PolicyVersion',
            PolicyArn=policy['Arn'],
            VersionId=policy['DefaultVersionId'],
            retry=retry)

        for sts in aws.force_list(policy_version['Document']['Statement']):
            vulnerable = sts['Effect'] == 'Allow' and 'Resource' in sts and \
                aws.resource_all(sts['Resource']) and 'ssm:*' in sts['Action']
            (vulns if vulnerable else safes).append(
                (policy['Arn'], 'has full access over ssm agent'))
    return _get_result_as_tuple(
        service='IAM',
        objects='Policies',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
