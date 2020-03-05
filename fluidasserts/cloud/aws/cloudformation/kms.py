"""
AWS CloudFormation checks for ``KMS`` (Key Management Service).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

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
def is_key_rotation_absent_or_disabled(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``KMS::Key`` is miss configured.

    The following checks are performed:

    * F19 EnableKeyRotation should not be false or absent on KMS::Key resource

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::KMS::Key',
            ],
            exclude=exclude):

        key_rotation: bool = res_props.get('EnableKeyRotation', False)

        with contextlib.suppress(CloudFormationInvalidTypeError):
            key_rotation = helper.to_boolean(key_rotation)

        if not key_rotation:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=f'AWS::KMS::Key',
                    identifier=res_name,
                    line=res_props['line'],
                    reason='has key rotation absent or disabled'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='EnableKeyRotation is absent or disabled on KMS Key',
        msg_closed='EnableKeyRotation is enabled on KMS Key')
