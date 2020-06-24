"""
AWS CloudFormation checks for ``EC2`` (Elastic Cloud Compute).
"""
# pylint: disable=bad-continuation

# Standard imports
from typing import List, Tuple, Dict, Set, Optional

# Treed imports
from networkx.algorithms import dfs_preorder_nodes
from networkx import DiGraph

# Local imports
from fluidasserts import MEDIUM
from fluidasserts import SAST
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import _get_result_as_tuple
from fluidasserts.cloud.aws.cloudformation import Vulnerability
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.db.neo4j_connection import ConnectionString
from fluidasserts.db.neo4j_connection import driver_session


def _get_securitygroups(graph: DiGraph,
                        exclude: Optional[List[str]] = None) -> List[Dict]:
    templates: List[Tuple[int, Dict]] = get_templates(graph, exclude)
    allow_groups: Set[str] = {'SecurityGroupEgress', 'SecurityGroupIngress'}
    return [{
        'node': node,
        'template': template,
        'type': graph.nodes[node]['labels'].intersection(allow_groups)
    }
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if graph.nodes[node]['labels'].intersection(
        {'SecurityGroup', *allow_groups})]


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def uses_default_security_group(connection: ConnectionString) -> tuple:
    """
    Verify if ``EC2`` have not **Security Groups** explicitely set.

    By default EC2 Instances that do not specify
    **SecurityGroups** or **SecurityGroupIds** are launched with the default
    security group (allow all).

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if the instance has not the **SecurityGroups** or
                **SecurityGroupIds** parameters set.
                (Either in the **LaunchTemplate** or in the
                **Instance** entities)
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    queries = [
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(launch:EC2)
        WHERE (launch:LaunchTemplate OR launch:Instance)
            AND (NOT exists { (launch)-[*1..6]->(:SecurityGroups) }
                OR NOT exists { (launch)-[*1..6]->(:SecurityGroupIds) })

        RETURN template.path as path, launch.name as resource,
            launch.line as line
        """
    ]
    session = driver_session(connection)
    query_result = [
        record for query in queries for record in list(session.run(query))
    ]
    for record in query_result:
        vulnerabilities.append(
            Vulnerability(
                path=record['path'],
                entity=('AWS::EC2::Instance/'
                        'SecurityGroups(Ids)'),
                identifier=record['resource'],
                line=record['line'],
                reason='is empty, and therefore uses default security group'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=('EC2 Instances or Launch Templates are using the default'
                  ' security group'),
        msg_closed=('EC2 Instances or Launch Templates are not using the '
                    'default security group'))
