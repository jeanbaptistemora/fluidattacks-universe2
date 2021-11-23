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
