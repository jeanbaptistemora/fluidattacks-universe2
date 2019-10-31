"""AWS CloudFormation checks for IAM."""

# Standard imports
import re
from typing import Any, List, Optional, Pattern

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


def _force_list(obj: Any) -> List[Any]:
    """Wrap the element in a list, or if list, leave it intact."""
    return obj if isinstance(obj, list) else [obj]


@api(risk=MEDIUM, kind=SAST)  # noqa: MC0001
@unknown_if(FileNotFoundError)
def is_role_over_privileged(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``IAM::Role`` is miss configured.

    The following checks are performed:

    - F2 IAM role should not allow * action on its trust policy
    - F3 IAM role should not allow * action on its permissions policy
    - F6 IAM role should not allow Allow+NotPrincipal in its trust policy
    - F38 IAM role should not allow * resource with PassRole action on its
        permissions policy
    - W11 IAM role should not allow * resource on its permissions policy
    - W14 IAM role should not allow Allow+NotAction on trust permissions
    - W15 IAM role should not allow Allow+NotAction
    - W21 IAM role should not allow Allow+NotResource
    - W43 IAM role should not have AdministratorAccess policy

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
