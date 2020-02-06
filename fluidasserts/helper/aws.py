# -*- coding: utf-8 -*-

"""AWS cloud helper."""

# standard imports
import csv
import time
import json
import functools
from io import StringIO
from contextlib import suppress
from typing import Any, Callable, Dict, Iterator, Tuple, List

# 3rd party imports
import yaml
import boto3
import botocore
import cfn_tools
import hcl

# local imports
from fluidasserts.utils.generic import get_paths
from fluidasserts.cloud.aws.cloudformation import (
    CloudFormationError,
    CloudFormationInvalidTypeError,
    CloudFormationInvalidTemplateError,
    services,
)
from fluidasserts.cloud.aws.terraform import (
    TerraformError,
    TerraformInvalidTemplateError,
)

# Constants
Template = Dict[str, Any]
TemplatePath = str
ResourceName = str
ResourceProperties = Dict[str, Any]
CLOUDFORMATION_EXTENSIONS = ('.yml', '.yaml', '.json', '.template')
TERRAFORM_EXTENSIONS = ('.tf',)


class ConnError(botocore.vendored.requests.exceptions.ConnectionError):
    """
    A connection error occurred.

    :py:exc:`ConnectionError` wrapper exception.
    """


class ClientErr(botocore.exceptions.BotoCoreError):
    """
    A connection error occurred.

    :py:exc:`ClientError` wrapper exception.
    """


def retry_on_errors(func: Callable) -> Callable:
    """Decorator to retry the function if a ConnError/ClientErr is raised."""
    @functools.wraps(func)
    def decorated(*args, **base_kwargs) -> Any:  # noqa
        """Retry the function if a ConnError/ClientErr is raised."""
        kwargs = base_kwargs.copy()
        retry_times = kwargs.pop('retry_times', 12)
        retry_sleep_seconds = kwargs.pop('retry_sleep_seconds', 1.0)
        if kwargs.get('retry'):
            for _ in range(retry_times):
                try:
                    return func(*args, **kwargs)
                except (ConnError, ClientErr):
                    # Wait some seconds and retry
                    time.sleep(retry_sleep_seconds)
        return func(*args, **kwargs)
    return decorated


# pylint: disable=unused-argument
@retry_on_errors
def get_aws_client(service: str,
                   key_id: str,
                   secret: str,
                   retry: bool = True,
                   **kwargs) -> object:
    """
    Get AWS client object.

    :param service: AWS Service
    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    final_kwargs = {'region_name': 'us-east-1'}
    final_kwargs.update(**kwargs)

    return boto3.client(
        service,
        aws_access_key_id=key_id,
        aws_secret_access_key=secret,
        **final_kwargs)


@retry_on_errors
def client_get_user(client, username):
    """
    Get AWS user from a provided Client.

    :param client: AWS Client instance
    :param username: Username to query for
    """
    return client.get_user(UserName=username)


@retry_on_errors
def client_get_login_profile(client, username):
    """
    Get AWS login profile from a provided Client.

    :param client: AWS Client instance
    :param username: Username to query for
    """
    return client.get_login_profile(UserName=username)


@retry_on_errors
def run_boto3_func(key_id: str,
                   secret: str,
                   service: str,
                   func: str,
                   param: str = None,
                   retry: bool = True,
                   boto3_client_kwargs: dict = None,
                   **kwargs) -> dict:
    """
    Run arbitrary boto3 function.

    :param service: AWS client
    :param func: AWS client's method to call
    :param param: Param to return from response
    """
    try:
        client = get_aws_client(service,
                                key_id=key_id,
                                secret=secret,
                                **(boto3_client_kwargs or {}))
        method_to_call = getattr(client, func)
        result = method_to_call(**kwargs)
        return result if not param else result[param]
    except botocore.vendored.requests.exceptions.ConnectionError:
        raise ConnError
    except botocore.exceptions.ClientError:
        raise ClientErr


@retry_on_errors
def assume_role_credential(key_id: str,
                           secret: str,
                           role_arn: str,
                           session_name: str,
                           external_id: str = None,
                           retry: bool = True,
                           boto3_client_kwargs: dict = None,
                           **kwargs) -> Tuple:
    """
    Allow a user to assume an IAM role.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :param role_arn: role to assume.
    :param session_name: name of the new session.

    :rtype: ``(access_key_id, secret_access_key, session_token)``
    """
    credentials = run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='sts',
        func='assume_role',
        param='Credentials',
        RoleArn=role_arn,
        ExternalId=external_id,
        RoleSessionName=session_name,
        retry=retry)
    return (credentials['AccessKeyId'], credentials['SecretAccessKey'],
            credentials['SessionToken'])


@retry_on_errors
def credentials_report(
        key_id: str,
        secret: str,
        retry: bool = True,
        boto3_client_kwargs: dict = None) -> Tuple[Dict[str, str]]:
    """
    Get IAM credentials report.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        client = get_aws_client(
            service='iam',
            key_id=key_id,
            secret=secret,
            **(boto3_client_kwargs or {}))
        client.generate_credential_report()
        response = client.get_credential_report()
        users_csv = StringIO(response['Content'].decode())
        # Fields are:
        #   user
        #   arn
        #   user_creation_time
        #   password_enabled
        #   password_last_used
        #   password_last_changed
        #   password_next_rotation
        #   mfa_active
        #   access_key_1_active
        #   access_key_1_last_rotated
        #   access_key_1_last_used_date
        #   access_key_1_last_used_region
        #   access_key_1_last_used_service
        #   access_key_2_active
        #   access_key_2_last_rotated
        #   access_key_2_last_used_date
        #   access_key_2_last_used_region
        #   access_key_2_last_used_service
        #   cert_1_active
        #   cert_1_last_rotated
        #   cert_2_active
        #   cert_2_last_rotated
        return tuple(csv.DictReader(users_csv, delimiter=','))
    except botocore.vendored.requests.exceptions.ConnectionError:
        raise ConnError
    except botocore.exceptions.ClientError:
        raise ClientErr


def get_bucket_public_grants(bucket, grants):
    """Check if there are public grants in dict."""
    public_acl = 'http://acs.amazonaws.com/groups/global/AllUsers'
    perms = ['READ', 'WRITE', 'FULL_CONTROL']
    public_buckets = {}
    for grant in grants:
        for (key, val) in grant.items():
            if key == 'Permission' and any(perm in val for perm in perms):
                for (grantee_k, _) in grant['Grantee'].items():
                    if 'URI' in grantee_k and \
                            grant['Grantee']['URI'] == public_acl:
                        public_buckets[val] = bucket
    return public_buckets


#
# CloudFormation
#


def to_boolean(obj: str) -> bool:
    """True if obj is a CloudFormation boolean, False otherwise."""
    if obj in (True, 'true', 'True', '1', 1):
        return True
    if obj in (False, 'false', 'False', '0', 0):
        return False
    raise CloudFormationInvalidTypeError(
        f'{obj} is not a CloudFormation boolean')


def is_scalar(obj: Any) -> bool:
    """True if obj is an scalar."""
    return isinstance(obj, (bool, int, float, str))


def load_cfn_template(template_path: str) -> Template:
    """Return the CloudFormation content of the template on `template_path`."""
    with open(
            template_path,
            encoding='utf-8',
            errors='replace') as template_handle:
        template_contents: str = template_handle.read()

    error_list = []
    for function, errors in (('load_yaml', yaml.error.YAMLError),
                             ('load_json', json.decoder.JSONDecodeError)):

        try:
            contents = getattr(cfn_tools, function)(template_contents)
        except errors as err:
            error_list.append((type(err), err))
        else:
            if isinstance(contents, cfn_tools.odict.ODict) \
                    and contents.get('Resources'):
                return contents

            err = CloudFormationInvalidTemplateError(
                'Not a CloudFormation template')
            error_list.append((type(err), err))

    raise CloudFormationInvalidTemplateError(str(error_list))


def load_tf_template(template_path: str) -> Template:
    """Return the Terraform content of the template on `template_path`."""
    with open(
            template_path,
            encoding='utf-8',
            errors='replace') as template_handle:

        try:
            contents = hcl.load(template_handle)
        except ValueError as exc:
            raise TerraformInvalidTemplateError(str(exc))
        else:
            if isinstance(contents, dict) and contents.get('resource'):
                return contents
            raise TerraformInvalidTemplateError('Not a Terraform Template')


def iterate_rsrcs_in_cfn_template(
        starting_path: str,
        resource_types: list,
        exclude: list = None,
        ignore_errors: bool = True) -> Iterator[
            Tuple[TemplatePath, ResourceName, ResourceProperties]]:
    """Yield resources of the provided types."""
    exclude = tuple(exclude or [])
    for template_path in get_paths(
            starting_path,
            exclude=exclude,
            endswith=CLOUDFORMATION_EXTENSIONS):
        try:
            template: Template = load_cfn_template(template_path)
            for res_name, res_data in template.get('Resources', {}).items():
                if res_name.startswith('Fn::') \
                        or res_name.startswith('!') \
                        or res_data['Type'] not in resource_types:
                    continue

                res_properties = res_data.get('Properties', {})
                res_properties['../Type'] = res_data['Type']

                yield template_path, res_name, res_properties
        except CloudFormationError as exc:
            if not ignore_errors:
                raise exc


def iterate_rsrcs_in_tf_template(
        starting_path: str,
        resource_types: list,
        exclude: list = None,
        ignore_errors: bool = True) -> Iterator[
            Tuple[TemplatePath, ResourceName, ResourceProperties]]:
    """Yield resources of the provided types."""
    exclude = tuple(exclude or [])
    for template_path in get_paths(
            starting_path,
            exclude=exclude,
            endswith=TERRAFORM_EXTENSIONS):
        try:
            template: Template = load_tf_template(template_path)
            resources = template.get('resource', {})
            for res_type in resource_types:
                for res_name, res_data in resources.get(res_type, {}).items():
                    res_properties = res_data
                    res_properties['type'] = res_type

                    yield template_path, res_name, res_properties
        except TerraformError as exc:
            if not ignore_errors:
                raise exc


def service_is_present_action(action: str, service: str) -> bool:
    """Check if a service is present in an action."""
    success = False
    with suppress(KeyError):
        if isinstance(action, list):
            success = service in [act.split(':')[0] for act in action]
        elif action == '*':
            success = True
        else:
            success = action.split(':')[0] == service
    return success


def service_is_present_statement(statement: str, effect: str, service: str):
    """Check if a service is present in a statement."""
    return any([
        sts['Effect'] == effect
        and service_is_present_action(sts['Action'], service)
        if 'Action' in sts else False for sts in force_list(statement)
    ])


def resource_all(resource):
    """Check if an action is permitted for any resource."""
    if isinstance(resource, list):
        aux = []
        for i in resource:
            aux.append(resource_all(i))
        success = any(aux)
    elif isinstance(resource, str):
        success = resource == '*'
    else:
        success = any([resource_all(i) for i in dict(resource).values()])

    return success


def force_list(obj: Any) -> List[Any]:
    """Wrap the element in a list, or if list, leave it intact."""
    return obj if isinstance(obj, list) else [obj]


def policy_statement_privilege(statement, effect: str, action: str):
    """
    Check if a statement of a policy allow an action in all resources.

    :param statemet: policy statement.
    :param effect: (Allow | Deny)
    :param action: (read | list | write | tagging | permissions_management)
    """
    writes = []
    for sts in force_list(statement):
        if sts['Effect'] == effect and 'Resource' in sts and resource_all(
                sts['Resource']):
            writes.append(policy_actions_has_privilege(sts['Action'], action))
    return any(writes)


def policy_actions_has_privilege(action, privilege) -> bool:
    """Check if an action have a privilege."""
    write_actions: dict = services.ACTIONS
    success = False
    with suppress(KeyError):
        if action == '*':
            success = True
        else:
            actions = []
            for act in force_list(action):
                serv, act = act.split(':')
                if act.startswith('*'):
                    actions.append(True)
                else:
                    act = act[:act.index('*')] if act.endswith('*') else act
                    actions.append(
                        act in write_actions.get(serv, {})[privilege])
            success = any(actions)
    return success
