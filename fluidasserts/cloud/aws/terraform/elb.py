"""AWS Terraform checks for ``ELB`` (Elastic Load Balancing)."""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, LOW
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.terraform import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_access_logging_disabled(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``LoadBalancer`` **has Access Logging** disabled.

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **AccessLoggingPolicy/Enabled** attribute is not
                set or set to **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_elb',
            ],
            exclude=exclude):

        is_logging_enabled = helper.to_boolean(
            res_props.get('access_logs', {}).get('enabled', True))

        if not is_logging_enabled:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'aws_elb'
                            f'/access_logs'
                            f'/enabled'
                            f'/{is_logging_enabled}'),
                    identifier=res_name,
                    reason='access logging is disabled'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Elastic Load Balancers have logging disabled',
        msg_closed='Elastic Load Balancers have logging enabled')
