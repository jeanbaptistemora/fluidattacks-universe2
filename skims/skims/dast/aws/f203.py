import ast
from collections.abc import (
    Callable,
    Coroutine,
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


async def acl_public_buckets(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets = response.get("Buckets", []) if response else []

    vulns: core_model.Vulnerabilities = ()
    if buckets:
        for bucket in buckets:
            locations: list[Location] = []
            bucket_name = bucket["Name"]

            bucket_grants: dict[str, Any] = await run_boto3_fun(
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


def iterate_s3_buckets_allow_unauthorized_public_access(
    policies_statements: list, bucket_name: str
) -> core_model.Vulnerabilities:
    locations: list[Location] = []
    vulns: core_model.Vulnerabilities = ()
    method = (
        core_model.MethodsEnum.AWS_S3_BUCKETS_ALLOW_UNAUTHORIZED_PUBLIC_ACCESS
    )
    for policy in policies_statements:
        with suppress(KeyError):
            if (
                policy["Effect"] == "Allow"
                and (
                    isinstance(policy["Principal"], dict)
                    and "*" in policy["Principal"].values()
                )
            ) or (policy["Effect"] == "Allow" and policy["Principal"] == "*"):
                locations = [
                    *locations,
                    *[
                        Location(
                            access_patterns=(
                                "/Effect",
                                "/Principal",
                            ),
                            arn=(f"arn:aws:s3:::{bucket_name}"),
                            values=(
                                policy["Effect"],
                                policy["Principal"],
                            ),
                            description=t(
                                "src.lib_path.f203."
                                "buckets_allow_unauthorized_"
                                "public_access"
                            ),
                        )
                    ],
                ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=method,
                aws_response=policy,
            ),
        )

    return vulns


async def s3_buckets_allow_unauthorized_public_access(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets = response.get("Buckets", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if buckets:
        for bucket in buckets:
            bucket_name = bucket["Name"]

            bucket_policy: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_bucket_policy",
                parameters={"Bucket": str(bucket_name)},
            )

            if bucket_policy:
                bucket_policies = ast.literal_eval(
                    str(bucket_policy.get("Policy", []))
                )

                vulns = (
                    *vulns,
                    *iterate_s3_buckets_allow_unauthorized_public_access(
                        bucket_policies["Statement"], bucket_name
                    ),
                )

    return vulns


async def is_trail_bucket_public(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudtrail", function="describe_trails"
    )
    method = core_model.MethodsEnum.AWS_IAM_IS_TRAIL_BUCKET_PUBLIC
    trail_list = response.get("traillist", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    public_acl = "http://acs.amazonaws.com/groups/global/AllUsers"
    perms = ["READ", "WRITE", "FULL_CONTROL", "READ_ACP", "WRITE_ACP"]

    if trail_list:
        for trail in trail_list:
            locations: list[Location] = []
            trail_arn = trail["TrailARN"]
            trail_bucket = trail["S3BucketName"]

            get_bucket_acl: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_bucket_acl",
                parameters={"Bucket": str(trail_bucket)},
            )
            grants = get_bucket_acl.get("Grants", [])

            for index, grant in enumerate(grants):
                locations = [
                    *locations,
                    *[
                        Location(
                            access_patterns=(f"/{index}/Permission",),
                            arn=(trail_arn),
                            values=(grant["Permission"],),
                            description=t(
                                "src.lib_path.f203.is_trail_bucket_public"
                            ),
                        )
                        for (key, val) in grant.items()
                        if key == "Permission"
                        and any(perm in val for perm in perms)
                        for (grantee_k, _) in grant["Grantee"].items()
                        if (
                            "URI" in grantee_k
                            and grant["Grantee"]["URI"] == public_acl
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=grants,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    is_trail_bucket_public,
    acl_public_buckets,
    s3_buckets_allow_unauthorized_public_access,
)
