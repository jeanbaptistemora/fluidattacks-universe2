# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    Callable,
    Coroutine,
    Dict,
    List,
    Tuple,
)
from zone import (
    t,
)


async def rds_has_unencrypted_storage(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_instances"
    )
    db_instances = response.get("DBInstances", []) if response else []
    method = core_model.MethodsEnum.AWS_RDS_HAS_UNENCRYPTED_STORAGE
    vulns: core_model.Vulnerabilities = ()
    if db_instances:
        for instance in db_instances:
            locations: List[Location] = []
            if not instance.get("StorageEncrypted", False):
                instance_arn = instance["DBInstanceArn"]
                locations = [
                    Location(
                        access_patterns=("/StorageEncrypted",),
                        arn=(f"{instance_arn}"),
                        values=(instance.get("StorageEncrypted", False),),
                        description=t(
                            "src.lib_path.f246.rds_has_unencrypted_storage"
                        ),
                    )
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=instance,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (rds_has_unencrypted_storage,)
