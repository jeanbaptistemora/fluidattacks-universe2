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


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def allows_all_outbound_traffic(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``EC2::SecurityGroup`` allows all outbound traffic.

    The following checks are performed:

    - F1000 Missing egress rule means all traffic is allowed outbound.
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

    - W2 Security Groups found with cidr open to world on ingress
    - W5 Security Groups found with cidr open to world on egress
    - W9 Security Groups found with ingress cidr that is not /32

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
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::SecurityGroup',
            ],
            exclude=exclude):
        entities = []
        for attribute in ('SecurityGroupEgress',
                          'SecurityGroupIngress'):
            for security_group in res_props.get(attribute, []):
                with contextlib.suppress(KeyError,
                                         ValueError,
                                         ipaddress.AddressValueError):
                    ipv4 = security_group['CidrIp']
                    ipv4_obj = ipaddress.IPv4Network(ipv4, strict=False)
                    if ipv4_obj == unrestricted_ipv4:
                        entities.append((ipv4, 'must not be 0.0.0.0/0'))
                    if attribute == 'SecurityGroupIngress' \
                            and ipv4_obj.num_addresses > 1:
                        entities.append((ipv4, 'must use /32 subnet mask'))

                with contextlib.suppress(KeyError,
                                         ValueError,
                                         ipaddress.AddressValueError):
                    ipv6 = security_group['CidrIpv6']
                    ipv6_obj = ipaddress.IPv6Network(ipv6, strict=False)
                    if ipv6_obj == unrestricted_ipv6:
                        entities.append((ipv6, 'must not be ::/0'))
                    if attribute == 'SecurityGroupIngress' \
                            and ipv6_obj.num_addresses > 1:
                        entities.append((ipv6, 'must use /32 subnet mask'))

        vulnerabilities.extend(
            Vulnerability(
                path=yaml_path,
                entity=f'AWS::EC2::SecurityGroup/{entity}',
                identifier=res_name,
                reason=reason)
            for entity, reason in entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 security groups have unrestricted CIDRs',
        msg_closed='EC2 security groups do not have unrestricted CIDRs')
