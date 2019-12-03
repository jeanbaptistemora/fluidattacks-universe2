"""
AWS CloudFormation checks for ``IAM`` (Identity and Access Management).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/master/LICENSE.md>`_
"""

# Standard imports
import re
from typing import Any, List, Optional, Pattern
from contextlib import suppress

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
    services
)
from fluidasserts.utils.decorators import api, unknown_if


def _force_list(obj: Any) -> List[Any]:
    """Wrap the element in a list, or if list, leave it intact."""
    return obj if isinstance(obj, list) else [obj]


def _policy_actions_has_privilege(action, privilege) -> bool:
    """Check if an action have a privilege."""
    write_actions: dict = services.ACTIONS
    susses = False
    with suppress(KeyError):
        if action == '*':
            susses = True
        else:
            actions = []
            for act in _force_list(action):
                serv, act = act.split(':')
                if act.startswith('*'):
                    actions.append(True)
                else:
                    act = act[:act.index('*')] if act.endswith('*') else act
                    actions.append(
                        act in write_actions.get(serv, {})[privilege])
            susses = any(actions)
    return susses


def _resource_all(resource):
    susses = False
    if isinstance(resource, list):
        aux = []
        for i in resource:
            aux.append(_resource_all(i))
        susses = any(aux)
    elif isinstance(resource, str):
        susses = resource == '*'
    else:
        susses = any([_resource_all(i) for i in dict(resource).values()])

    return susses


def _policy_statement_privilege(statement, effect: str, action: str):
    """
    Check if a statement of a policy allow an action in all resources.

    :param statemet: policy statement.
    :param effect: (Allow | Deny)
    :param action: (read | list | write | tagging | permissions_management)
    """
    writes = []
    for sts in _force_list(statement):
        if sts['Effect'] == effect and 'Resource' in sts and _resource_all(
                sts['Resource']):
            writes.append(_policy_actions_has_privilege(sts['Action'], action))
    return any(writes)


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
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
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
            for statement in _force_list(policy_document.get('Statement', [])):
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
                for action in map(str, _force_list(
                        statement.get('Action', []))):
                    # F3: IAM role should not allow * action on its
                    #   permissions policy
                    if wildcard_action.match(action):
                        entity = (f'Policies/PolicyDocument'
                                  f'/Statement/Action: {action}')
                        reason = 'grants wildcard privileges'
                        vulnerable_entities.append((entity, reason))
                for resource in map(str, _force_list(
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

        for statement in _force_list(res_props.get(
                'AssumeRolePolicyDocument', {}).get('Statement', [])):
            if statement.get('Effect') != 'Allow':
                continue
            for action in map(str, _force_list(
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
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                f'AWS::IAM::{resource}',
            ],
            exclude=exclude):
        vulnerable_entities: List[str] = []

        policy_document = res_props.get('PolicyDocument', {})
        for statement in _force_list(policy_document.get('Statement', [])):
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
            for action in map(str, _force_list(
                    statement.get('Action', []))):
                # F4: IAM policy should not allow * action
                # F5: IAM managed policy should not allow * action
                if wildcard_action.match(action):
                    entity = (f'{resource}/PolicyDocument'
                              f'/Statement/Action: {action}')
                    reason = 'grants wildcard privileges'
                    vulnerable_entities.append((entity, reason))
            for _resource in map(str, _force_list(
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
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
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

    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
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
            if _policy_statement_privilege(policy['Statement'], 'Allow',
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
                    if _policy_statement_privilege(
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
                    reason=reason) for entity, reason in vulnerable_entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Write actions are allowed for all resources.',
        msg_closed='Write actions are not allowed for all resources.')
