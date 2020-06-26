"""AWS CloudFormation checks for ``ELB v2`` (Elastic Load Balancing v2)."""

# Standard imports
from typing import List, Set, Optional, Tuple

# Treed imports
from networkx import DiGraph

# Local imports
from fluidasserts import SAST, LOW
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import get_graph
from fluidasserts.cloud.aws.cloudformation import get_predecessor
from fluidasserts.cloud.aws.cloudformation import get_resources


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_access_logging_disabled(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``LoadBalancers`` have **access_logs.s3.enabled** set to **true**.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if *access_logs.s3.enabled** attribute in the
                **LoadBalancerAttributes** section is not set or **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    graph: DiGraph = get_graph(path, exclude)
    templates = get_templates(graph, path, exclude)
    balancers = get_resources(
        graph, map(lambda x: x[0], templates),
        {'AWS', 'ElasticLoadBalancingV2', 'LoadBalancer'})
    attributes = get_resources(
        graph, balancers, 'LoadBalancerAttributes', depth=3)
    for attr in attributes:
        templates = graph.nodes[get_predecessor(
            graph, attr, 'CloudFormationTemplate')]
        resource = graph.nodes[get_predecessor(graph, attr, 'LoadBalancer')]
        keys = [
            node for node in get_resources(graph, attr, 'Key', depth=3)
            if graph.nodes[node]['value'] == 'access_logs.s3.enabled'
        ]
        vulnerable = True
        if keys:
            key = keys[0]
            father = list(graph.predecessors(key))[0]
            value = [
                node for node in get_resources(graph, father, 'Value')
                if graph.nodes[node]['value'] == 'false'
            ]
            if not value:
                vulnerable = False

        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=templates['path'],
                    entity=(f'AWS::ElasticLoadBalancingV2::LoadBalancer'
                            f'/LoadBalancerAttributes'
                            f'/access_logs.s3.enabled'
                            f'/false'),
                    identifier=resource['name'],
                    line=graph.nodes[value[0]]['line'],
                    reason='has access logging disabled'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Elastic Load Balancers have access logging disabled',
        msg_closed='Elastic Load Balancers have have access logging enabled')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_deletion_protection(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``LoadBalancers`` have **Deletion Protection**.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if *deletion_protection.enabled** attribute in the
                **LoadBalancerAttributes** section is not set or **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    graph: DiGraph = get_graph(path, exclude)
    templates = get_templates(graph, path, exclude)
    balancers = get_resources(
        graph, map(lambda x: x[0], templates),
        {'AWS', 'ElasticLoadBalancingV2', 'LoadBalancer'})
    attributes = get_resources(
        graph, balancers, 'LoadBalancerAttributes', depth=3)
    for attr in attributes:
        template = graph.nodes[get_predecessor(
            graph, attr, 'CloudFormationTemplate')]
        resource = graph.nodes[get_predecessor(graph, attr, 'LoadBalancer')]
        keys = [
            node for node in get_resources(graph, attr, 'Key', depth=3)
            if graph.nodes[node]['value'] == 'deletion_protection.enabled'
        ]
        vulnerable = True
        if keys:
            key = keys[0]
            father = list(graph.predecessors(key))[0]
            value = [
                node for node in get_resources(graph, father, 'Value')
                if graph.nodes[node]['value'] == 'false'
            ]
            if not value:
                vulnerable = False
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=(f'AWS::ElasticLoadBalancingV2::LoadBalancer'
                            f'/LoadBalancerAttributes'
                            f'/deletion_protection.enabled'
                            f'/false'),
                    identifier=resource['name'],
                    line=graph.nodes[value[0]]['line'],
                    reason='has not deletion protection'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Elastic Load Balancers have not deletion protection',
        msg_closed='Elastic Load Balancers have deletion protection')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def uses_insecure_port(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``TargetGroup`` uses **Port 443**.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if *Port** attribute in the
                **LoadBalancerAttributes** section is not **443**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    safe_ports = (443,)
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::ElasticLoadBalancingV2::TargetGroup',
            ],
            exclude=exclude):

        port = int(res_props.get('Port', 80))
        unsafe_port = port not in safe_ports

        is_port_required = not res_props.get('TargetType', '') == 'lambda'

        if is_port_required and unsafe_port:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'AWS::ElasticLoadBalancingV2::TargetGroup'
                            f'/Port'
                            f'/{port}'),
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason='is not secure'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Target Group does not use secure port',
        msg_closed='Target Group uses secure port')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def uses_insecure_protocol(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``TargetGroup`` uses **HTTP** protocol.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if *Port** attribute in the
                **LoadBalancerAttributes** section is not **443**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    unsafe_protos = ('HTTP',)
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::ElasticLoadBalancingV2::TargetGroup',
            ],
            exclude=exclude):

        proto = res_props.get('Protocol', 'HTTP')
        unsafe_proto = proto in unsafe_protos

        is_proto_required = not res_props.get('TargetType', '') == 'lambda'

        if is_proto_required and unsafe_proto:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'AWS::ElasticLoadBalancingV2::TargetGroup'
                            f'/protocol'
                            f'/{proto}'),
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason='is not secure'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Target Group does not use secure protocol',
        msg_closed='Target Group uses secure protocol')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def uses_insecure_security_policy(
        path: str, exclude: Optional[List[str]] = None) -> Tuple:
    """
    Check if Listeners uses unsafe security policy.

    https://www.cloudconformity.com/knowledge-base/aws/ELBv2/
    network-load-balancer-security-policy.html#

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if *SSLPolicy** attribute in the
                **Listener** is insecure.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    acceptable: Set = {'ELBSecurityPolicy-2016-08',
                       'ELBSecurityPolicy-TLS-1-1-2017-01',
                       'ELBSecurityPolicy-FS-2018-06',
                       'ELBSecurityPolicy-TLS-1-2-Ext-2018-06'}
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::ElasticLoadBalancingV2::Listener',
            ],
            exclude=exclude):

        policy: str = res_props.get('SslPolicy', '')
        if policy not in acceptable:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'AWS::ElasticLoadBalancingV2::Listener'
                            f'/{policy}'),
                    identifier=res_name,
                    line=helper.get_line(res_props),
                    reason='is not secure'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='ELB Load Balancers implement insecure security policy',
        msg_closed=('ELB Load Balancers do not implement '
                    'insecure security policy'))
