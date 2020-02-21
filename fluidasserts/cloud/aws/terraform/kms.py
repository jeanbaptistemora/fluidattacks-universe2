"""
AWS Terraform checks for ``KMS`` (Key Management Service).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, MEDIUM, LOW
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.terraform import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_key_rotation_absent_or_disabled(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``aws_kms_key`` is miss configured.

    The following checks are performed:

    * F19 enable_key_rotation should not be false or absent
    on aws_kms_key resource

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_kms_key',
            ],
            exclude=exclude):

        key_rotation: bool = res_props.get('enable_key_rotation', False)

        key_rotation = helper.to_boolean(key_rotation)

        if not key_rotation:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=f'aws_kms_key',
                    identifier=res_name,
                    reason='has key rotation absent or disabled'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='enable_key_rotation is absent or disabled on KMS Key',
        msg_closed='enable_key_rotation is enabled on KMS Key')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def is_deletion_window_misconfigured(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``aws_kms_key`` has a wrong deletion_window_in_days.

    Value of ``deletion_window_in_days`` must be == 30

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_kms_key',
            ],
            exclude=exclude):

        key_rotation: int = int(res_props.get('deletion_window_in_days', 30))

        if key_rotation != 30:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=f'aws_kms_key',
                    identifier=res_name,
                    reason='has deletion window != 30'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='value of deletion_window_in_days is not 30',
        msg_closed='value of deletion_window_in_days is 30')
