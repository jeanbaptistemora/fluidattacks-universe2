"""AWS CloudFormation checks for ``FSx`` (Amazon FSx file systems)."""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unencrypted_volumes(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``FileSystem`` entities are encrypted with a **KmsKeyId**.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **KmsKeyId** attribute is not present.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::FSx::FileSystem',
            ],
            exclude=exclude):
        is_vulnerable: bool = 'KmsKeyId' not in res_props

        if is_vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity='AWS::FSx::FileSystem',
                    identifier=res_name,
                    reason='volume is not encrypted'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='FSx File Systems are not encrypted',
        msg_closed='FSx File Systems are encrypted')
