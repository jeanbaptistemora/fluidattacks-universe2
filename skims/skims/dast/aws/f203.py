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


async def acl_public_buckets(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets = response.get("Buckets", []) if response else []

    vulns: core_model.Vulnerabilities = ()
    if buckets:
        for bucket in buckets:
            locations: List[Location] = []
            bucket_name = bucket["Name"]

            bucket_grants: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_bucket_acl",
                parameters={"Bucket": str(bucket_name)},
            )

            grants = bucket_grants.get("Grants", [])
            for index, grant in enumerate(grants):
                if grant["Permission"] == "FULL_CONTROL":
                    locations = [
                        *locations,
                        *[
                            Location(
                                access_patterns=(
                                    f"/Grants/{index}/Permission",
                                ),
                                arn=(f"arn:aws:s3:::{bucket_name}"),
                                values=(grant["Permission"],),
                                description=t(
                                    "src.lib_path.f203.public_buckets"
                                ),
                            )
                        ],
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_ACL_PUBLIC_BUCKETS),
                    aws_response=bucket_grants,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (acl_public_buckets,)
