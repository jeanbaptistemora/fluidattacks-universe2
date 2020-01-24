"""
AWS Terraform checks for ``RDS`` (Relational Database Service).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, LOW
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


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

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance or cluster have not the
                **deletion_protection** parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_db_instance',
                'aws_rds_cluster',
            ],
            exclude=exclude):
        res_type = res_props['type']
        deletion_protection = helper.to_boolean(
            res_props.get('deletion_protection', False)
        )
        if not deletion_protection:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'{res_type}/'
                            f'deletion_protection/'
                            f'{deletion_protection}'),
                    identifier=res_name,
                    reason='has not deletion protection'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS instances or clusters have not deletion protection',
        msg_closed='RDS instances or clusters have deletion protection')
