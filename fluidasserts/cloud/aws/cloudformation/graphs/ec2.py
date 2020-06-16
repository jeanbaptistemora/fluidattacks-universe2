"""
AWS CloudFormation checks for ``EC2`` (Elastic Cloud Compute).
"""

# Standard imports
import ipaddress
from contextlib import suppress
from typing import List

# Treed imports
from networkx.algorithms import dfs_preorder_nodes
from networkx.algorithms import all_simple_paths
import networkx as nx
from networkx import DiGraph

# Local imports
from fluidasserts import MEDIUM
from fluidasserts import LOW
from fluidasserts import SAST
from fluidasserts.cloud.aws.cloudformation import (
    CloudFormationInvalidTypeError)
from fluidasserts.cloud.aws.cloudformation import _get_result_as_tuple
from fluidasserts.cloud.aws.cloudformation import Vulnerability
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.db.neo4j_connection import ConnectionString
from fluidasserts.db.neo4j_connection import driver_session
from fluidasserts.helper import aws as helper


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def allows_all_outbound_traffic(graph: DiGraph) -> tuple:
    """
    Check if any ``EC2::SecurityGroup`` allows all outbound traffic.

    The following checks are performed:

    * F1000 Missing egress rule means all traffic is allowed outbound,
        Make this explicit if it is desired configuration

    When you specify a VPC security group, Amazon EC2 creates a
    **default egress rule** that **allows egress traffic** on **all ports
    and IP protocols to any location**.

    The default rule is removed only when you specify one or more egress
    rules in the **SecurityGroupEgress** directive.

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    templates: List[int] = [
        _id for _id, node in graph.nodes.data()
        if node['kind'] == 'CloudFormationTemplate'
    ]
    for template in templates:
        security_groups = [
            node for node in dfs_preorder_nodes(graph, template, 2)
            if graph.nodes[node]['kind'] == 'SecurityGroup'
        ]
        destination_groups = [
            node for group in dfs_preorder_nodes(graph, template, 4)
            if graph.nodes[group]['kind'] == 'SecurityGroupEgress'
            for node in dfs_preorder_nodes(graph, group, 3) if graph.nodes[
                node]['kind'] in ['DestinationSecurityGroupId', 'GroupId']
        ]
        group_names = [
            graph.nodes[node]['value']
            for group in dfs_preorder_nodes(graph, template, 4)
            if graph.nodes[group]['kind'] == 'SecurityGroupEgress'
            for node in dfs_preorder_nodes(graph, group, 3)
            if graph.nodes[node]['kind'] == 'GroupName'
        ]
        for group in security_groups:
            _group = graph.nodes[group]
            group_egress = [
                graph.nodes[node]
                for node in dfs_preorder_nodes(graph, group, 3)
                if graph.nodes[node]['kind'] == 'SecurityGroupEgress'
            ]
            group_destination = nx.utils.flatten([
                list(all_simple_paths(graph, node, group))
                for node in destination_groups
            ])

            if not group_egress and not group_destination \
                    and _group['name'] not in group_names:
                path = graph.nodes[template]['path']
                resource = graph.nodes[group]
                vulnerabilities.append(
                    Vulnerability(
                        path=path,
                        entity='AWS::EC2::SecurityGroup',
                        identifier=resource['name'],
                        line=resource['line'],
                        reason='allows all outbound traffic'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 security groups allows all outbound traffic',
        msg_closed='EC2 security groups do not allow all outbound traffic')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_cidrs(connection: ConnectionString) -> tuple:
    """
    Check if any ``EC2::SecurityGroup`` has ``0.0.0.0/0`` or ``::/0`` CIDRs.

    The following checks are performed:

    * W2 Security Groups found with cidr open to world on ingress
    * W5 Security Groups found with cidr open to world on egress
    * W9 Security Groups found with ingress cidr that is not /32

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    unrestricted_ipv4 = ipaddress.IPv4Network('0.0.0.0/0')
    unrestricted_ipv6 = ipaddress.IPv6Network('::/0')
    queries = [
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            group:EC2:SecurityGroup)-[*1..3]->(rule)
        WHERE rule:SecurityGroupIngress OR rule:SecurityGroupEgress
        MATCH (rule)-[:HAS*1..3]->(ip:CidrIp{version})
        WHERE exists(ip.value)
        WITH DISTINCT group, template, rule, ip
        RETURN template.path as path, ip.line as line,
          group.name as resource, [x IN labels(rule) WHERE x IN [
              'SecurityGroupEgress', 'SecurityGroupIngress']] [-1] as type,
          ip.value as ip
        """, """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            group:EC2:SecurityGroup)-[*1..3]->(rule)
        WHERE rule:SecurityGroupIngress OR rule:SecurityGroupEgress
        MATCH (rule)-[:HAS*1..3]->(:CidrIp{version})-[*1..6]->(ref_ip)
        WHERE exists(ref_ip.value)
        WITH DISTINCT group, template, rule, ref_ip
        RETURN template.path as path, ref_ip.line as line,
          group.name as resource, [x IN labels(rule) WHERE x IN [
              'SecurityGroupEgress', 'SecurityGroupIngress']] [-1] as type,
          ref_ip.value as ip
        """, """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            group:EC2:SecurityGroup)<-[*1..6]-(rule)-[*1..6]-(
                ip:CidrIp{version})
        WHERE (
            rule:SecurityGroupIngress OR rule:SecurityGroupEgress) AND exists(
                ip.value)
        WITH DISTINCT group, template, rule, ip
        RETURN template.path as path,
          group.name as resource, [x IN labels(rule) WHERE x IN [
              'SecurityGroupEgress', 'SecurityGroupIngress']][0] as type,
          ip.value as ip, ip.line as line
        """, """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            group:EC2:SecurityGroup)<-[*1..4]-(rule)-[*1..6]-(
                ip:CidrIp)-[*1..6]->(ref_ip)
        WHERE (
            rule:SecurityGroupIngress OR rule:SecurityGroupEgress)
             AND exists(ref_ip.value)
        WITH DISTINCT group, template, rule, ref_ip
        RETURN template.path as path,
          group.name as resource, [x IN labels(rule) WHERE x IN [
              'SecurityGroupEgress', 'SecurityGroupIngress']][0]  as type,
          ref_ip.value as ip,  ref_ip.line as line
        """
    ]
    queries_ipv4 = [query.format(version='') for query in queries]
    queries_ipv6 = [query.format(version='v6') for query in queries]
    session = driver_session(connection)
    query_result = [
        record for query in queries_ipv4
        for record in list(session.run(query))
    ]
    for record in query_result:
        entities = []
        ipv4 = record['ip']
        with suppress(ipaddress.AddressValueError):
            ipv4_obj = ipaddress.IPv4Network(ipv4, strict=False)

            if ipv4_obj == unrestricted_ipv4:
                entities.append((f'CidrIp/{ipv4}', 'must not be 0.0.0.0/0'))
            if record['type'] == 'SecurityGroupIngress' \
                    and ipv4_obj.num_addresses > 1:
                entities.append((f'CidrIp/{ipv4}', 'must use /32 subnet mask'))
            vulnerabilities.extend(
                Vulnerability(
                    path=record['path'],
                    entity=(
                        f"AWS::EC2::SecurityGroup/{record['type']}/{entity}')"
                    ),
                    identifier=record['resource'],
                    line=record['line'],
                    reason=reason) for entity, reason in entities)
    query_result = [
        record for query in queries_ipv6
        for record in list(session.run(query))
    ]
    for record in query_result:
        entities = []
        ipv6 = record['ip']
        with suppress(ipaddress.AddressValueError):
            ipv6_obj = ipaddress.IPv6Network(ipv6, strict=False)
            if ipv6_obj == unrestricted_ipv6:
                entities.append((f'CidrIpv6/{ipv6}', 'must not be ::/0'))
            if record['type'] == 'SecurityGroupIngress' \
                    and ipv6_obj.num_addresses > 1:
                entities.append((f'CidrIpv6/{ipv6}',
                                 'must use /128 subnet mask'))
            vulnerabilities.extend(
                Vulnerability(
                    path=record['path'],
                    entity=f"{record['type']}/{entity}'",
                    identifier=record['resource'],
                    line=record['line'],
                    reason=reason) for entity, reason in entities)
    session.close()
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 security groups have unrestricted CIDRs',
        msg_closed='EC2 security groups do not have unrestricted CIDRs')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_ip_protocols(connection: ConnectionString) -> tuple:
    """
    Avoid ``EC2::SecurityGroup`` ingress/egress rules with any ip protocol.

    The following checks are performed:

    * W40 Security Groups egress with an IpProtocol of -1 found
    * W42 Security Groups ingress with an ipProtocol of -1 found

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    queries = [
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(group)
        WHERE group:SecurityGroupIngress OR group:SecurityGroupEgress OR
            group:SecurityGroup
        MATCH (group)-[:HAS*1..6]->(ip:IpProtocol)
        WHERE ip.value = -1 OR ip.value = '-1'
        RETURN template.path as path, ip.line as line,
          group.name as resource, [x IN labels(group) WHERE x IN [
              'SecurityGroupEgress', 'SecurityGroupIngress']][0]  as type,
          ip.value as ipProtocol
        """, """
        MATCH (template:CloudFormationTemplate)-[*2]->(
            group)-[:HAS*1..6]->(rule)
        WHERE group:SecurityGroupIngress OR group:SecurityGroupEgress OR
            group:SecurityGroup
        MATCH (rule)-[:HAS*]->(:IpProtocol)-[:REFERENCE]->(
            )-[:HAS*1..3]->(proto)
        WHERE exists(proto.value) AND
            (proto.value = -1 OR proto.value = '-1')
        RETURN template.path as path, proto.line as line,
          group.name as resource, [x IN labels(rule) WHERE x IN [
              'SecurityGroupEgress', 'SecurityGroupIngress']][0]  as type,
          proto.value as ipProtocol
        """
    ]
    session = driver_session(connection)

    for query in queries:
        for record in session.run(query):
            vulnerabilities.append(
                Vulnerability(
                    path=record['path'],
                    entity=(f"AWS::EC2::{record['type']}/IpProtocol/"
                            f"{record['ipProtocol']}"),
                    identifier=record['resource'],
                    line=record['line'],
                    reason='Authorize all IP protocols'))
    session.close()

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=('EC2 security groups have ingress/egress rules '
                  'with unrestricted IP protocols'),
        msg_closed=('EC2 security groups do not have ingress/egress rules '
                    'with unrestricted IP protocols'))


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_ports(connection: ConnectionString) -> tuple:
    """
    Avoid ``EC2::SecurityGroup`` ingress/egress rules with port ranges.

    The following checks are performed:

    * W27 Security Groups found ingress with port range
        instead of just a single port
    * W29 Security Groups found egress with port range
        instead of just a single port

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    queries = [
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(group)-[*1..5]->()-[
            *1]->(rule)
        WHERE group:SecurityGroupIngress OR group:SecurityGroupEgress OR
            group:SecurityGroup
        MATCH (rule)-[*1]->(:FromPort)-[:REFERENCE]->(
            )-[:HAS*1..3]->(from), (rule)-[*1]->(:ToPort)-[:REFERENCE]->(
            )-[:HAS*1..3]->(to)
        WHERE toInteger(from.value) <> toInteger(to.value)
        WITH DISTINCT rule, template, group, from, to
        RETURN template.path as path, from.line as line,
          group.name as resource, [x IN labels(group) WHERE x IN [
              'SecurityGroupEgress', 'SecurityGroupIngress',
              'SecurityGroup']][0]  as type,
           from.value as fromPort, to.value as toPort
        """,
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(group)-[*1..5]->()-[
            *1]->(rule)
        WHERE group:SecurityGroupIngress OR group:SecurityGroupEgress OR
            group:SecurityGroup
        MATCH (rule)-[*1]->(from:FromPort), (rule)-[*1]->(to:ToPort)
        WHERE toInteger(from.value) <> toInteger(to.value)
        WITH DISTINCT rule, template, group, from, to
        RETURN template.path as path, from.line as line,
          group.name as resource, [x IN labels(group) WHERE x IN [
              'SecurityGroupEgress', 'SecurityGroupIngress',
              'SecurityGroup']][0]  as type,
           from.value as fromPort, to.value as toPort
        """
    ]
    session = driver_session(connection)
    vulnerabilities: list = []
    for query in queries:
        for record in session.run(query):
            entities = []
            from_port, to_port = tuple(map(
                str, (record['fromPort'], record['toPort'])))

            if float(from_port) != float(to_port):
                entities.append(f'{from_port}->{to_port}')

            vulnerabilities.extend(
                Vulnerability(
                    path=record['path'],
                    entity=(f"AWS::EC2::{record['type']}/"
                            f"FromPort->ToPort/{entity}"),
                    identifier=record['resource'],
                    line=record['line'],
                    reason='Grants access over a port range')
                for entity in entities)
    session.close()
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
def has_not_an_iam_instance_profile(connection: ConnectionString) -> tuple:
    """
    Verify if ``EC2::Instance`` uses an IamInstanceProfile.

    EC2 instances need credentials to access other AWS services.

    An IAM role attached to the instance provides these credentials in a secure
    way. With this, you don't have to manage credentials because they are
    temporarily provided by the IAM Role and are rotated automatically.

    See: https://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide
    /iam-roles-for-amazon-ec2.html

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if the instance has not attached an
                IamInstanceProfile.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    query = """
        MATCH (template:CloudFormationTemplate)-[*2]->(
           instance:EC2:Instance)
        WHERE NOT EXISTS {(instance)-[*1..3]-(:IamInstanceProfile)}
        RETURN template.path as path, instance.line as line,
             instance.name as resource
       """
    session = driver_session(connection)
    for record in session.run(query):
        vulnerabilities.append(
            Vulnerability(
                path=record['path'],
                entity='AWS::EC2::Instance/IamInstanceProfile',
                identifier=record['resource'],
                line=record['line'],
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
