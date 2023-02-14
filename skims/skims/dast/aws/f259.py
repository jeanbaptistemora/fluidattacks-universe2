from collections.abc import (
    Callable,
    Coroutine,
)
from dast.aws.types import (
    Location,
)
from dast.aws.utils import (
    build_vulnerabilities,
    run_boto3_fun,
)
from model import (
    core_model,
)
from model.core_model import (
    AwsCredentials,
    Vulnerability,
)
from typing import (
    Any,
)
from zone import (
    t,
)


async def dynamodb_has_not_point_in_time_recovery(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="dynamodb", function="list_tables"
    )
    table_names = response.get("TableNames", []) if response else []
    method = core_model.MethodsEnum.AWS_DYNAMODB_HAS_NOT_POINT_IN_TIME_RECOVERY
    vulns: core_model.Vulnerabilities = ()
    if table_names:
        for table in table_names:
            locations: list[Location] = []

            table_backup: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="dynamodb",
                function="describe_continuous_backups",
                parameters={
                    "TableName": table,
                },
            )
            describe_table: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="dynamodb",
                function="describe_table",
                parameters={
                    "TableName": table,
                },
            )
            table_arn = describe_table["Table"]["TableArn"]
            backup_description = table_backup.get(
                "ContinuousBackupsDescription", {}
            )

            if (
                backup_description["PointInTimeRecoveryDescription"][
                    "PointInTimeRecoveryStatus"
                ]
                == "DISABLED"
            ):
                locations = [
                    Location(
                        access_patterns=(
                            (
                                "/ContinuousBackupsDescription/"
                                "PointInTimeRecoveryDescription/"
                                "PointInTimeRecoveryStatus"
                            ),
                        ),
                        arn=(table_arn),
                        values=(
                            backup_description[
                                "PointInTimeRecoveryDescription"
                            ]["PointInTimeRecoveryStatus"],
                        ),
                        description=t(
                            "src.lib_path.f259.has_not_point_in_time_recovery"
                        ),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=table_backup,
                ),
            )
    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (dynamodb_has_not_point_in_time_recovery,)
