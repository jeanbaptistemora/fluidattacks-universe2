"""AWS CloudFormation checks for ``DynamoDB`` (NoSQL Database Service)."""

# Standard imports
from typing import List, Optional, Tuple, Dict

# Treed imports
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
from fluidasserts.cloud.aws.cloudformation import get_ref_nodes
from fluidasserts.cloud.aws.cloudformation import get_resources


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_point_in_time_recovery(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``Table`` has not **Point In Time Recovery** enabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **PointInTimeRecoveryEnabled** attribute is set
                to **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    tables: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates), {'AWS', 'DynamoDB', 'Table'},
        info=True)
    for table, resource, template in tables:
        line = resource['line']
        vulnerable = True
        specify_node = get_resources(graph, table,
                                     'PointInTimeRecoverySpecification')
        enabled_node = helper.get_index(
            get_resources(graph, specify_node, 'PointInTimeRecoveryEnabled'),
            0)
        if enabled_node:
            line = graph.nodes[enabled_node]['line']
            value = get_ref_nodes(graph, enabled_node, helper.is_boolean)
            if value:
                vulnerable = not helper.to_boolean(
                    graph.nodes[value[0]]['value'])

        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity='AWS::DynamoDB::Table',
                    identifier=resource['name'],
                    line=line,
                    reason='is missing Point In Time Recovery'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='DynamoDB tables are missing point in time recovery',
        msg_closed='DynamoDB tables have point in time recovery')
