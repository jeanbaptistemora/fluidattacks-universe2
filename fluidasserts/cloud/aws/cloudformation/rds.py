"""
AWS CloudFormation checks for ``RDS`` (Relational Database Service).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/master/LICENSE.md>`_
"""

# Standard imports
import contextlib
from typing import List, Optional

# Local imports
from fluidasserts import SAST, LOW, MEDIUM
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

    The following checks are performed:

    * F26 RDS DBCluster should have StorageEncrypted enabled
    * F27 RDS DBInstance should have StorageEncrypted enabled

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

        with contextlib.suppress(CloudFormationInvalidTypeError):
            res_storage_encrypted = helper.to_boolean(res_storage_encrypted)

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
def has_not_automated_backups(
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


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_publicly_accessible(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``RDS::DBInstance`` is Internet facing (a.k.a. public).

    The following checks are performed:

    * F22 RDS instance should not be publicly accessible

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **PubliclyAccessible** attribute is set to
                **true**.
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
        is_public: bool = res_props.get('PubliclyAccessible', False)

        with contextlib.suppress(CloudFormationInvalidTypeError):
            is_public = helper.to_boolean(is_public)

        if is_public:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=f'AWS::RDS::DBInstance',
                    identifier=res_name,
                    reason='is publicly accessible'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS instances are publicly accessible',
        msg_closed='RDS instances are not publicly accessible')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_not_inside_a_db_subnet_group(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``DBInstance`` or ``DBCluster`` are not inside a DB Subnet Group.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **DBSubnetGroupName** attribute is not set.
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
        res_type = res_props['../Type']
        db_subnet_group_name: bool = res_props.get('DBSubnetGroupName')

        if not db_subnet_group_name:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'{res_type}'
                            f'/DBSubnetGroupName'
                            f'/{db_subnet_group_name}'),
                    identifier=res_name,
                    reason='is not inside a DB Subnet Group'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS Cluster or Instances are not inside a DB Subnet Group',
        msg_closed='RDS Cluster or Instances are inside a DB Subnet Group')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_termination_protection(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``RDS`` clusters and instances have termination protection.

    By default RDS Clusters and Instances can be terminated using the
    Amazon EC2 console, CLI, or API.

    This is not desirable if the termination is done unintentionally
    because DB Snapshots and Automated Backups are deleted
    automatically after some time (or immediately in some cases)
    which make cause data lost and service interruption.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance or cluster have not the
                **DeletionProtection** parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_resources_in_template(
            starting_path=path,
            resource_types=[
                'AWS::RDS::DBInstance',
                'AWS::RDS::DBCluster',
            ],
            exclude=exclude):
        res_type = res_props['../Type']
        deletion_protection: bool = res_props.get('DeletionProtection', False)

        with contextlib.suppress(CloudFormationInvalidTypeError):
            deletion_protection = helper.to_boolean(deletion_protection)

        if not deletion_protection:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'{res_type}/'
                            f'DeletionProtection/'
                            f'{deletion_protection}'),
                    identifier=res_name,
                    reason='has not deletion protection'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS instances or clusters have not deletion protection',
        msg_closed='RDS instances or clusters have deletion protection')
