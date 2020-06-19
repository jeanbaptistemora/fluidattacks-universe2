"""
AWS CloudFormation checks for ``EC2`` (Elastic Cloud Compute).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

# Standard imports
from ipaddress import IPv4Network, IPv6Network, AddressValueError
import contextlib
from typing import List, Optional, Tuple, Dict, Set, Union

# Treed imports
from networkx import DiGraph
from networkx.algorithms import dfs_preorder_nodes
from networkx.algorithms import all_simple_paths
import networkx as nx

# Local imports
from fluidasserts import SAST, LOW, MEDIUM, HIGH
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import get_graph
from fluidasserts.cloud.aws.cloudformation import get_predecessor
from fluidasserts.cloud.aws.cloudformation import get_ref_nodes
from fluidasserts.cloud.aws.cloudformation import get_type
from fluidasserts.helper.aws import CloudFormationInvalidTypeError
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _index,
    _get_result_as_tuple
)
from fluidasserts.utils.decorators import api, unknown_if


def _iterate_security_group_rules(
        path: str, exclude: Optional[List[str]] = None):
    """Iterate over the different security groups entities in the template."""
    for yaml_path, sg_name, sg_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::SecurityGroup',
            ],
            exclude=exclude):
        sg_type = sg_props['../Type']
        sg_line = helper.get_line(sg_props)
        for sg_flow in ('SecurityGroupEgress', 'SecurityGroupIngress'):
            for sg_rule in sg_props.get(sg_flow, []):
                sg_path = f'{sg_type}/{sg_flow}'
                yield yaml_path, sg_name, sg_rule, sg_path, sg_flow, sg_line

    for yaml_path, sg_name, sg_rule in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::SecurityGroupEgress',
                'AWS::EC2::SecurityGroupIngress',
            ],
            exclude=exclude):
        sg_path = sg_rule['../Type']
        sg_flow = sg_path.replace('AWS::EC2::', '')
        sg_line = helper.get_line(sg_rule)
        yield yaml_path, sg_name, sg_rule, sg_path, sg_flow, sg_line


def _get_securitygroups(graph: DiGraph,
                        exclude: Optional[List[str]] = None) -> List[Dict]:
    templates: List[int] = get_templates(graph, exclude)
    allow_groups: Set[str] = {'SecurityGroupEgress', 'SecurityGroupIngress'}
    return [node
            for template, _ in templates
            for node in dfs_preorder_nodes(graph, template, 2)
            if graph.nodes[node]['labels'].intersection(
                {'SecurityGroup', *allow_groups})]


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def allows_all_outbound_traffic(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
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
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, exclude)
    vulnerabilities: List[Vulnerability] = []
    for template, _ in templates:
        security_groups: List[int] = [
            node for node in dfs_preorder_nodes(graph, template, 2)
            if 'SecurityGroup' in graph.nodes[node]['labels']
        ]
        destination_groups: List[int] = [
            node for group in dfs_preorder_nodes(graph, template, 4)
            if 'SecurityGroupEgress' in graph.nodes[group]['labels']
            for node in dfs_preorder_nodes(graph, group, 3)
            if graph.nodes[node]['labels'].intersection(
                {'DestinationSecurityGroupId', 'GroupId'})
        ]
        group_names: List[str] = [
            graph.nodes[node]['value']
            for group in dfs_preorder_nodes(graph, template, 4)
            if 'SecurityGroupEgress' in graph.nodes[group]['labels']
            for node in dfs_preorder_nodes(graph, group, 3)
            if 'GroupName' in graph.nodes[node]['labels']
        ]
        for group in security_groups:
            _group: Dict = graph.nodes[group]
            group_egress: List[Dict] = [
                graph.nodes[node]
                for node in dfs_preorder_nodes(graph, group, 3)
                if 'SecurityGroupEgress' in graph.nodes[node]['labels']
            ]
            group_destination: List[int] = nx.utils.flatten([
                list(all_simple_paths(graph, node, group))
                for node in destination_groups
            ])

            if not group_egress and not group_destination \
                    and _group['name'] not in group_names:
                path: str = graph.nodes[template]['path']
                resource: Dict = graph.nodes[group]
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
def has_unrestricted_cidrs(path: str,
                           exclude: Optional[List[str]] = None) -> Tuple:
    """
    Check if any ``EC2::SecurityGroup`` has ``0.0.0.0/0`` or ``::/0`` CIDRs.

    The following checks are performed:

    * W2 Security Groups found with cidr open to world on ingress
    * W5 Security Groups found with cidr open to world on egress
    * W9 Security Groups found with ingress cidr that is not /32

    :param graph: Templates converted into a DiGraph.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph: DiGraph = get_graph(path, exclude)
    vulnerabilities: List[Vulnerability] = []
    unrestricted_ipv4 = IPv4Network('0.0.0.0/0')
    unrestricted_ipv6 = IPv6Network('::/0')
    allow_groups = {'SecurityGroupEgress', 'SecurityGroupIngress'}
    security_groups: List[Dict] = _get_securitygroups(graph, exclude)
    for group in security_groups:
        template: Dict = graph.nodes[get_predecessor(graph, group,
                                                     'CloudFormationTemplate')]
        resource: Dict = graph.nodes[group]
        rules: List[Dict] = [
            node for node in dfs_preorder_nodes(graph, group, 3)
            if graph.nodes[node]['labels'].intersection(
                {*allow_groups, 'Properties'})
        ]

        for rule in rules:
            cidr_ips: List[int] = [
                node for node in dfs_preorder_nodes(graph, rule, 3)
                if graph.nodes[node]['labels'].intersection(
                    {'CidrIp', 'CidrIpv6'})
            ]
            ips: List[int] = nx.utils.flatten(
                [get_ref_nodes(graph, node) for node in cidr_ips])
            for _ip in ips:
                entities: List[Tuple] = []
                ip_node: int = graph.nodes[_ip]
                _type: str = get_type(graph, rule, allow_groups)
                resource_type: str = [
                    res for res in resource['labels']
                    if res in {'SecurityGroup', *allow_groups}
                ][-1]
                resource_type = (f'{resource_type}/{_type}'
                                 if _type != resource_type else
                                 f'{resource_type}')

                ip_object: [Union[IPv4Network, IPv6Network]] = None
                ip_type = None
                with contextlib.suppress(AddressValueError):
                    ip_value = ip_node['value']
                    ip_object: IPv4Network = IPv4Network(
                        ip_value, strict=False)
                    ip_type = 'ipv4'
                with contextlib.suppress(AddressValueError):
                    ip_value = ip_node['value']
                    ip_object: IPv6Network = IPv6Network(
                        ip_value, strict=False)
                    ip_type = 'ipv6'

                if ip_type == 'ipv4':
                    if ip_object == unrestricted_ipv4:
                        entities.append((f'CidrIp/{ip_value}',
                                         'must not be 0.0.0.0/0'))
                    if _type == 'SecurityGroupIngress' and \
                            ip_object.num_addresses > 1:
                        entities.append((f'CidrIp/{ip_value}',
                                         'must use /32 subnet mask'))
                if ip_type == 'ipv6':
                    if ip_object == unrestricted_ipv6:
                        entities.append((f'CidrIpv6/{ip_value}',
                                         'must not be ::/0'))
                    if _type == 'SecurityGroupIngress' and \
                            ip_object.num_addresses > 1:
                        entities.append((f'CidrIpv6/{ip_value}',
                                         'must use /128 subnet mask'))

                vulnerabilities.extend(
                    Vulnerability(
                        path=template['path'],
                        entity=f"AWS::EC2::{resource_type}/{entity}'",
                        identifier=resource['name'],
                        line=ip_node['line'],
                        reason=reason) for entity, reason in entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 security groups have unrestricted CIDRs',
        msg_closed='EC2 security groups do not have unrestricted CIDRs')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_ip_protocols(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
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
    for yaml_path, sg_name, sg_rule, sg_path, _, sg_line in \
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
                line=sg_line,
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
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
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
    for yaml_path, sg_name, sg_rule, sg_path, _, sg_line in \
            _iterate_security_group_rules(path, exclude):

        entities = []

        with contextlib.suppress(KeyError, TypeError, ValueError):
            from_port, to_port = tuple(map(
                float, (sg_rule['FromPort'], sg_rule['ToPort'])))
            if from_port != to_port:
                entities.append(f'{from_port}->{to_port}')

        vulnerabilities.extend(
            Vulnerability(
                path=yaml_path,
                entity=f'{sg_path}/FromPort->ToPort/{entity}',
                identifier=sg_name,
                line=sg_line,
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
def has_unencrypted_volumes(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Verify if ``EC2::Volume`` has the encryption attribute set to **true**.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the volume is not encrypted.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::Volume',
            ],
            exclude=exclude):
        if 'Encrypted' not in res_props:
            continue

        with contextlib.suppress(CloudFormationInvalidTypeError):
            if not helper.to_boolean(res_props['Encrypted']):
                vulnerabilities.append(
                    Vulnerability(
                        path=yaml_path,
                        entity='AWS::EC2::Volume',
                        identifier=res_name,
                        line=helper.get_line(res_props),
                        reason='is not encrypted'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 volumes are not encrypted',
        msg_closed='EC2 volumes are encrypted')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_an_iam_instance_profile(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Verify if ``EC2::Instance`` uses an IamInstanceProfile.

    EC2 instances need credentials to access other AWS services.

    An IAM role attached to the instance provides these credentials in a secure
    way. With this, you don't have to manage credentials because they are
    temporarily provided by the IAM Role and are rotated automatically.

    See: https://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide
    /iam-roles-for-amazon-ec2.html

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance has not attached an
                IamInstanceProfile.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::Instance',
            ],
            exclude=exclude):

        if 'IamInstanceProfile' not in res_props:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity='AWS::EC2::Instance/IamInstanceProfile',
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason='is not present'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 instances have not an IamInstanceProfile set',
        msg_closed='EC2 instances have an IamInstanceProfile set')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_termination_protection(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Verify if ``EC2`` has not deletion protection enabled.

    By default EC2 Instances can be terminated using the Amazon EC2 console,
    CLI, or API.

    This is not desirable, as terminated instances are deleted from the account
    automatically after some time,
    personal may take-down the service without intention,
    and volumes attached to the instance may be lost and therefore wiped.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance has not the **DisableApiTermination**
                parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::LaunchTemplate',
            ],
            exclude=exclude):
        disable_api_termination = _index(
            dictionary=res_props,
            indexes=('LaunchTemplateData', 'DisableApiTermination'),
            default=False)

        with contextlib.suppress(CloudFormationInvalidTypeError):
            disable_api_termination = \
                helper.to_boolean(disable_api_termination)

        if not disable_api_termination:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=('AWS::EC2::LaunchTemplate/'
                            'LaunchTemplateData/'
                            'DisableApiTermination/'
                            f'{disable_api_termination}'),
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason='has not disabled api termination'))

    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::Instance',
            ],
            exclude=exclude):
        disable_api_termination = res_props.get('DisableApiTermination', False)

        with contextlib.suppress(CloudFormationInvalidTypeError):
            disable_api_termination = \
                helper.to_boolean(disable_api_termination)

        if not disable_api_termination:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=('AWS::EC2::Instance/'
                            'DisableApiTermination/'
                            f'{disable_api_termination}'),
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason='has not disabled api termination'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 Launch Templates have API termination enabled',
        msg_closed='EC2 Launch Templates have API termination disabled')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_terminate_shutdown_behavior(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Verify if ``EC2::LaunchTemplate`` has **Terminate** as Shutdown Behavior.

    By default EC2 Instances can be terminated using the shutdown command,
    from the underlying operative system.

    This is not desirable, as terminated instances are deleted from the account
    automatically after some time,
    personal may take-down the service without intention,
    and volumes attached to the instance may be lost and therefore wiped.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance has not the
                **InstanceInitiatedShutdownBehavior** attribute set to
                **terminate**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::LaunchTemplate',
            ],
            exclude=exclude):
        initiated_sd_behavior = _index(
            dictionary=res_props,
            indexes=(
                'LaunchTemplateData',
                'InstanceInitiatedShutdownBehavior'),
            default='stop')

        if str(initiated_sd_behavior).lower() == 'terminate':
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=('AWS::EC2::LaunchTemplate/'
                            'LaunchTemplateData/'
                            'InstanceInitiatedShutdownBehavior/'
                            f'{initiated_sd_behavior}'),
                    identifier=res_name,
                    line=helper.get_line(res_props),
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
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Verify if ``EC2::Instance`` has **NetworkInterfaces** with public IPs.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if instance's **NetworkInterfaces** attribute has the
                **AssociatePublicIpAddress** parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::Instance',
            ],
            exclude=exclude):
        for network_interface in res_props.get('NetworkInterfaces', []):
            public_ip = network_interface.get('AssociatePublicIpAddress')

            with contextlib.suppress(CloudFormationInvalidTypeError):
                public_ip = helper.to_boolean(public_ip)

            if public_ip:
                vulnerabilities.append(
                    Vulnerability(
                        path=yaml_path,
                        entity=('AWS::EC2::Instance/'
                                'NetworkInterfaces/'
                                'AssociatePublicIpAddress/'
                                f'{public_ip}'),
                        identifier=res_name,
                        line=helper.get_line(res_props),
                        reason='associates public IP on launch'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EC2 instances will be launched with public ip addresses',
        msg_closed='EC2 instances won\'t be launched with public ip addresses')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def uses_default_security_group(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Verify if ``EC2`` have not **Security Groups** explicitely set.

    By default EC2 Instances that do not specify
    **SecurityGroups** or **SecurityGroupIds** are launched with the default
    security group (allow all).

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance has not the **SecurityGroups** or
                **SecurityGroupIds** parameters set.
                (Either in the **LaunchTemplate** or in the
                **Instance** entities)
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::LaunchTemplate',
            ],
            exclude=exclude):
        launch_template_sgs = _index(
            dictionary=res_props,
            indexes=('LaunchTemplateData', 'SecurityGroups'))
        launch_template_sgs_ids = _index(
            dictionary=res_props,
            indexes=('LaunchTemplateData', 'SecurityGroupIds'))

        if launch_template_sgs or launch_template_sgs_ids:
            # Not vulnerable
            continue

        vulnerabilities.append(
            Vulnerability(
                path=yaml_path,
                entity=('AWS::EC2::LaunchTemplate/'
                        'LaunchTemplateData/'
                        'SecurityGroups(Ids)'),
                identifier=res_name,
                line=helper.get_line(res_props),
                reason='is empty, and therefore uses default security group'))

    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::EC2::Instance',
            ],
            exclude=exclude):
        instance_sgs = res_props.get('SecurityGroups')
        instance_sgs_ids = res_props.get('SecurityGroupIds')

        if instance_sgs or instance_sgs_ids:
            # Not vulnerable
            continue

        vulnerabilities.append(
            Vulnerability(
                path=yaml_path,
                entity=('AWS::EC2::Instance/'
                        'SecurityGroups(Ids)'),
                identifier=res_name,
                line=helper.get_line(res_props),
                reason='is empty, and therefore uses default security group'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=('EC2 Instances or Launch Templates are using the default'
                  ' security group'),
        msg_closed=('EC2 Instances or Launch Templates are not using the '
                    'default security group'))


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def security_group_allows_anyone_to_admin_ports(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Check if ``EC2::SecurityGroup`` allows connection from internet
    to admin services.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    admin_ports = {
        22,  # SSH
        1521,  # Oracle
        2438,  # Oracle
        3306,  # MySQL
        3389,  # RDP
        5432,  # Postgres
        6379,  # Redis
        7199,  # Cassandra
        8111,  # DAX
        8888,  # Cassandra
        9160,  # Cassandra
        11211,  # Memcached
        27017,  # MongoDB
        445,  # CIFS
    }
    vulnerabilities: list = []
    for yaml_path, sg_name, sg_rule, sg_path, _, sg_line in \
            _iterate_security_group_rules(path, exclude):

        entities = []
        with contextlib.suppress(KeyError, TypeError, ValueError):
            from_port, to_port = tuple(map(
                float, (sg_rule['FromPort'], sg_rule['ToPort'])))
            for port in admin_ports:
                if from_port <= port <= to_port \
                        and sg_rule['CidrIp'] == '0.0.0.0/0':
                    entities.append(f'{sg_name}/{port}')

        vulnerabilities.extend(
            Vulnerability(
                path=yaml_path,
                entity=f'{sg_path}/{entity}',
                identifier=sg_name,
                line=sg_line,
                reason='Grants access to admin ports from internet')
            for entity in entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=('EC2 security groups have ingress/egress rules '
                  'that allow access to admin ports over the internet'),
        msg_closed=('EC2 security groups have ingress/egress rules '
                    'that deny access to admin ports over the internet'))


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_dns_access(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Check if inbound rules that allow unrestricted access to port 53.

    TCP/UDP port 53 is used by the Domain Name Service during DNS resolution.
    Restrict access to TCP and UDP port 53 only those IP addresses that
    require, to implement the principle of least privilege and reduce the
    possibility of a attack.

    Allowing unrestricted  to DNS access can give chance of an attack such as
    Denial of Services (DOS) or Distributed Denial of Service Syn Flood (DDoS).

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, sg_name, sg_rule, sg_path, _, sg_line in \
            _iterate_security_group_rules(path, exclude):

        entities = []
        with contextlib.suppress(KeyError, TypeError, ValueError):
            from_port, to_port = tuple(map(
                float, (sg_rule['FromPort'], sg_rule['ToPort'])))
            if from_port <= 53 <= to_port \
                    and sg_rule['CidrIp'] == '0.0.0.0/0':
                entities.append(f'{sg_name}/{53}')

        vulnerabilities.extend(
            Vulnerability(
                path=yaml_path,
                entity=f'{sg_path}/{entity}',
                identifier=sg_name,
                line=sg_line,
                reason=('Group must restrict access to TCP port'
                        ' and UDP 53 to the necessary IP addresses.'))
            for entity in entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Security groups allow access to DNS without restrictions.',
        msg_closed=('Security groups allow access to DNS to'
                    ' the necessary IP addresses.'))


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unrestricted_ftp_access(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Check if security groups allow unrestricted access to TCP ports 20 and 21.

    Restrict access to TCP ports 20 y 21 to only IP addresses that require,
    it in order to implement the principle of least privilege.
    TCP ports 20 and 21 are used for data transfer and communication by the
    File Transfer Protocol (FTP) client-server applications:

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, sg_name, sg_rule, sg_path, _, sg_line in \
            _iterate_security_group_rules(path, exclude):

        entities = []
        with contextlib.suppress(KeyError, TypeError, ValueError):
            from_port, to_port = tuple(map(
                float, (sg_rule['FromPort'], sg_rule['ToPort'])))
            for port in range(20, 22):
                if from_port <= port <= to_port \
                        and sg_rule['CidrIp'] == '0.0.0.0/0'\
                        and str(sg_rule['IpProtocol']) in ('tcp', '-1'):
                    entities.append(f'{sg_name}/{port}')

        vulnerabilities.extend(
            Vulnerability(
                path=yaml_path,
                entity=f'{sg_path}/{entity}',
                identifier=sg_name,
                line=sg_line,
                reason=('Group must restrict access to TCP port'
                        ' 20/21 to the necessary IP addresses.'))
            for entity in entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Security groups allow access to FTP without restrictions.',
        msg_closed=('Security groups allow access to FTP to'
                    ' the necessary IP addresses.'))


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_security_groups_ip_ranges_in_rfc1918(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Check if inbound rules access from IP address ranges specified in RFC-1918.

    Using RFC-1918 CIDRs within your EC2 security groups allow an entire
    private network to access EC2 instancess. Restrict access to only those
    private IP addresses that require, it in order to implement the principle
    of least privilege.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []

    rfc1918 = {'10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', }

    for yaml_path, sg_name, sg_rule, sg_path, _, sg_line in \
            _iterate_security_group_rules(path, exclude):

        entities = []
        with contextlib.suppress(KeyError, TypeError, ValueError):
            if sg_rule['CidrIp'] in rfc1918 \
                    and 'SecurityGroupIngress' in sg_path:
                entities.append(f'{sg_name}')

        vulnerabilities.extend(
            Vulnerability(
                path=yaml_path,
                entity=f'{sg_path}/{entity}',
                identifier=sg_name,
                line=sg_line,
                reason=('Group must restrict access to TCP port'
                        ' 20/21 to the necessary IP addresses.'))
            for entity in entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Security groups contain RFC-1918 CIDRs open.',
        msg_closed='Security groups do not contain RFC-1918 CIDRs open.')


@api(risk=HIGH, kind=SAST)
@unknown_if(FileNotFoundError)
def has_open_all_ports_to_the_public(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Check if security groups has all ports or protocols open to the public..

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List = []
    unrestricted_ipv4 = IPv4Network('0.0.0.0/0')
    unrestricted_ipv6 = IPv6Network('::/0')
    for yaml_path, sg_name, sg_rule, sg_path, _, sg_line in \
            _iterate_security_group_rules(path, exclude):

        entities: List = []

        with contextlib.suppress(KeyError, TypeError, ValueError,
                                 AddressValueError):
            from_port, to_port = tuple(map(
                float, (sg_rule['FromPort'], sg_rule['ToPort'])))
            ipv4: str = sg_rule.get('CidrIp', '')
            ipv6: str = sg_rule.get('CidrIpv6', '')
            if ipv4:
                ipv4_obj: IPv4Network = IPv4Network(ipv4, strict=False)
            else:
                ipv6_obj: IPv6Network = IPv6Network(ipv6, strict=False)
            if (from_port == 1 and to_port == 65535) \
                    and (ipv4_obj == unrestricted_ipv4
                         or ipv6_obj == unrestricted_ipv6):
                entities.append(f'{from_port}->{to_port}')

        vulnerabilities.extend(
            Vulnerability(
                path=yaml_path,
                entity=f'{sg_path}/FromPort->ToPort/{entity}',
                identifier=sg_name,
                line=sg_line,
                reason='Grants public access to all ports')
            for entity in entities)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Security groups has all ports open to the pubic',
        msg_closed='Security groups do not have all ports open to the pubic.')
