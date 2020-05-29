"""
AWS CloudFormation checks for ``EC2`` (Elastic Cloud Compute).
"""

# Standard imports
import ipaddress

# Local imports
from fluidasserts import MEDIUM
from fluidasserts import SAST
from fluidasserts.cloud.aws.cloudformation import _get_result_as_tuple
from fluidasserts.cloud.aws.cloudformation import Vulnerability
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.db.neo4j_connection import ConnectionString
from fluidasserts.db.neo4j_connection import database, driver_session


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def allows_all_outbound_traffic(connection: ConnectionString) -> tuple:
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
    query = """
        MATCH (template:CloudFormationTemplate)-[*]->(
            group:EC2:SecurityGroup)-[:HAS]->(prop:Properties)
        WHERE NOT EXISTS { (group)-[*]->(:SecurityGroupEgress) } AND
        NOT EXISTS { (:DestinationSecurityGroupId)-[*]->(group) }
        RETURN group.logicalName as resource, template.path as path,
        prop.line as line
     """
    with database(connection) as session:
        for record in session.run(query):
            vulnerabilities.append(
                Vulnerability(
                    path=record['path'],
                    entity='AWS::EC2::SecurityGroup',
                    identifier=record['resource'],
                    line=record['line'],
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
    query_simple = """
        MATCH (template:CloudFormationTemplate)-[*]->(
            group:EC2:SecurityGroup)-[:HAS*]->(rule)
        WHERE rule:SecurityGroupIngress OR rule:SecurityGroupEgress
        MATCH (rule)-[:HAS*]->(ip:CidrIp{version})
        WHERE exists(ip.value)
        RETURN template.path as path, ip.line as line,
          group.logicalName as resource, [x IN labels(rule) WHERE x IN [
              'SecurityGroupEgres', 'SecurityGroupIngress']] [-1] as type,
          ip.value as ip
        """
    query_reference = """
        MATCH (template:CloudFormationTemplate)-[*]->(
            group:EC2:SecurityGroup)-[:HAS*]->(rule)
        WHERE rule:SecurityGroupIngress OR rule:SecurityGroupEgress
        MATCH (rule)-[:HAS*]->(:CidrIp{version})-[*]->(ref_ip)
        WHERE (ref_ip: Default OR ref_ip: MapVar) AND
            exists(ref_ip.value)
        RETURN template.path as path, ref_ip.line as line,
          group.logicalName as resource, [x IN labels(rule) WHERE x IN [
              'SecurityGroupEgres', 'SecurityGroupIngress']] [-1] as type,
          ref_ip.value as ip
        """
    queries_ipv4 = [
        query_simple.format(version=''),
        query_reference.format(version='')]
    queries_ipv6 = [
        query_simple.format(version='v6'),
        query_reference.format(version='v6')]
    session = driver_session(connection)

    for query in queries_ipv4:
        for record in session.run(query):
            entities = []
            ipv4 = record['ip']
            ipv4_obj = ipaddress.IPv4Network(ipv4, strict=False)
            if ipv4_obj == unrestricted_ipv4:
                entities.append(
                    (f'CidrIp/{ipv4}', 'must not be 0.0.0.0/0'))
            if record['type'] == 'SecurityGroupIngress' \
                    and ipv4_obj.num_addresses > 1:
                entities.append(
                    (f'CidrIp/{ipv4}', 'must use /32 subnet mask'))
            vulnerabilities.extend(
                Vulnerability(
                    path=record['path'],
                    entity=(
                        f"AWS::EC2::SecurityGroup/{record['type']}/{entity}')"
                    ),
                    identifier=record['resource'],
                    line=record['line'],
                    reason=reason)
                for entity, reason in entities)
    for query in queries_ipv6:
        for record in session.run(query):
            entities = []
            ipv6 = record['ip']
            ipv6_obj = ipaddress.IPv6Network(ipv6, strict=False)
            if ipv6_obj == unrestricted_ipv6:
                entities.append(
                    (f'CidrIpv6/{ipv6}', 'must not be ::/0'))
            if record['type'] == 'SecurityGroupIngress'\
                    and ipv6_obj.num_addresses > 1:
                entities.append(
                    (f'CidrIpv6/{ipv6}', 'must use /128 subnet mask'))
            vulnerabilities.extend(
                Vulnerability(
                    path=record['path'],
                    entity=f"{record['type']}/{entity}'",
                    identifier=record['resource'],
                    line=record['line'],
                    reason=reason)
                for entity, reason in entities)
    session.close()
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 security groups have unrestricted CIDRs',
        msg_closed='EC2 security groups do not have unrestricted CIDRs')
