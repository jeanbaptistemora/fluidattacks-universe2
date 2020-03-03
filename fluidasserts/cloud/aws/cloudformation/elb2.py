"""AWS CloudFormation checks for ``ELB v2`` (Elastic Load Balancing v2)."""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, LOW
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


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
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::ElasticLoadBalancingV2::LoadBalancer',
            ],
            exclude=exclude):
        access_logs = 'false'
        for attribute in res_props.get('LoadBalancerAttributes', [{
                'Key': 'access_logs.s3.enabled',
                'Value': 'false'}]):
            key = attribute.get('Key', 'default')
            if key == 'access_logs.s3.enabled':
                access_logs = attribute.get('Value', 'false')

        if access_logs == 'false':
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'AWS::ElasticLoadBalancingV2::LoadBalancer'
                            f'/LoadBalancerAttributes'
                            f'/access_logs.s3.enabled'
                            f'/{access_logs}'),
                    identifier=res_name,
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
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::ElasticLoadBalancingV2::LoadBalancer',
            ],
            exclude=exclude):
        deletion_protection = 'false'
        for attribute in res_props.get('LoadBalancerAttributes', [{
                'Key': 'deletion_protection.enabled',
                'Value': 'false'}]):
            key = attribute.get('Key', 'default')
            if key == 'deletion_protection.enabled':
                deletion_protection = attribute.get('Value', 'false')

        if deletion_protection == 'false':
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'AWS::ElasticLoadBalancingV2::LoadBalancer'
                            f'/LoadBalancerAttributes'
                            f'/deletion_protection.enabled'
                            f'/{deletion_protection}'),
                    identifier=res_name,
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
                    reason='is not secure'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Target Group does not use secure protocol',
        msg_closed='Target Group uses secure protocol')
