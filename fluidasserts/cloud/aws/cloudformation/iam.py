"""
AWS CloudFormation checks for ``IAM`` (Identity and Access Management).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

# Standard imports
import re
from typing import List, Optional, Pattern, Dict, Tuple
from contextlib import suppress

from networkx import DiGraph

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import get_graph
from fluidasserts.cloud.aws.cloudformation import get_resources
from fluidasserts.cloud.aws.cloudformation import has_values
from fluidasserts.cloud.aws.cloudformation import get_type


@api(risk=MEDIUM, kind=SAST)  # noqa: MC0001
@unknown_if(FileNotFoundError)
def is_role_over_privileged(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``IAM::Role`` is miss configured.

    The following checks are performed:

    * F2 IAM role should not allow * action on its trust policy
    * F3 IAM role should not allow * action on its permissions policy
    * F6 IAM role should not allow Allow+NotPrincipal in its trust policy
    * F38 IAM role should not allow * resource with PassRole action on its
        permissions policy
    * W11 IAM role should not allow * resource on its permissions policy
    * W14 IAM role should not allow Allow+NotAction on trust permissions
    * W15 IAM role should not allow Allow+NotAction
    * W21 IAM role should not allow Allow+NotResource
    * W43 IAM role should not have AdministratorAccess policy

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    # pylint: disable=too-many-branches
    vulnerabilities: list = []
    wildcard_action: Pattern = re.compile(r'^(\*)|(\w+:\*)$')
    wildcard_resource: Pattern = re.compile(r'^(\*)$')
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::IAM::Role',
            ],
            exclude=exclude):
        vulnerable_entities: List[str] = []

        for managed_policy in res_props.get('ManagedPolicyArns', []):
            # W43: IAM role should not have AdministratorAccess policy
            if 'AdministratorAccess' in managed_policy:
                entity = f'ManagedPolicyArns: {managed_policy}'
                reason = 'grants excessive privileges'
                vulnerable_entities.append((entity, reason))

        for policy in res_props.get('Policies', []):
            policy_document = policy.get('PolicyDocument', {})
            for statement in helper.force_list(
                    policy_document.get('Statement', [])):
                if statement.get('Effect') != 'Allow':
                    continue

                # W15: IAM role should not allow Allow+NotAction
                if 'NotAction' in statement:
                    entity = 'Policies/PolicyDocument/Statement/NotAction'
                    reason = 'avoid security through black listing'
                    vulnerable_entities.append((entity, reason))
                # W21: IAM role should not allow Allow+NotResource
                if 'NotResource' in statement:
                    entity = 'Policies/PolicyDocument/Statement/NotResource'
                    reason = 'avoid security through black listing'
                    vulnerable_entities.append((entity, reason))
                for action in map(str, helper.force_list(
                        statement.get('Action', []))):
                    # F3: IAM role should not allow * action on its
                    #   permissions policy
                    if wildcard_action.match(action):
                        entity = (f'Policies/PolicyDocument'
                                  f'/Statement/Action: {action}')
                        reason = 'grants wildcard privileges'
                        vulnerable_entities.append((entity, reason))
                for resource in map(str, helper.force_list(
                        statement.get('Resource', []))):
                    # W11: IAM role should not allow * resource on its
                    #   permissions policy
                    # F38: IAM role should not allow * resource with
                    #   PassRole action on its permissions policy
                    if wildcard_resource.match(resource):
                        entity = (f'Policies/PolicyDocument'
                                  f'/Statement/Resource: {resource}')
                        reason = 'grants wildcard privileges'
                        vulnerable_entities.append((entity, reason))

        for statement in helper.force_list(res_props.get(
                'AssumeRolePolicyDocument', {}).get('Statement', [])):
            if statement.get('Effect') != 'Allow':
                continue
            for action in map(str, helper.force_list(
                    statement.get('Action', []))):
                # F2: IAM role should not allow * action on its trust policy
                if wildcard_action.match(action):
                    entity = (f'AssumeRolePolicyDocument'
                              f'/Statement/Action: {action}')
                    reason = 'grants wildcard privileges'
                    vulnerable_entities.append((entity, reason))
            # W14: IAM role should not allow Allow+NotAction on
            #   trust permissions
            if 'NotAction' in statement:
                entity = f'AssumeRolePolicyDocument/Statement/NotAction'
                reason = 'avoid security through black listing'
                vulnerable_entities.append((entity, reason))
            # F6: IAM role should not allow Allow+NotPrincipal in
            #   its trust policy
            if 'NotPrincipal' in statement:
                entity = 'AssumeRolePolicyDocument/Statement/NotPrincipal'
                reason = 'avoid security through black listing'
                vulnerable_entities.append((entity, reason))

        if vulnerable_entities:
            vulnerabilities.extend(
                Vulnerability(
                    path=yaml_path,
                    entity=f'AWS::IAM::Role/{entity}',
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason=reason)
                for entity, reason in set(vulnerable_entities))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='IAM Role grants unnecessary privileges',
        msg_closed='IAM Role grants granular privileges')


def _is_generic_policy_miss_configured(  # noqa: MC0001
        path: str, exclude: Optional[List[str]], resource: str) -> tuple:
    """Policy and ManagedPolicy are equal in its PolicyDocument, reuse code."""
    vulnerabilities: list = []
    wildcard_action: Pattern = re.compile(r'^(\*)|(\w+:\*)$')
    wildcard_resource: Pattern = re.compile(r'^(\*)$')
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                f'AWS::IAM::{resource}',
            ],
            exclude=exclude):
        vulnerable_entities: List[str] = []

        policy_document = res_props.get('PolicyDocument', {})
        for statement in helper.force_list(
                policy_document.get('Statement', [])):
            if statement.get('Effect') != 'Allow':
                continue

            # W16: IAM policy should not allow Allow+NotAction
            # W17: IAM managed policy should not allow Allow+NotAction
            if 'NotAction' in statement:
                entity = f'{resource}/PolicyDocument/Statement/NotAction'
                reason = 'avoid security through black listing'
                vulnerable_entities.append((entity, reason))
            # W22: IAM policy should not allow Allow+NotResource
            # W23: IAM managed policy should not allow Allow+NotResource
            if 'NotResource' in statement:
                entity = f'{resource}/PolicyDocument/Statement/NotResource'
                reason = 'avoid security through black listing'
                vulnerable_entities.append((entity, reason))
            for action in map(str, helper.force_list(
                    statement.get('Action', []))):
                # F4: IAM policy should not allow * action
                # F5: IAM managed policy should not allow * action
                if wildcard_action.match(action):
                    entity = (f'{resource}/PolicyDocument'
                              f'/Statement/Action: {action}')
                    reason = 'grants wildcard privileges'
                    vulnerable_entities.append((entity, reason))
            for _resource in map(str, helper.force_list(
                    statement.get('Resource', []))):
                # W12: IAM policy should not allow * resource
                # W13: IAM managed policy should not allow * resource
                # F39: IAM policy should not allow * resource with
                #   PassRole action
                # F40: IAM managed policy should not allow a * resource with
                #   PassRole action
                if wildcard_resource.match(_resource):
                    entity = (f'{resource}/PolicyDocument'
                              f'/Statement/Resource: {_resource}')
                    reason = 'grants wildcard privileges'
                    vulnerable_entities.append((entity, reason))

        for user in res_props.get('Users', []):
            # F11: IAM policy should not apply directly to users.
            #   Should be on group
            # F12: IAM managed policy should not apply directly to users.
            #   Should be on group
            entity = f'{resource}/Users: {user}'
            reason = f'{resource} applied to user, apply to role instead'
            vulnerable_entities.append((entity, reason))

        if vulnerable_entities:
            vulnerabilities.extend(
                Vulnerability(
                    path=yaml_path,
                    entity=f'AWS::IAM::{resource}/{entity}',
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason=reason)
                for entity, reason in set(vulnerable_entities))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=f'IAM {resource} is miss configured',
        msg_closed=f'IAM {resource} is properly configured')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_policy_miss_configured(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``IAM::Policy`` is miss configured.

    The following checks are performed:

    * F4 IAM policy should not allow * action
    * F11 IAM policy should not apply directly to users.
        Should be on group
    * F39 IAM policy should not allow * resource with PassRole action
    * W12 IAM policy should not allow * resource
    * W16 IAM policy should not allow Allow+NotAction
    * W22 IAM policy should not allow Allow+NotResource

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _is_generic_policy_miss_configured(
        path=path, exclude=exclude, resource='Policy')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_managed_policy_miss_configured(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``IAM::ManagedPolicy`` is miss configured.

    The following checks are performed:

    * F5 IAM managed policy should not allow * action
    * F12 IAM managed policy should not apply directly to users.
        Should be on group
    * F40 IAM managed policy should not allow a * resource with PassRole action
    * W13 IAM managed policy should not allow * resource
    * W17 IAM managed policy should not allow Allow+NotAction
    * W23 IAM managed policy should not allow Allow+NotResource

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _is_generic_policy_miss_configured(
        path=path, exclude=exclude, resource='ManagedPolicy')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def missing_role_based_security(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``IAM::User`` is granted privileges but not through a Role.

    The following checks are performed:

    * F10 IAM user should not have any inline policies.
        Should be centralized Policy object on group (Role)

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::IAM::User',
            ],
            exclude=exclude):
        vulnerable_entities: List[str] = []

        # F10: IAM user should not have any inline policies.
        #   Should be centralized Policy object on group (Role)
        for policy in res_props.get('Policies', []):
            policy_name = policy.get('PolicyName')
            if not policy_name:
                policy_name = policy.get('Ref')
            if not policy_name:
                policy_name = 'any'
            entity = f'Policies: {policy_name}'
            reason = ('do not attach inline policies'
                      '; use role-based access control')
            vulnerable_entities.append((entity, reason))

        if vulnerable_entities:
            vulnerabilities.extend(
                Vulnerability(
                    path=yaml_path,
                    entity=f'AWS::IAM::User/{entity}',
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason=reason)
                for entity, reason in set(vulnerable_entities))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='IAM User is not assigned permissions through a role',
        msg_closed='IAM User is assigned permissions through a role')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_wildcard_resource_on_write_action(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if write actions are allowed on all resources.

    Do not allow ``"Resource": "*"`` to have write actions.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []

    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::IAM::Role',
                'AWS::IAM::ManagedPolicy',
            ],
            exclude=exclude):
        vulnerable_entities: List[str] = []
        type_ = res_props['../Type']

        if res_props.get('PolicyDocument', []):
            policy = res_props['PolicyDocument']
            if helper.policy_statement_privilege(policy['Statement'], 'Allow',
                                                 'write'):
                type_name = res_props['../Type'].split('::')[-1]
                try:
                    name = res_props[f'{type_name}Name']
                    entity = name if isinstance(name, str) else res_name
                except KeyError:
                    entity = res_name
                reason = 'allows write actions on a wildcard resource.'
                vulnerable_entities.append((entity, reason))

        if res_props.get('Policies', []):
            for policy in res_props['Policies']:
                with suppress(KeyError):
                    if helper.policy_statement_privilege(
                            policy['PolicyDocument']['Statement'], 'Allow',
                            'write'):
                        name = policy['PolicyName']
                        entity = name if isinstance(name, str) else res_name
                        reason = 'allows write actions on a wildcard resource.'
                        vulnerable_entities.append((entity, reason))

        if vulnerable_entities:
            vulnerabilities.extend(
                Vulnerability(
                    path=yaml_path,
                    entity=f'{type_}/{entity}',
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason=reason) for entity, reason in vulnerable_entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Write actions are allowed for all resources.',
        msg_closed='Write actions are not allowed for all resources.')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_privileges_over_iam(path: str,
                            exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if a policy documents has privileges over iam.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any policy documents has privileges over iam.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::IAM::Role',
                'AWS::IAM::ManagedPolicy',
            ],
            exclude=exclude):
        type_ = res_props['../Type']
        vulnerable_entities: List[str] = []
        if res_props.get('PolicyDocument', []):
            policy = res_props['PolicyDocument']
            if helper.service_is_present_statement(policy['Statement'],
                                                   'Allow', 'iam'):
                type_name = res_props['../Type'].split('::')[-1]
                try:
                    name = res_props[f'{type_name}Name']
                    entity = name if isinstance(name, str) else res_name
                except KeyError:
                    entity = res_name
                reason = 'has privileges over iam.'
                vulnerable_entities.append((entity, reason))

        if res_props.get('Policies', []):
            for policy in res_props['Policies']:
                with suppress(KeyError):
                    if helper.service_is_present_statement(
                            policy['PolicyDocument']['Statement'], 'Allow',
                            'iam'):
                        name = policy['PolicyName']
                        entity = name if isinstance(name, str) else res_name
                        reason = 'has privileges over iam.'
                        vulnerable_entities.append((entity, reason))

        if vulnerable_entities:
            vulnerabilities.extend(
                Vulnerability(
                    path=yaml_path,
                    entity=f'{type_}/{entity}',
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason=reason) for entity, reason in vulnerable_entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Policies have privileges over iam.',
        msg_closed='Policies have no privileges over iam.')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_full_access_to_ssm(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if there are policy documents that allow full access to ssm agent.

    SSM allows everyone with access to run commands as root on EC2 instances

    https://cloudonaut.io/aws-ssm-is-a-trojan-horse-fix-it-now/

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    documents: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates), {
            'AWS', 'IAM', 'ManagedPolicy', 'Policy', 'Role'},
        info=True, num_labels=3)
    for doc, resource, template in documents:
        type_: str = "AWS::IAM::" + \
            get_type(graph, doc, {'ManagedPolicy', 'Policy', 'Role'})
        reason: str = 'allows full access to SSM.'
        vulnerable_lines: List[int] = []
        policy_document: int = helper.get_index(get_resources(
            graph, doc, 'PolicyDocument', depth=8), 0)
        if not policy_document:
            continue

        effects = has_values(graph, policy_document, 'Effect', 'Allow', 4)
        for effect in effects:
            vulnerable = False
            father = graph.predecessors(effect)
            action = helper.get_index(
                get_resources(graph, father, 'Action'), 0)
            if action:
                vulnerable = [graph.nodes[node]['line'] for node in has_values(
                    graph, action, 'Item', 'ssm:*', depth=4)]
            if vulnerable:
                vulnerable_lines.extend(vulnerable)
        if vulnerable_lines:
            vulnerabilities.extend(
                Vulnerability(
                    path=template['path'],
                    entity=f'{type_}/PolicyDocument',
                    identifier=resource['name'],
                    line=line,
                    reason=reason) for line in vulnerable_lines)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Policy allows full access to SSM.',
        msg_closed='Policy does not allow full access to SSM.')
