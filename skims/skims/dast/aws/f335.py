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


async def s3_bucket_versioning_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    method = core_model.MethodsEnum.AWS_S3_BUCKET_VERSIONING_DISABLED
    buckets = response.get("Buckets", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if buckets:
        for bucket in buckets:
            locations: list[Location] = []
            bucket_name = bucket["Name"]
            bucket_versioning: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_bucket_versioning",
                parameters={"Bucket": str(bucket_name)},
            )
            status = bucket_versioning.get("Status", "")
            if not status:
                locations = [
                    *locations,
                    Location(
                        arn=(f"arn:aws:s3:::{bucket_name}"),
                        description=t(
                            "lib_path.f335.cfn_s3_bucket_versioning_disabled"
                        ),
                        values=(),
                        access_patterns=(),
                    ),
                ]
            elif status != "Enabled":
                locations = [
                    *locations,
                    Location(
                        arn=(f"arn:aws:s3:::{bucket_name}"),
                        description=t(
                            "lib_path.f335.cfn_s3_bucket_versioning_disabled"
                        ),
                        values=(status,),
                        access_patterns=("/Status",),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=bucket_versioning,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (s3_bucket_versioning_disabled,)
