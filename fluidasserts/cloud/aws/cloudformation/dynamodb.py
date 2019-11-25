"""AWS CloudFormation checks for ``DynamoDB`` (NoSQL Database Service)."""

# Standard imports
import contextlib
from typing import List, Optional

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    CloudFormationInvalidTypeError,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_point_in_time_recovery(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``Table`` has not **Point In Time Recovery** enabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **PointInTimeRecoveryEnabled** attribute is set
                to **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::DynamoDB::Table',
            ],
            exclude=exclude):
        point_in_time_recovery = res_props
        point_in_time_recovery = \
            point_in_time_recovery.get('PointInTimeRecoverySpecification', {})
        point_in_time_recovery = \
            point_in_time_recovery.get('PointInTimeRecoveryEnabled', False)

        with contextlib.suppress(CloudFormationInvalidTypeError):
            point_in_time_recovery = helper.to_boolean(point_in_time_recovery)

        is_vulnerable: bool = not point_in_time_recovery

        if is_vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity='AWS::DynamoDB::Table',
                    identifier=res_name,
                    reason='is missing Point In Time Recovery'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='DynamoDB tables are missing point in time recovery',
        msg_closed='DynamoDB tables have point in time recovery')
