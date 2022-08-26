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


async def group_with_inline_policies(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="list_groups"
    )
    groups: List[Dict[str, Any]] = response.get("Groups", [])

    vulns: core_model.Vulnerabilities = ()
    if groups:
        for group in groups:
            group_policies: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_group_policies",
                parameters={"GroupName": str(group["GroupName"])},
            )
            policy_names: List[Dict[str, Any]] = group_policies.get(
                "PolicyNames", []
            )

            locations: List[Location] = []
            if policy_names:
                locations = [
                    *[
                        Location(
                            access_patterns=("/PolicyNames",),
                            arn=(f"{group['Arn']}"),
                            values=(policy_names[0],),
                            description=t(
                                "src.lib_path.f031."
                                "iam_group_missing_role_based_security"
                            ),
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_GROUP_WITH_INLINE_POLICY
                    ),
                    aws_response=group_policies,
                ),
            )

    return vulns


async def full_access_policies(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies: List[Dict[str, Any]] = response.get("Policies", [])

    vulns: core_model.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: List[Location] = []
            pol_ver: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": str(policy["Arn"]),
                    "VersionId": str(policy["DefaultVersionId"]),
                },
            )
            policy_names = pol_ver.get("PolicyVersion", [])
            pol_access = list(policy_names["Document"]["Statement"])

            for index, item in enumerate(pol_access):
                if (
                    item["Effect"] == "Allow"
                    and item["Action"] == "*"
                    and item["Resource"] == "*"
                ):
                    locations = [
                        *[
                            Location(
                                access_patterns=(
                                    f"/Document/Statement/{index}/Effect",
                                    f"/Document/Statement/{index}/Action",
                                    f"/Document/Statement/{index}/Resource",
                                ),
                                arn=(f"{policy['Arn']}"),
                                values=(
                                    pol_access[index]["Effect"],
                                    pol_access[index]["Action"],
                                    pol_access[index]["Resource"],
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
                    method=(core_model.MethodsEnum.AWS_FULL_ACCESS_POLICIES),
                    aws_response=policy_names,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    admin_policy_attached,
    full_access_policies,
    public_buckets,
    group_with_inline_policies,
)
