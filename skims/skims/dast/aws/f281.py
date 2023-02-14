import ast
from collections.abc import (
    Callable,
    Coroutine,
    Iterable,
)
from contextlib import (
    suppress,
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


def iterate_s3_has_insecure_transport(
    bucket_name: str, bucket_statements: Iterable
) -> list[Location]:
    locations: list[Location] = []
    for index, stm in enumerate(bucket_statements):
        with suppress(KeyError):
            if (
                stm["Condition"]["Bool"]["aws:SecureTransport"] != "false"
                and stm["Effect"] == "Deny"
            ):
                locations = [
                    *locations,
                    Location(
                        access_patterns=(
                            (
                                f"/{index}/Condition/Bool"
                                "/aws:SecureTransport"
                            ),
                        ),
                        arn=(f"arn:aws:s3:::{bucket_name}"),
                        values=(
                            stm["Condition"]["Bool"]["aws:SecureTransport"],
                            stm["Effect"],
                        ),
                        description=t(
                            "src.lib_path.f281."
                            "bucket_policy_has_secure_transport"
                        ),
                    ),
                ]
            elif (
                stm["Condition"]["Bool"]["aws:SecureTransport"] != "true"
                and stm["Effect"] == "Allow"
            ):
                locations = [
                    *locations,
                    Location(
                        access_patterns=(
                            (
                                f"/{index}/Condition/Bool"
                                "/aws:SecureTransport"
                            ),
                        ),
                        arn=(f"arn:aws:s3:::{bucket_name}"),
                        values=(
                            stm["Condition"]["Bool"]["aws:SecureTransport"],
                        ),
                        description=t(
                            "src.lib_path.f281."
                            "bucket_policy_has_secure_transport"
                        ),
                    ),
                ]

    return locations


async def s3_has_insecure_transport(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets = response.get("Buckets", []) if response else []
    method = core_model.MethodsEnum.AWS_S3_HAS_INSECURE_TRANSPORT
    vulns: core_model.Vulnerabilities = ()
    if buckets:
        for bucket in buckets:
            bucket_name = bucket["Name"]
            bucket_policy_string: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_bucket_policy",
                parameters={
                    "Bucket": bucket_name,
                },
            )
            policy = ast.literal_eval(
                str(bucket_policy_string.get("Policy", {}))
            )
            bucket_statements = ast.literal_eval(
                str(policy.get("Statement", []))
            )
            if not isinstance(bucket_statements, list):
                bucket_statements = [bucket_statements]

            locations = iterate_s3_has_insecure_transport(
                bucket_name, bucket_statements
            )

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=bucket_statements,
                ),
            )
    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (s3_has_insecure_transport,)
