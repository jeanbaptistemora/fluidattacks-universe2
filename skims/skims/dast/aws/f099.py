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
    Tuple,
)


async def unencrypted_buckets(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="s3",
        function="list_buckets",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    buckets = response.get("Buckets", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    for bucket in buckets:
        encryption: Dict[str, Any] = await run_boto3_fun(
            credentials,
            service="s3",
            function="get_bucket_encryption",
            parameters={
                "Bucket": str(bucket["Name"]),
            },
        )
        if not encryption:
            locations = [
                Location(
                    access_patterns=(),
                    arn=(f"arn:aws:s3:::{bucket['Name']}"),
                    values=(),
                    description=("lib_path.f099.unencrypted_buckets"),
                )
            ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_UNENCRYPTED_BUCKETS),
                aws_response=bucket,
            ),
        )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (unencrypted_buckets,)
