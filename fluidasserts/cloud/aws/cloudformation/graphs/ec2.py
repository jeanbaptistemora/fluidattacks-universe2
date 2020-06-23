"""
AWS CloudFormation checks for ``EC2`` (Elastic Cloud Compute).
"""
# pylint: disable=bad-continuation

# Standard imports
from contextlib import suppress
from typing import List, Tuple, Dict, Set, Optional

# Treed imports
from networkx.algorithms import dfs_preorder_nodes
from networkx import DiGraph

# Local imports
from fluidasserts import MEDIUM
from fluidasserts import LOW
from fluidasserts import SAST
from fluidasserts.helper.aws import CloudFormationInvalidTypeError
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import _get_result_as_tuple
from fluidasserts.cloud.aws.cloudformation import Vulnerability
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.db.neo4j_connection import ConnectionString
from fluidasserts.db.neo4j_connection import driver_session
from fluidasserts.helper import aws as helper


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


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_termination_protection(connection: ConnectionString) -> tuple:
    """
    Verify if ``EC2`` has not deletion protection enabled.

    By default EC2 Instances can be terminated using the Amazon EC2 console,
    CLI, or API.

    This is not desirable, as terminated instances are deleted from the account
    automatically after some time,
    personal may take-down the service without intention,
    and volumes attached to the instance may be lost and therefore wiped.

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if the instance has not the **DisableApiTermination**
                parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    queries: List[str] = [
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            launch:EC2:LaunchTemplate)
        WHERE NOT exists{ (launch)-[*1..3]->(:DisableApiTermination) }
        RETURN template.path as path, launch.line as line, launch.name
            as resource, 'LaunchTemplate' as type
        """,
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            launch:EC2:LaunchTemplate)-[*1..3]->(
                    termination:DisableApiTermination)
        WHERE  exists(termination.value) AND (termination.value = 'false'
            OR termination.value = false)
        RETURN template.path as path, termination.line as line, launch.name
            as resource, 'LaunchTemplate' as type
        """,
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            launch:EC2:LaunchTemplate)-[*1..3]->(
                    :DisableApiTermination)-[*1..6]->(termination)
        WHERE  exists(termination.value) AND (termination.value = 'false'
            OR termination.value = false)
        RETURN template.path as path, termination.line as line, launch.name
            as resource, 'LaunchTemplate' as type
        """,
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            instance:EC2:Instance)
        WHERE NOT exists{ (instance)-[*1..3]->(:DisableApiTermination)}
        AND NOT exists{(instance)-[*1..4]->()-[*1..3]->(:EC2:LaunchTemplate)}
        RETURN template.path as path, instance.line as line, instance.name
            as resource, 'Instance'  as type
        """,
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            instance:EC2:Instance)-[*1..3]->(
                    termination:DisableApiTermination)
        WHERE  exists(termination.value) AND (termination.value = 'false'
            OR termination.value = false)
        RETURN template.path as path, termination.line as line, instance.name
            as resource, 'Instance' as type
        """,
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            instance:EC2:Instance)-[*1..3]->(
                    :DisableApiTermination)-[*1..6]->(termination)
        WHERE  exists(termination.value) AND (termination.value = 'false'
            OR termination.value = false)
        RETURN template.path as path, termination.line as line, instance.name
            as resource, 'Instance' as type
        """
    ]
    session = driver_session(connection)
    query_result = [
        record for query in queries
        for record in list(session.run(query))
    ]
    for record in query_result:
        vulnerabilities.append(
            Vulnerability(
                path=record['path'],
                entity=(f'AWS::EC2::{record["type"]}/'
                        'DisableApiTermination/'),
                identifier=record['resource'],
                line=record['line'],
                reason='has not disabled api termination'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 Launch Templates have API termination enabled',
        msg_closed='EC2 Launch Templates have API termination disabled')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_terminate_shutdown_behavior(connection: ConnectionString) -> tuple:
    """
    Verify if ``EC2::LaunchTemplate`` has **Terminate** as Shutdown Behavior.

    By default EC2 Instances can be terminated using the shutdown command,
    from the underlying operative system.

    This is not desirable, as terminated instances are deleted from the account
    automatically after some time,
    personal may take-down the service without intention,
    and volumes attached to the instance may be lost and therefore wiped.

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if the instance has not the
                **InstanceInitiatedShutdownBehavior** attribute set to
                **terminate**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    queries = [
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            launch:EC2)
        WHERE launch:LaunchTemplate OR launch:Instance
        MATCH (launch)-[*1..6]->(behavior:InstanceInitiatedShutdownBehavior)
        WHERE behavior.value = 'terminate'
        WITH DISTINCT template, launch, behavior
        RETURN template.path as path, behavior.line as line, launch.name
            as resource, [x IN labels(launch) WHERE x IN [
              'Instance', 'LaunchTemplate']][0] as type
        """, """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            launch:EC2)
        WHERE launch:LaunchTemplate OR launch:Instance
        MATCH (launch)-[*1..6]->(
            :InstanceInitiatedShutdownBehavior)-[*1..3]->(behavior)
        WHERE behavior.value = 'terminate'
        WITH DISTINCT template, launch, behavior
        RETURN template.path as path, behavior.line as line, launch.name
            as resource, [x IN labels(launch) WHERE x IN [
              'Instance', 'LaunchTemplate']][0] as type
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
                entity=(f'AWS::EC2::{record["type"]}/'
                        'InstanceInitiatedShutdownBehavior/'),
                identifier=record['resource'],
                line=record['line'],
                reason='has -terminate- as shutdown behavior'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=('EC2 Launch Templates allows the shutdown command to'
                  ' terminate the instance'),
        msg_closed=('EC2 Launch Templates disallow the shutdown command to'
                    ' terminate the instance'))


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def is_associate_public_ip_address_enabled(
        connection: ConnectionString) -> tuple:
    """
    Verify if ``EC2::Instance`` has **NetworkInterfaces** with public IPs.

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if instance's **NetworkInterfaces** attribute has the
                **AssociatePublicIpAddress** parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    queries = [
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            instance:EC2:Instance)-[*1..3]->(:NetworkInterfaces)-[*1..3]->(
                ip:AssociatePublicIpAddress)
        WHERE exists(ip.value)
        RETURN template.tah as path, ip.line as line, instance.name
          as resource, ip.value as ip_value
        """, """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            instance:EC2:Instance)-[*1..3]->(:NetworkInterfaces)-[*1..3]->(
                :AssociatePublicIpAddress)-[*1..6]->(ip)
        WHERE exists(ip.value)
        RETURN template.tah as path, ip.line as line, instance.name
          as resource, ip.value as ip_value
        """
    ]
    session = driver_session(connection)
    query_result = [
        record for query in queries for record in list(session.run(query))
    ]
    for record in query_result:
        public_ip = record['ip_value']
        with suppress(CloudFormationInvalidTypeError):
            public_ip = helper.to_boolean(public_ip)

            if public_ip:
                vulnerabilities.append(
                    Vulnerability(
                        path=record['path'],
                        entity=('AWS::EC2::Instance/'
                                'NetworkInterfaces/'
                                'AssociatePublicIpAddress/'
                                f'{public_ip}'),
                        identifier=record['resource'],
                        line=record['line'],
                        reason='associates public IP on launch'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 instances will be launched with public ip addresses',
        msg_closed='EC2 instances won\'t be launched with public ip addresses')


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
