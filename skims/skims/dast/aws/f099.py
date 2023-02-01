import ast
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
        locations: List[Location] = []
        encryption: Dict[str, Any] = await run_boto3_fun(
            credentials,
            service="s3",
            function="get_bucket_encryption",
            parameters={
                "Bucket": str(bucket["Name"]),
            },
        )
        if not encryption.get("ServerSideEncryptionConfiguration"):
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


async def bucket_policy_has_server_side_encryption_disable(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.AWS_BUCKET_POLICY_ENCRYPTION_DISABLE
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="s3",
        function="list_buckets",
    )
    buckets = response.get("Buckets", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    for bucket in buckets:
        locations: List[Location] = []
        bucket_policy_string: Dict[str, Any] = await run_boto3_fun(
            credentials,
            service="s3",
            function="get_bucket_policy",
            parameters={
                "Bucket": str(bucket["Name"]),
            },
        )
        if bucket_policy_string:
            policy = ast.literal_eval(str(bucket_policy_string["Policy"]))
            bucket_statements = policy["Statement"]

            for index, stm in enumerate(bucket_statements):
                if (
                    (conditions := stm.get("Condition", None))
                    and conditions.get("Null", None)
                    and conditions["Null"].get(
                        "s3:x-amz-server-side-encryption", None
                    )
                    and conditions["Null"]["s3:x-amz-server-side-encryption"]
                    != "true"
                ):
                    condition = stm["Condition"]["Null"][
                        "s3:x-amz-server-side-encryption"
                    ]
                    locations = [
                        *locations,
                        Location(
                            access_patterns=(
                                (
                                    f"/Statement/{index}/Condition/Null"
                                    "/s3:x-amz-server-side-encryption"
                                ),
                            ),
                            arn=(f"arn:aws:s3:::{bucket['Name']}"),
                            values=(f"{condition}",),
                            description=(
                                "src.lib_path.f099."
                                "bckp_has_server_side_encryption_disabled"
                            ),
                        ),
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=policy,
                ),
            )
    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    unencrypted_buckets,
    bucket_policy_has_server_side_encryption_disable,
)
