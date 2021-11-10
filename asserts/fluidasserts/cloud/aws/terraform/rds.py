"""
AWS Terraform checks for ``RDS`` (Relational Database Service).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""


from fluidasserts import (
    LOW,
    MEDIUM,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    Vulnerability,
)
from fluidasserts.helper import (
    aws as helper,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from typing import (
    List,
    Optional,
)


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unencrypted_storage(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if any RDS resource use unencrypted storage.

    The following checks are performed:

    * F26 RDS DBCluster should have StorageEncrypted enabled
    * F27 RDS DBInstance should have StorageEncrypted enabled

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **StorageEncrypted** attribute is set to **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
        starting_path=path,
        resource_types=[
            "aws_db_instance",
            "aws_rds_cluster",
        ],
        exclude=exclude,
    ):
        res_type = res_props["type"]
        res_storage_encrypted = res_props.get("storage_encrypted", False)

        res_storage_encrypted = helper.to_boolean(res_storage_encrypted)

        if not res_storage_encrypted:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=res_type,
                    identifier=res_name,
                    reason="uses unencrypted storage",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="RDS clusters or instances have unencrypted storage",
        msg_closed="RDS clusters or instances have encrypted storage",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_automated_backups(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if any RDS does not have automated backups enabled.

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **backup_retention_period** attribute is set to 0.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
        starting_path=path,
        resource_types=[
            "aws_db_instance",
            "aws_rds_cluster",
        ],
        exclude=exclude,
    ):
        back_up_retention_period = res_props.get("backup_retention_period", 1)

        if not helper.is_scalar(back_up_retention_period):
            continue

        is_vulnerable: bool = back_up_retention_period in (0, "0")

        if is_vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=res_props["type"],
                    identifier=res_name,
                    reason="has not automated backups enabled",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="RDS cluster or instances have not automated backups enabled",
        msg_closed="RDS cluster or instances have automated backups enabled",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_publicly_accessible(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if any ``aws_db_instance`` is Internet facing (a.k.a. public).

    The following checks are performed:

    * F22 RDS instance should not be publicly accessible

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **publicly_accessible** attribute is set to
                **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
        starting_path=path,
        resource_types=[
            "aws_db_instance",
        ],
        exclude=exclude,
    ):
        is_public: bool = res_props.get("publicly_accessible", False)

        if helper.to_boolean(is_public):
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=res_props["type"],
                    identifier=res_name,
                    reason="is publicly accessible",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="RDS instances are publicly accessible",
        msg_closed="RDS instances are not publicly accessible",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_not_inside_a_db_subnet_group(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if ``DBInstance`` or ``DBCluster`` are not inside a DB Subnet Group.

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **db_subnet_group_name** attribute is not set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
        starting_path=path,
        resource_types=[
            "aws_db_instance",
            "aws_rds_cluster",
        ],
        exclude=exclude,
    ):
        res_type = res_props["type"]
        db_subnet_group_name: bool = res_props.get("db_subnet_group_name", "")

        if not db_subnet_group_name:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(
                        f"{res_type}"
                        f"/db_subnet_group_name"
                        f"/{db_subnet_group_name}"
                    ),
                    identifier=res_name,
                    reason="is not inside a DB Subnet Group",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="RDS Cluster or Instances are not inside a DB Subnet Group",
        msg_closed="RDS Cluster or Instances are inside a DB Subnet Group",
    )
