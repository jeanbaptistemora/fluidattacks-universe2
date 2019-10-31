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


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def role_with_unnecessary_privileges(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``Role`` Policies grants wildcard permissions (``*``).

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any **PolicyDocument** grants access over
                wildcard (``*``) Resource or wildcard (``Service::*``) Action
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
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
        for policy in res_props.get('Policies', []):
            policy_document = policy.get('PolicyDocument', {})
            for statement in policy_document.get('Statement', []):
                if statement.get('Effect') != 'Allow':
                    continue
                for action in map(str, _force_list(
                        statement.get('Action', []))):
                    if wildcard_action.match(action):
                        vulnerable_entities.append(f'AWS::IAM::Role/Policies/'
                                                   f'PolicyDocument/Statement/'
                                                   f'Action: {action}')
                for resource in map(str, _force_list(
                        statement.get('Resource', []))):
                    if wildcard_resource.match(resource):
                        vulnerable_entities.append(f'AWS::IAM::Role/Policies/'
                                                   f'PolicyDocument/Statement/'
                                                   f'Resource: {resource}')

        if vulnerable_entities:
            vulnerabilities.extend(
                Vulnerability(
                    path=yaml_path,
                    entity=entity,
                    identifier=res_name,
                    reason='grants wildcard privileges')
                for entity in set(vulnerable_entities))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='IAM Role grants unnecessary privileges',
        msg_closed='IAM Role grants granular privileges')
