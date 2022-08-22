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


async def admin_policy_attached(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="list_policies"
    )
    policies: List[Dict[str, Any]] = response.get("Policies", [])
    elevated_policies = {
        "arn:aws:iam::aws:policy/PowerUserAccess",
        "arn:aws:iam::aws:policy/IAMFullAccess",
        "arn:aws:iam::aws:policy/AdministratorAccess",
    }
    vulns: core_model.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: List[Location] = []
            if (
                policy["Arn"] in elevated_policies
                and policy["AttachmentCount"] != 0
            ):
                locations = [
                    *[
                        Location(
                            access_patterns=("/Arn", "/AttachmentCount"),
                            arn=(
                                f"{policy['Arn']}: "
                                f"AttachmentCount/{policy['AttachmentCount']}"
                            ),
                            values=(
                                policy["Arn"],
                                policy["AttachmentCount"],
                            ),
                            description=t(
                                "src.lib_path.f031_aws.permissive_policy"
                            ),
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_ADMIN_POLICY_ATTACHED),
                    aws_response=policy,
                ),
            )

    return vulns


async def public_buckets(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets: List[Dict[str, Any]] = response.get("Buckets", [])

    perms = ["READ", "WRITE", "FULL_CONTROL", "READ_ACP", "WRITE_ACP"]
    public_acl = "http://acs.amazonaws.com/groups/global/AllUsers"
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
            grants: List[Dict[str, Any]] = bucket_grants.get("Grants", [])
            for index, grant in enumerate(grants):
                locations = [
                    *[
                        Location(
                            access_patterns=(f"/Grants/{index}/Permission",),
                            arn=(f"arn:aws:s3:::{bucket_name}"),
                            values=(grant["Permission"],),
                            description=t(
                                "src.lib_path.f031."
                                "bucket_policy_allows_public_access"
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
                    method=(core_model.MethodsEnum.AWS_PUBLIC_BUCKETS),
                    aws_response=bucket_grants,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    admin_policy_attached,
    public_buckets,
)
