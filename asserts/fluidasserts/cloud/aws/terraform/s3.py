"""AWS Terraform checks for ``S3`` (Simple Storage Service)."""

# Standard imports
from typing import List, Optional, Set

# Local imports
from fluidasserts import SAST, HIGH
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.terraform import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


#: A set of available S3 Access Controls
ACCESS_CONTROLS = {
    'private',
    'public-read',
    'public-read-write',
    'authenticated-read',
    'bucket-owner-read',
    'bucket-owner-full-control'
}


@unknown_if(FileNotFoundError)
def _has_not_access_control_in_list(
        path: str,
        msg_open: str,
        msg_closed: str,
        vulnerability_reason: str,
        safe_access_controls: Set[str],
        exclude: Optional[List[str]] = None) -> list:
    safe_access_controls = set(safe_access_controls)
    helper.validate_access_controls(safe_access_controls, ACCESS_CONTROLS)
    vulnerable_access_controls = ACCESS_CONTROLS - safe_access_controls

    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_s3_bucket',
            ],
            exclude=exclude):
        access_control: bool = res_props.get('acl', "private")
        if access_control in vulnerable_access_controls:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'{res_props["type"]}/'
                            f'acl/'
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
    Check if ``aws_s3_bucket`` has an **acl** that is not **private**.

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the **S3 Bucket** has the **acl**
                attribute set to **public-read**, **pulblic-read-write**,
                **authenticated-read**, **bucket-owner-read**,
                **bucket-owner-full-control**, or **log-delivery-write**.
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
            'private',
        },
        exclude=exclude,
    )
