"""AWS CloudFormation checks for ``ELB`` (Elastic Load Balancing)."""

# Standard imports
import contextlib
from typing import List, Optional

# Local imports
from fluidasserts import SAST, LOW
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    CloudFormationInvalidTypeError,
    _index,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_access_logging_disabled(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``LoadBalancer`` **has Access Logging** disabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **AccessLoggingPolicy/Enabled** attribute is not
                set or set to **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::ElasticLoadBalancing::LoadBalancer',
            ],
            exclude=exclude):
        is_logging_enabled = _index(
            dictionary=res_props,
            indexes=('AccessLoggingPolicy', 'Enabled'),
            default=False)

        with contextlib.suppress(CloudFormationInvalidTypeError):
            is_logging_enabled = helper.to_boolean(is_logging_enabled)

        if not is_logging_enabled:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'AWS::ElasticLoadBalancing::LoadBalancer'
                            f'/AccessLoggingPolicy'
                            f'/Enabled'
                            f'/{is_logging_enabled}'),
                    identifier=res_name,
                    reason='access logging is disabled'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Elastic Load Balancers have logging disabled',
        msg_closed='Elastic Load Balancers have logging enabled')
