"""AWS CloudFormation checks for ``ELB`` (Elastic Load Balancing)."""

# Standard imports
import contextlib
from typing import List, Optional

# Treed imports
from networkx import DiGraph

# Local imports
from fluidasserts import SAST, LOW
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


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_access_logging_disabled(path: str,
                                exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``LoadBalancer`` **has Access Logging** disabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **AccessLoggingPolicy/Enabled** attribute is not
                set or set to **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[int] = get_templates(graph, path, exclude)
    balancers: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {'AWS', 'ElasticLoadBalancing', 'LoadBalancer'},
        info=True)
    for balancer, resource, template in balancers:
        line: int = resource['line']
        vulnerable: bool = True
        logging_node: int = helper.get_index(
            get_resources(graph, balancer, 'AccessLoggingPolicy', depth=4), 0)
        if logging_node:
            line = graph.nodes[logging_node]['line']
            enabled_node: int = helper.get_index(
                get_ref_nodes(graph,
                              helper.get_index(
                                  get_resources(graph, logging_node,
                                                'Enabled'), 0)), 0)
            if enabled_node:
                line = graph.nodes[enabled_node]['line']
                with contextlib.suppress(CloudFormationInvalidTypeError):
                    enabled = helper.to_boolean(
                        graph.nodes[enabled_node]['value'])
                    vulnerable = not enabled
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=(f'AWS::ElasticLoadBalancing::LoadBalancer'
                            f'/AccessLoggingPolicy'
                            f'/Enabled'
                            f'/false'),
                    identifier=resource['name'],
                    line=line,
                    reason='access logging is disabled'), )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Elastic Load Balancers have logging disabled',
        msg_closed='Elastic Load Balancers have logging enabled')
