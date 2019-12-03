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
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::ElasticLoadBalancingV2::LoadBalancer',
            ],
            exclude=exclude):
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
                            f'/LoadBalancerAttributes',
                            f'/access_logs.s3.enabled',
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
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::ElasticLoadBalancingV2::LoadBalancer',
            ],
            exclude=exclude):
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
                            f'/LoadBalancerAttributes',
                            f'/deletion_protection.enabled',
                            f'/{deletion_protection}'),
                    identifier=res_name,
                    reason='has not deletion protection'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Elastic Load Balancers have not deletion protection',
        msg_closed='Elastic Load Balancers have deletion protection')
