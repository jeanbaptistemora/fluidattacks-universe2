"""AWS CloudFormation checks for ``S3`` (Simple Storage Service)."""

# Standard imports
from typing import List, NoReturn, Optional, Set

# Local imports
from fluidasserts import SAST, HIGH
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


#: A set of available S3 Access Controls
ACCESS_CONTROLS = {
    'Private',
    'PublicRead',
    'PublicReadWrite',
    'AuthenticatedRead',
    'BucketOwnerRead',
    'BucketOwnerFullControl',
    'LogDeliveryWrite',
}


def _validate_access_controls(access_controls: Set[str]) -> NoReturn:
    """Validate that the provided acl is recognized by CloudFormation."""
    invalid_access_controls = access_controls - ACCESS_CONTROLS
    if invalid_access_controls:
        raise AssertionError(
            f'Invalid Access Controls detected: {invalid_access_controls}')


@unknown_if(FileNotFoundError)
def _has_not_access_control_in_list(
        path: str,
        msg_open: str,
        msg_closed: str,
        vulnerability_reason: str,
        safe_access_controls: Set[str],
        exclude: Optional[List[str]] = None) -> list:
    safe_access_controls = set(safe_access_controls)
    _validate_access_controls(safe_access_controls)
    vulnerable_access_controls = ACCESS_CONTROLS - safe_access_controls

    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::S3::Bucket',
            ],
            exclude=exclude):
        access_control: bool = res_props.get('AccessControl', 'Private')
        if not isinstance(access_control, str):
            continue
        if access_control in vulnerable_access_controls:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'AWS::S3::Bucket/'
                            f'AccessControl/'
                            f'{access_control}'),
                    identifier=res_name,
                    reason=vulnerability_reason))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=msg_open,
        msg_closed=msg_closed)


@api(risk=HIGH, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_private_access_control(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``S3::Bucket`` has an **AccessControl** that is not **Private**.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the **S3 Bucket** has the **AccessControl**
                attribute set to **PublicRead**, **PublicReadWrite**,
                **AuthenticatedRead**, **BucketOwnerRead**,
                **BucketOwnerFullControl**, or **LogDeliveryWrite**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_not_access_control_in_list(
        path=path,
        msg_open='S3 Bucket has not Private Access Control',
        msg_closed='S3 Bucket has Private Access Control',
        vulnerability_reason='is not Private',
        safe_access_controls={
            'Private',
        },
        exclude=exclude,
    )
