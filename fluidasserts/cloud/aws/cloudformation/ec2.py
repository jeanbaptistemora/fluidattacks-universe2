"""
AWS CloudFormation checks for ``EC2`` (Elastic Cloud Compute).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/master/LICENSE.md>`_
"""

# Standard imports
import ipaddress
import contextlib
from typing import List, Optional

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


def _iterate_security_group_rules(
        path: str, exclude: Optional[List[str]] = None):
    """Iterate over the different security groups entities in the template."""
    for yaml_path, sg_name, sg_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::SecurityGroup',
            ],
            exclude=exclude):
        sg_type = sg_props['../Type']
        for sg_flow in ('SecurityGroupEgress', 'SecurityGroupIngress'):
            for sg_rule in sg_props.get(sg_flow, []):
                sg_path = f'{sg_type}/{sg_flow}'
                yield yaml_path, sg_name, sg_rule, sg_path, sg_flow

    for yaml_path, sg_name, sg_rule in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::SecurityGroupEgress',
                'AWS::EC2::SecurityGroupIngress',
            ],
            exclude=exclude):
        sg_path = sg_rule['../Type']
        sg_flow = sg_path.replace('AWS::EC2::', '')
        yield yaml_path, sg_name, sg_rule, sg_path, sg_flow


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def allows_all_outbound_traffic(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
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

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::SecurityGroup',
            ],
            exclude=exclude):
        security_groups_egress = res_props.get('SecurityGroupEgress', [])

        if not security_groups_egress:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity='AWS::EC2::SecurityGroup',
                    identifier=res_name,
                    reason='allows all outbound traffic'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 security groups allows all outbound traffic',
        msg_closed='EC2 security groups do not allow all outbound traffic')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_cidrs(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``EC2::SecurityGroup`` has ``0.0.0.0/0`` or ``::/0`` CIDRs.

    The following checks are performed:

    * W2 Security Groups found with cidr open to world on ingress
    * W5 Security Groups found with cidr open to world on egress
    * W9 Security Groups found with ingress cidr that is not /32

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    unrestricted_ipv4 = ipaddress.IPv4Network('0.0.0.0/0')
    unrestricted_ipv6 = ipaddress.IPv6Network('::/0')
    for yaml_path, sg_name, sg_rule, sg_path, _ in \
            _iterate_security_group_rules(path, exclude):
        entities = []

        with contextlib.suppress(KeyError,
                                 ValueError,
                                 ipaddress.AddressValueError):
            ipv4 = sg_rule['CidrIp']
            ipv4_obj = ipaddress.IPv4Network(ipv4, strict=False)
            if ipv4_obj == unrestricted_ipv4:
                entities.append(
                    (f'CidrIp/{ipv4}', 'must not be 0.0.0.0/0'))
            if 'SecurityGroupIngress' in sg_path \
                    and ipv4_obj.num_addresses > 1:
                entities.append(
                    (f'CidrIp/{ipv4}', 'must use /32 subnet mask'))

        with contextlib.suppress(KeyError,
                                 ValueError,
                                 ipaddress.AddressValueError):
            ipv6 = sg_rule['CidrIpv6']
            ipv6_obj = ipaddress.IPv6Network(ipv6, strict=False)
            if ipv6_obj == unrestricted_ipv6:
                entities.append(
                    (f'CidrIpv6/{ipv6}', 'must not be ::/0'))
            if 'SecurityGroupIngress' in sg_path \
                    and ipv6_obj.num_addresses > 1:
                entities.append(
                    (f'CidrIpv6/{ipv6}', 'must use /32 subnet mask'))

            vulnerabilities.extend(
                Vulnerability(
                    path=yaml_path,
                    entity=f'{sg_path}/{entity}',
                    identifier=sg_name,
                    reason=reason)
                for entity, reason in entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 security groups have unrestricted CIDRs',
        msg_closed='EC2 security groups do not have unrestricted CIDRs')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_ip_protocols(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Avoid ``EC2::SecurityGroup`` ingress/egress rules with any ip protocol.

    The following checks are performed:

    * W40 Security Groups egress with an IpProtocol of -1 found
    * W42 Security Groups ingress with an ipProtocol of -1 found

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, sg_name, sg_rule, sg_path, _ in \
            _iterate_security_group_rules(path, exclude):
        entities = []
        with contextlib.suppress(KeyError):
            ip_protocol = sg_rule['IpProtocol']
            if ip_protocol in (-1, '-1'):
                entities.append(ip_protocol)

        vulnerabilities.extend(
            Vulnerability(
                path=yaml_path,
                entity=f'{sg_path}/IpProtocol/{entity}',
                identifier=sg_name,
                reason='Authorize all IP protocols')
            for entity in entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=('EC2 security groups have ingress/egress rules '
                  'with unrestricted IP protocols'),
        msg_closed=('EC2 security groups do not have ingress/egress rules '
                    'with unrestricted IP protocols'))


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_ports(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Avoid ``EC2::SecurityGroup`` ingress/egress rules with port ranges.

    The following checks are performed:

    * W27 Security Groups found ingress with port range
        instead of just a single port
    * W29 Security Groups found egress with port range
        instead of just a single port

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, sg_name, sg_rule, sg_path, _ in \
            _iterate_security_group_rules(path, exclude):

        entities = []

        with contextlib.suppress(KeyError):
            from_port, to_port = tuple(map(
                str, (sg_rule['FromPort'], sg_rule['ToPort'])))
            if from_port != to_port:
                entities.append(f'{from_port}->{to_port}')

        vulnerabilities.extend(
            Vulnerability(
                path=yaml_path,
                entity=f'{sg_path}/FromPort->ToPort/{entity}',
                identifier=sg_name,
                reason='Grants access over a port range')
            for entity in entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=('EC2 security groups have ingress/egress rules '
                  'that allow access over a range of ports'),
        msg_closed=('EC2 security groups have ingress/egress rules '
                    'that allow access over single ports'))
