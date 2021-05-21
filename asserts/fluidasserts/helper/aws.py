# -*- coding: utf-8 -*-

# pylint: disable=import-outside-toplevel
"""AWS cloud helper."""

# standard imports
from contextlib import suppress
import csv
import functools
from io import StringIO
from ipaddress import IPv4Network
from ipaddress import IPv6Network
from ipaddress import AddressValueError
import random
import string
import time
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterator
from typing import List
from typing import NoReturn
from typing import Set
from typing import Tuple

# 3rd party imports
import boto3
import botocore
import cfn_tools
import hcl
import yaml
from lark import LarkError
from networkx import DiGraph
from networkx.algorithms import dfs_preorder_nodes

# local imports
from fluidasserts.cloud.aws.terraform import TerraformError
from fluidasserts.cloud.aws.terraform import TerraformInvalidTemplateError
from fluidasserts.helper.yaml_loader_alt import LineLoader
from fluidasserts.utils.generic import get_paths
from fluidasserts.utils.parsers import json as l_json

# Constants
Template = Dict[str, Any]
TemplatePath = str
ResourceName = str
ResourceProperties = Dict[str, Any]
CLOUDFORMATION_EXTENSIONS = (".yml", ".yaml", ".json", ".template")
TERRAFORM_EXTENSIONS = (".tf",)


class ConnError(botocore.vendored.requests.exceptions.ConnectionError):
    """A connection error occurred.

    :py:exc:`ConnectionError` wrapper exception.
    """


class ClientErr(botocore.exceptions.BotoCoreError):
    """A connection error occurred.

    :py:exc:`ClientError` wrapper exception.
    """


class CloudFormationError(Exception):
    """Base class for all errors in this module."""


class CloudFormationInvalidTypeError(CloudFormationError):
    """The Value is not of recognized type."""


class CloudFormationInvalidTemplateError(CloudFormationError):
    """The template is not JSON or YAML compliant."""


def retry_on_errors(func: Callable) -> Callable:
    """Decorator to retry the function if a ConnError/ClientErr is raised."""

    @functools.wraps(func)
    def decorated(*args, **base_kwargs) -> Any:  # noqa
        """Retry the function if a ConnError/ClientErr is raised."""
        kwargs = base_kwargs.copy()
        retry_times = kwargs.pop("retry_times", 12)
        retry_sleep_seconds = kwargs.pop("retry_sleep_seconds", 1.0)
        if kwargs.get("retry"):
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
def get_aws_client(
    service: str, key_id: str, secret: str, retry: bool = True, **kwargs
) -> object:
    """Get AWS client object.

    :param service: AWS Service
    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    final_kwargs = {"region_name": "us-east-1"}
    final_kwargs.update(**kwargs)

    return boto3.client(
        service,
        aws_access_key_id=key_id,
        aws_secret_access_key=secret,
        **final_kwargs,
    )


def validate_access_controls(
    access_controls: Set[str], valid_controls: Set[str]
) -> NoReturn:
    """Validate that the provided acl is recognized by Terraform."""
    invalid_access_controls = access_controls - valid_controls
    if invalid_access_controls:
        raise AssertionError(
            f"Invalid Access Controls detected: {invalid_access_controls}"
        )


@retry_on_errors
def client_get_user(client, username):
    """Get AWS user from a provided Client.

    :param client: AWS Client instance
    :param username: Username to query for
    """
    return client.get_user(UserName=username)


@retry_on_errors
def client_get_login_profile(client, username):
    """Get AWS login profile from a provided Client.

    :param client: AWS Client instance
    :param username: Username to query for
    """
    return client.get_login_profile(UserName=username)


@retry_on_errors
def run_boto3_func(
    key_id: str,
    secret: str,
    service: str,
    func: str,
    param: str = None,
    retry: bool = True,
    boto3_client_kwargs: dict = None,
    **kwargs,
) -> dict:
    """Run arbitrary boto3 function.

    :param service: AWS client
    :param func: AWS client's method to call
    :param param: Param to return from response
    """
    try:
        client = get_aws_client(
            service,
            key_id=key_id,
            secret=secret,
            **(boto3_client_kwargs or {}),
        )
        method_to_call = getattr(client, func)
        result = method_to_call(**kwargs)
        return result if not param else result[param]
    except botocore.vendored.requests.exceptions.ConnectionError:
        raise ConnError
    except botocore.exceptions.ClientError:
        raise ClientErr


@retry_on_errors
def assume_role_credential(
    key_id: str,
    secret: str,
    role_arn: str,
    session_name: str,
    external_id: str = None,
    retry: bool = True,
    boto3_client_kwargs: dict = None,
    **kwargs,
) -> Tuple:
    """Allow a user to assume an IAM role.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :param role_arn: role to assume.
    :param session_name: name of the new session.

    :rtype: ``(access_key_id, secret_access_key, session_token)``
    """
    credentials = run_boto3_func(
        key_id=key_id,
        secret=secret,
        service="sts",
        func="assume_role",
        param="Credentials",
        RoleArn=role_arn,
        ExternalId=external_id,
        RoleSessionName=session_name,
        retry=retry,
    )
    return (
        credentials["AccessKeyId"],
        credentials["SecretAccessKey"],
        credentials["SessionToken"],
    )


@retry_on_errors
def credentials_report(
    key_id: str,
    secret: str,
    retry: bool = True,
    boto3_client_kwargs: dict = None,
) -> Tuple[Dict[str, str]]:
    """Get IAM credentials report.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        client = get_aws_client(
            service="iam",
            key_id=key_id,
            secret=secret,
            **(boto3_client_kwargs or {}),
        )
        client.generate_credential_report()
        response = client.get_credential_report()
        users_csv = StringIO(response["Content"].decode())
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
        return tuple(csv.DictReader(users_csv, delimiter=","))
    except botocore.vendored.requests.exceptions.ConnectionError:
        raise ConnError
    except botocore.exceptions.ClientError:
        raise ClientErr


def get_bucket_public_grants(bucket, grants):
    """Check if there are public grants in dict."""
    public_acl = "http://acs.amazonaws.com/groups/global/AllUsers"
    public_buckets = _get_buckets_acl(bucket, grants, public_acl)
    return public_buckets


def get_bucket_authenticated_grants(bucket, grants):
    """Check if there are authenticated grants in dict."""
    public_acl = "http://acs.amazonaws.com/groups/global/AuthenticatedUsers"
    public_buckets = _get_buckets_acl(bucket, grants, public_acl)
    return public_buckets


def _get_buckets_acl(bucket, grants, public_acl):
    perms = ["READ", "WRITE", "FULL_CONTROL", "READ_ACP", "WRITE_ACP"]
    public_buckets = {}
    for grant in grants:
        for (key, val) in grant.items():
            if key == "Permission" and any(perm in val for perm in perms):
                for (grantee_k, _) in grant["Grantee"].items():
                    if (
                        "URI" in grantee_k
                        and grant["Grantee"]["URI"] == public_acl
                    ):
                        public_buckets[val] = bucket
    return public_buckets


#
# CloudFormation
#


def to_boolean(obj: str) -> bool:
    """True if obj is a CloudFormation boolean, False otherwise."""
    if obj in (True, "true", "True", "1", 1):
        return True
    if obj in (False, "false", "False", "0", 0):
        return False
    raise CloudFormationInvalidTypeError(
        f"{obj} is not a CloudFormation boolean"
    )


def is_boolean(obj) -> bool:
    """Validate if it is a cloudformation boolean."""
    return obj in (
        True,
        "true",
        "True",
        "1",
        1,
        False,
        "false",
        "False",
        "0",
        0,
    )


def is_scalar(obj: Any) -> bool:
    """True if obj is an scalar."""
    return isinstance(obj, (bool, int, float, str))


def is_yaml(path: str) -> bool:
    """True if path is a yaml file."""
    return path.endswith((".yml", ".yaml"))


def load_cfn_template(template_path: str) -> Template:
    """Return the CloudFormation content of the template on `template_path`."""
    with open(
        template_path, encoding="utf-8", errors="replace"
    ) as template_handle:
        template_contents: str = template_handle.read()

    error_list = []

    try:
        if is_yaml(template_path):
            contents = yaml.load(template_contents, Loader=LineLoader)  # nosec
        else:
            contents = l_json.parse(template_contents)
    except (yaml.error.YAMLError, LarkError) as err:
        error_list.append((type(err), err))
    else:
        if isinstance(
            contents, (cfn_tools.odict.ODict, l_json.CustomDict)
        ) and contents.get("Resources"):
            return contents

        err = CloudFormationInvalidTemplateError(
            "Not a CloudFormation template"
        )
        error_list.append((type(err), err))

    raise CloudFormationInvalidTemplateError(str(error_list))


def load_tf_template(template_path: str) -> Template:
    """Return the Terraform content of the template on `template_path`."""
    with open(
        template_path, encoding="utf-8", errors="replace"
    ) as template_handle:

        try:
            contents = hcl.load(template_handle)
        except ValueError as exc:
            raise TerraformInvalidTemplateError(str(exc))
        else:
            if isinstance(contents, dict) and contents.get("resource"):
                return contents
            raise TerraformInvalidTemplateError("Not a Terraform Template")


def iterate_rsrcs_in_cfn_template(
    starting_path: str,
    resource_types: list,
    exclude: list = None,
    ignore_errors: bool = True,
) -> Iterator[Tuple[TemplatePath, ResourceName, ResourceProperties]]:
    """Yield resources of the provided types."""
    exclude = tuple(exclude or [])
    for template_path in get_paths(
        starting_path, exclude=exclude, endswith=CLOUDFORMATION_EXTENSIONS
    ):
        try:
            template: Template = load_cfn_template(template_path)
            if is_yaml(template_path):
                resources = template.get("Resources", {}).items()[:-1]
            else:
                resources = template.get("Resources", {}).items()
            for res_name, res_data in resources:
                if (
                    res_name.startswith("Fn::")
                    or res_name.startswith("!")
                    or res_data["Type"] not in resource_types
                ):
                    continue

                res_properties = res_data.get("Properties", {})
                res_properties["../Type"] = res_data["Type"]
                if "__line__" in res_data:
                    res_properties["line"] = res_data["__line__"]
                else:
                    res_properties["line"] = 0

                yield template_path, res_name, res_properties
        except CloudFormationError as exc:
            if not ignore_errors:
                raise exc


def iterate_rsrcs_in_tf_template(
    starting_path: str,
    resource_types: list,
    exclude: list = None,
    ignore_errors: bool = True,
) -> Iterator[Tuple[TemplatePath, ResourceName, ResourceProperties]]:
    """Yield resources of the provided types."""
    exclude = tuple(exclude or [])
    for template_path in get_paths(
        starting_path, exclude=exclude, endswith=TERRAFORM_EXTENSIONS
    ):
        try:
            template: Template = load_tf_template(template_path)
            resources = template.get("resource", {})
            for res_type in resource_types:
                for res_name, res_data in resources.get(res_type, {}).items():
                    res_properties = res_data
                    res_properties["type"] = res_type

                    yield template_path, res_name, res_properties
        except TerraformError as exc:
            if not ignore_errors:
                raise exc


def service_is_present_action(action: str, service: str) -> bool:
    """Check if a service is present in an action."""
    success = False
    with suppress(KeyError):
        if isinstance(action, (list, l_json.CustomList)):
            success = service in [act.split(":")[0] for act in action]
        elif action == "*":
            success = True
        else:
            success = action.split(":")[0] == service
    return success


def service_is_present_action_(
    graph: DiGraph, action: int, service: str
) -> bool:
    """Check if a service is present in an action."""
    success = False
    action_node = graph.nodes[action]
    if "value" in action_node:
        if action_node["value"] == "*":
            success = True
        else:
            success = action_node["value"].split(":")[0] == service
    else:
        services = []
        actions = dfs_preorder_nodes(graph, action)
        for act in actions:
            node = graph.nodes[act]
            if "value" in node:
                services.append(node["value"].split(":")[0])
        success = service in services
    return success


def service_is_present_statement_(
    graph: DiGraph, statement: int, effect: str, service: str
):
    """Check if a service is present in a statement."""
    effect_nodes = [
        node
        for node in dfs_preorder_nodes(graph, statement)
        if "Effect" in graph.nodes[node]["labels"]
    ]
    vulns = []
    for eff in effect_nodes:
        father = list(graph.predecessors(eff))[0]
        action_node = get_index(
            [
                node
                for node in dfs_preorder_nodes(graph, father)
                if "Action" in graph.nodes[node]["labels"]
            ],
            0,
        )
        eff_node = graph.nodes[eff]
        if action_node:
            vulns.append(
                eff_node["value"] == effect
                and service_is_present_action_(graph, action_node, service)
            )
    return any(vulns)


def service_is_present_statement(statement: str, effect: str, service: str):
    """Check if a service is present in a statement."""
    return any(
        [
            sts["Effect"] == effect
            and service_is_present_action(sts["Action"], service)
            if "Action" in sts
            else False
            for sts in force_list(statement)
        ]
    )


def resource_all(resource):
    """Check if an action is permitted for any resource."""
    if isinstance(resource, (list, l_json.CustomList)):
        aux = []
        for i in resource:
            aux.append(resource_all(i))
        success = any(aux)
    elif isinstance(resource, str):
        success = resource == "*"
    else:
        success = any([resource_all(i) for i in dict(resource).values()])

    return success


def resource_all_(graph: DiGraph, resource: int):
    """Check if an action is permitted for any resource."""
    nodes = dfs_preorder_nodes(graph, resource)
    for node in nodes:
        node_data = graph.nodes[node]
        if "value" in node_data:
            if node_data["value"] == "*":
                return True
    return False


def force_list(obj: Any) -> List[Any]:
    """Wrap the element in a list, or if list, leave it intact."""
    if not obj:
        ret = []
    elif isinstance(obj, (list, l_json.CustomList)):
        ret = obj
    else:
        ret = [obj]
    return ret


def get_line(obj: any):
    """Return the line of an cloudformation node."""
    line = getattr(obj, "__line__", None)
    with suppress(AttributeError):
        line = line or obj.get("__line__")
    with suppress(KeyError, TypeError):
        line = line or obj["line"]
    line = line or 0

    return line


def get_items(obj: any):
    """Return the items of a cloudformation node."""
    return map(lambda x: x, obj)


def policy_statement_privilege(statement, effect: str, action: str):
    """Check if a statement of a policy allow an action in all resources.

    :param statemet: policy statement.
    :param effect: (Allow | Deny)
    :param action: (read | list | write | tagging | permissions_management)
    """
    writes = []
    for sts in force_list(statement):
        if (
            sts["Effect"] == effect
            and "Resource" in sts
            and resource_all(sts["Resource"])
        ):
            writes.append(policy_actions_has_privilege(sts["Action"], action))
    return any(writes)


def policy_actions_has_privilege(action, privilege) -> bool:
    """Check if an action have a privilege."""
    from fluidasserts.cloud.aws.cloudformation import services

    write_actions: dict = services.ACTIONS
    success = False
    with suppress(KeyError):
        if action == "*":
            success = True
        else:
            actions = []
            for act in force_list(action):
                serv, act = act.split(":")
                if act.startswith("*"):
                    actions.append(True)
                else:
                    act = act[: act.index("*")] if act.endswith("*") else act
                    actions.append(
                        act in write_actions.get(serv, {})[privilege]
                    )
            success = any(actions)
    return success


def get_paginated_items(
    key_id,
    retry,
    secret,
    session_token,
    service_name,
    func_name,
    max_name,
    token_name,
    object_name,
    next_token_name=None,
    extra_args=None,
):
    """Get all items in paginated API calls."""
    pools = []
    args = {
        "key_id": key_id,
        "secret": secret,
        "service": service_name,
        "func": func_name,
        max_name: 50,
        "retry": retry,
        "boto3_client_kwargs": {"aws_session_token": session_token},
    }
    if extra_args:
        args.update(extra_args)
    data = run_boto3_func(**args)
    pools += data.get(object_name, [])
    next_token = data.get(token_name, "")
    args[next_token_name if next_token_name else token_name] = next_token
    while next_token:
        data = run_boto3_func(**args)
        pools += data[object_name]
        next_token = data.get(next_token_name, "")
    return pools


def _random_string(string_length=5):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return "".join(random.sample(letters, string_length))


def is_cidr(cidr: str):
    """Validate if a string is a valid CIDR."""
    result = False
    with suppress(AddressValueError, ValueError):
        IPv4Network(cidr, strict=False)
        result = True
    with suppress(AddressValueError, ValueError):
        IPv6Network(cidr, strict=False)
        result = True
    return result


def is_ip_protocol(protocol):
    """Validate if a value is a valid ip protocol."""
    if protocol in ("tcp", "udp", "icmp", "icmpv6"):
        return True
    if isinstance(protocol, (int, float)):
        return True
    with suppress(ValueError):
        int(protocol)
        return True
    return False


def get_index(items: List, index: int, default: Any = None):
    """Get items from a list safely."""
    value = default
    with suppress(IndexError):
        value = items[index]
    return value
