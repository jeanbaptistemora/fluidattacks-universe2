"""
AWS CloudFormation checks for ``RDS`` (Relational Database Service).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/master/LICENSE.md>`_
"""

# Standard imports
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
def has_unencrypted_storage(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``DBCluster`` or ``DBInstance`` use unencrypted storage.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **StorageEncrypted** attribute is set to **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::RDS::DBCluster',
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
                    entity='AWS::RDS::(DBCluster,DBInstance)',
                    identifier=res_name,
                    reason='uses unencrypted storage'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS clusters or instances have unencrypted storage',
        msg_closed='RDS clusters or instances have encrypted storage')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_automated_back_ups(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``DBCluster`` or ``DBInstance`` have not automated backups.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **BackupRetentionPeriod** attribute is set to 0.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::RDS::DBCluster',
                'AWS::RDS::DBInstance',
            ],
            exclude=exclude):
        back_up_retention_period = res_props.get('BackupRetentionPeriod', 1)
        if not helper.is_scalar(back_up_retention_period):
            # In the future we'll be able to dereference custom CF's functions
            #   for now ignore them
            continue

        is_vulnerable: bool = back_up_retention_period in (0, '0')

        if is_vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity='AWS::RDS::(DBCluster,DBInstance)',
                    identifier=res_name,
                    reason='has not automated backups enabled'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS cluster or instances have not automated backups enabled',
        msg_closed='RDS cluster or instances have automated backups enabled')
