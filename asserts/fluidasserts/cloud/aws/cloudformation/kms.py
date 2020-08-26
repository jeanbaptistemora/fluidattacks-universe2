"""
AWS CloudFormation checks for ``KMS`` (Key Management Service).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

# Standard imports
import contextlib
from typing import Dict, List, Optional, Tuple

# Treed imports
from networkx import DiGraph

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.helper.aws import CloudFormationInvalidTypeError
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple
)
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import get_graph
from fluidasserts.cloud.aws.cloudformation import get_resources
from fluidasserts.cloud.aws.cloudformation import get_ref_nodes


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_key_rotation_absent_or_disabled(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Check if any ``KMS::Key`` is miss configured.

    The following checks are performed:

    * F19 EnableKeyRotation should not be false or absent on KMS::Key resource

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
    keys: List[int] = get_resources(graph, map(lambda x: x[0], templates),
                                    {'AWS', 'KMS', 'Key'}, info=True)
    for key, resource, template in keys:
        line: int = resource['line']
        key_rotation: bool = False
        rotation_node: int = helper.get_index(
            get_resources(graph, key, 'EnableKeyRotation', depth=3), 0)
        if rotation_node:
            rotation_node_value: int = get_ref_nodes(graph, rotation_node)[0]
            line = graph.nodes[rotation_node_value]['line']
            with contextlib.suppress(CloudFormationInvalidTypeError):
                key_rotation = helper.to_boolean(
                    graph.nodes[rotation_node_value]['value'])

        if not key_rotation:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=f'AWS::KMS::Key',
                    identifier=resource['name'],
                    line=line,
                    reason='has key rotation absent or disabled'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EnableKeyRotation is absent or disabled on KMS Key',
        msg_closed='EnableKeyRotation is enabled on KMS Key')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_master_keys_exposed_to_everyone(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Check if Amazon KMS master keys are exposed to everyone.

    Allowing anonymous access to your AWS KMS keys is considered bad practice
    and can lead to sensitive data leakage.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    keys: List[int] = get_resources(graph, map(lambda x: x[0], templates),
                                    {'AWS', 'KMS', 'Key'}, info=True)
    for key, resource, template in keys:
        key_policy_node: int = helper.get_index(
            get_resources(graph, key, 'KeyPolicy', depth=3), 0)
        statements: List[int] = get_resources(
            graph, key_policy_node, 'Statement', depth=3)
        principals: List[int] = get_resources(
            graph, statements, 'Principal', depth=3)

        for principal in principals:
            line = graph.nodes[principal]['line']
            vulnerable: bool = False
            father = list(graph.predecessors(principal))[0]
            condition: int = get_resources(graph, father, 'Condition')
            aws_node: int = helper.get_index(
                get_resources(graph, principal, 'AWS'), 0)

            if aws_node:
                node: int = graph.nodes[aws_node]
                line = node['line']
                if node['value'] == '*' and not condition:
                    vulnerable = True

            if vulnerable:
                vulnerabilities.append(
                    Vulnerability(
                        path=template['path'],
                        entity=f'AWS::KMS::Key',
                        identifier=resource['name'],
                        line=line,
                        reason=('AWS KMS master key must not be '
                                'publicly accessible,')))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Amazon KMS master keys are accessible to all users.',
        msg_closed='Amazon KMS master keys are not accessible to all users.')
