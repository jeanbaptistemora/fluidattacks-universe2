"""
AWS CloudFormation checks for ``EC2`` (Elastic Cloud Compute).
"""
# pylint: disable=bad-continuation

# Standard imports
from contextlib import suppress
from typing import List, Tuple, Dict, Set, Union, Optional

# Treed imports
from networkx.algorithms import dfs_preorder_nodes
from networkx import DiGraph

# Local imports
from fluidasserts import MEDIUM
from fluidasserts import LOW
from fluidasserts import SAST
from fluidasserts.helper.aws import CloudFormationInvalidTypeError
from fluidasserts.cloud.aws.cloudformation import get_predecessor
from fluidasserts.cloud.aws.cloudformation import get_ref_nodes
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import get_graph
from fluidasserts.cloud.aws.cloudformation import get_type
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


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_ports(
        path: str, exclude: Optional[Tuple[str]] = None) -> Tuple:
    """
    Avoid ``EC2::SecurityGroup`` ingress/egress rules with port ranges.

    The following checks are performed:

    * W27 Security Groups found ingress with port range
        instead of just a single port
    * W29 Security Groups found egress with port range
        instead of just a single port

    :param graph: Templates converted into a DiGraph.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph = get_graph(path, exclude)
    vulnerabilities: list = []
    allow_groups: Set[str] = {'SecurityGroupEgress', 'SecurityGroupIngress'}
    # all security groups in templates
    security_groups: List[Dict] = _get_securitygroups(graph, exclude)
    for group in security_groups:
        # node of resource
        resource: Dict = graph.nodes[group['node']]
        # nodes that could be a rule within the security group
        rules: List[int] = list(dfs_preorder_nodes(graph, group['node'], 5))
        for node in [
                x for rule in rules
                for x in dfs_preorder_nodes(graph, rule, 5)
                if not graph.nodes[x]['labels'].intersection(
                    {'FromPort', 'ToPort'})
        ]:
            from_port_node: Union[List[int], int] = [
                x for x in dfs_preorder_nodes(graph, node, 1)
                if 'FromPort' in graph.nodes[x]['labels']
            ]

            to_port_node: Union[List[int], int] = [
                x for x in dfs_preorder_nodes(graph, node, 1)
                if 'ToPort' in graph.nodes[x]['labels']
            ]
            # validate if there are nodes with labels FromPor and ToPort
            if not from_port_node or not to_port_node:
                continue

            # get the FromPort reference if it exists
            from_port_node = get_ref_nodes(
                graph, from_port_node[0],
                lambda x: isinstance(x, (int, float)))[0]
            # get the ToPort reference if it exists
            to_port_node = get_ref_nodes(
                graph, to_port_node[0],
                lambda x: isinstance(x, (int, float)))[0]
            # get the type of rule (SecurityGroupEgress,
            #                           SecurityGroupIngress)
            _type: str = get_type(graph, node, allow_groups) or list(
                group['type'])[-1]
            resource_type: str = [
                res for res in resource['labels']
                if res in {'SecurityGroup', *allow_groups}
            ][-1]
            resource_type = (f'{resource_type}/{_type}'
                             if _type != resource_type else f'{resource_type}')
            entities = []
            from_port: str
            to_port: str
            from_port, to_port = tuple(
                map(str, (graph.nodes[from_port_node]['value'],
                          graph.nodes[to_port_node]['value'])))

            if float(from_port) != float(to_port):
                entities.append(f'{from_port}->{to_port}')

            vulnerabilities.extend(
                Vulnerability(
                    path=graph.nodes[group['template']]['path'],
                    entity=(f"AWS::EC2::{resource_type}/"
                            f"FromPort->ToPort/{entity}"),
                    identifier=resource['name'],
                    line=graph.nodes[from_port_node]['line'],
                    reason='Grants access over a port range')
                for entity in entities)
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=('EC2 security groups have ingress/egress rules '
                  'that allow access over a range of ports'),
        msg_closed=('EC2 security groups have ingress/egress rules '
                    'that allow access over single ports'))


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unencrypted_volumes(connection: ConnectionString) -> tuple:
    """
    Verify if ``EC2::Volume`` has the encryption attribute set to **true**.

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if the volume is not encrypted.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    queries = [
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(
        volume:EC2:Volume)-[rel:HAS*1..3]->(encrypt:Encrypted)
        WHERE encrypt.value = false or encrypt.value = 'false'
        RETURN template.path as path, encrypt.line as line,
          volume.name as resource
        """, """
        MATCH (template:CloudFormationTemplate)-[*2]->(
        volume:EC2:Volume)-[:HAS*1..3]->(encrypt:Encrypted)-[*1..6]->(ref)
        WHERE ref.value = false OR ref.value = 'false'
        WITH DISTINCT ref, template, volume
        RETURN template.path as path, ref.line as line,
          volume.line as resource
        """
    ]
    vulnerabilities: list = []
    session = driver_session(connection)
    for query in queries:
        for record in session.run(query):
            vulnerabilities.append(
                Vulnerability(
                    path=record['path'],
                    entity='AWS::EC2::Volume',
                    identifier=record['resource'],
                    line=record['line'],
                    reason='is not encrypted'))
    session.close()
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 volumes are not encrypted',
        msg_closed='EC2 volumes are encrypted')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_an_iam_instance_profile(
        path: str, exclude: Optional[Tuple[str]] = None) -> Tuple:
    """
    Verify if ``EC2::Instance`` uses an IamInstanceProfile.

    EC2 instances need credentials to access other AWS services.

    An IAM role attached to the instance provides these credentials in a secure
    way. With this, you don't have to manage credentials because they are
    temporarily provided by the IAM Role and are rotated automatically.

    See: https://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide
    /iam-roles-for-amazon-ec2.html

    :param graph: Templates converted into a DiGraph.
    :returns: - ``OPEN`` if the instance has not attached an
                IamInstanceProfile.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph = get_graph(path, exclude)
    templates = get_templates(graph, exclude)
    vulnerabilities: List[Vulnerability] = []
    instances: List[int] = [node for template, _ in templates
                            for node in dfs_preorder_nodes(graph, template, 2)
                            if len(graph.nodes[node]['labels'].intersection(
                                {'AWS', 'EC2', 'Instance'})) > 2]
    for instance in instances:
        instance_node = graph.nodes[instance]
        profile = [node for node in dfs_preorder_nodes(graph, instance, 3)
                   if 'IamInstanceProfile' in graph.nodes[node]['labels']]
        if not profile:
            template = graph.nodes[get_predecessor(
                graph, instance, 'CloudFormationTemplate')]
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity='AWS::EC2::Instance/IamInstanceProfile',
                    identifier=instance_node['name'],
                    line=instance_node['line'],
                    reason='is not present'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 instances have not an IamInstanceProfile set',
        msg_closed='EC2 instances have an IamInstanceProfile set')


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
