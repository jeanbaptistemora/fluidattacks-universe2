
"""AWS CloudFormation checks for RDS."""

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
def has_unencrypted_storage(path: str, exclude: list = None) -> tuple:
    """
    Check if any `AWS::RDS::DBInstance` uses unencrypted storage.

    :param path: Location of CloudFormation's template file.
    :returns: - ``OPEN`` if any *RDS-DB* Instance uses unencrypted snapshots.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::RDS::DBInstance',
            ],
            exclude=exclude):
        res_storage_encrypted = res_props.get('StorageEncrypted', False)
        try:
            res_storage_encrypted = helper.to_boolean(res_storage_encrypted)
        except CloudFormationInvalidTypeError:
            # In the future we'll be able to dereference custom CF's functions
            #   for now ignore them
            continue

        is_vulnerable: bool = not res_storage_encrypted

        if is_vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    service='RDS',
                    identifier=res_name,
                    reason='uses unencrypted storage'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS instances use unencrypted storage',
        msg_closed='RDS instances use encrypted storage')
