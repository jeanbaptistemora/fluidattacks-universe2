import ast
import boto3
import botocore
from botocore import (
    UNSIGNED,
)
from botocore.client import (
    Config,
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
import re
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Tuple,
)
from utils.logs import (
    log_exception_blocking,
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
    policies = response.get("Policies", []) if response else []
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


async def bucket_objects_can_be_listed(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets = response.get("Buckets", []) if response else []
    s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    vulns: core_model.Vulnerabilities = ()
    for bucket in buckets:
        try:
            nice = s3_client.list_objects_v2(Bucket=bucket["Name"], MaxKeys=10)
            if nice:
                locations = [
                    *[
                        Location(
                            access_patterns=("/Name",),
                            arn=(f"arn:aws:s3:::{bucket['Name']}"),
                            values=(bucket["Name"],),
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
                        method=(core_model.MethodsEnum.AWS_PUBLIC_BUCKETS),
                        aws_response=bucket,
                    ),
                )
        except botocore.exceptions.ClientError:
            log_exception_blocking(
                "exception", botocore.exceptions.ClientError
            )
    return vulns


async def public_buckets(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets = response.get("Buckets", []) if response else []

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
            grants = bucket_grants.get("Grants", [])
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
    groups = response.get("Groups", []) if response else []

    vulns: core_model.Vulnerabilities = ()
    if groups:
        for group in groups:
            group_policies: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_group_policies",
                parameters={"GroupName": str(group["GroupName"])},
            )
            policy_names = group_policies.get("PolicyNames", [])

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


async def user_with_inline_policies(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="list_users"
    )
    users = response.get("Users", []) if response else []

    vulns: core_model.Vulnerabilities = ()
    if users:
        for user in users:
            user_policies: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_user_policies",
                parameters={"UserName": str(user["UserName"])},
            )

            policy_names = user_policies.get("PolicyNames", [])

            locations: List[Location] = []
            if policy_names:
                locations = [
                    *[
                        Location(
                            access_patterns=("/PolicyNames",),
                            arn=(f"{user['Arn']}"),
                            values=(policy_names[0],),
                            description=t(
                                "src.lib_path.f031."
                                "iam_user_missing_role_based_security"
                            ),
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_USER_WITH_INLINE_POLICY
                    ),
                    aws_response=user_policies,
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
    policies = response.get("Policies", []) if response else []

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
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, List):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
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
                                        (
                                            f"/Document/Statement/{index}"
                                            "/Resource"
                                        ),
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Effect"],
                                        policy_statements[index]["Action"],
                                        policy_statements[index]["Resource"],
                                    ),
                                    description=t(
                                        "src.lib_path."
                                        "f031_aws.permissive_policy"
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


def _match_pattern(pattern: str, target: str, flags: int = 0) -> bool:
    # Escape everything that is not `*` and replace `*` with regex `.*`
    pattern = r".*".join(map(re.escape, pattern.split("*")))
    return bool(re.match(f"^{pattern}$", target, flags=flags))


def _match_iam_passrole(action: str) -> bool:
    return _match_pattern(str(action), "iam:PassRole")


async def open_passrole(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []

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
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, list):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    if isinstance(item["Action"], str):
                        action = [item["Action"]]
                    else:
                        action = item["Action"]

                    if (
                        item["Effect"] == "Allow"
                        and any(map(_match_iam_passrole, action))
                        and item["Resource"] == "*"
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/Document/Statement/{index}/Effect",
                                        f"/Document/Statement/{index}/Action",
                                        (
                                            f"/Document/Statement/{index}"
                                            "/Resource"
                                        ),
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Effect"],
                                        policy_statements[index]["Action"],
                                        policy_statements[index]["Resource"],
                                    ),
                                    description=t(
                                        "src.lib_path.f031_aws.open_passrole"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_OPEN_PASSROLE),
                    aws_response=policy_names,
                ),
            )

    return vulns


def _is_action_permissive(action: Any) -> bool:
    if not isinstance(action, str):
        # A var or syntax error
        return False

    splitted = action.split(":", 1)  # a:b
    provider = splitted[0]  # a
    effect = splitted[1] if splitted[1:] else None  # b

    return (
        (provider == "*")
        or (effect and effect.startswith("*"))
        or ("*" in provider and effect is None)
    )


async def permissive_policy(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
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
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, List):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    if isinstance(item["Action"], str):
                        action = [item["Action"]]
                    else:
                        action = item["Action"]

                    if (
                        item["Effect"] == "Allow"
                        and any(map(_is_action_permissive, action))
                        and item["Resource"] == "*"
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/Document/Statement/{index}/Action",
                                        (
                                            f"/Document/Statement/{index}"
                                            "/Resource"
                                        ),
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Action"],
                                        policy_statements[index]["Resource"],
                                    ),
                                    description=t(
                                        "src.lib_path."
                                        "f031_aws.permissive_policy"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_PERMISSIVE_POLICY),
                    aws_response=policy_names,
                ),
            )

    return vulns


async def full_access_to_ssm(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
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
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, List):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    if isinstance(item["Action"], str):
                        action = [item["Action"]]
                    else:
                        action = item["Action"]

                    if item["Effect"] == "Allow" and any(
                        map(lambda act: act == "ssm:*", action)
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/Document/Statement/{index}/Action",
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Action"],
                                    ),
                                    description=t(
                                        "src.lib_path."
                                        "f031.iam_has_full_access_to_ssm"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_FULL_ACCESS_SSM),
                    aws_response=policy_names,
                ),
            )

    return vulns


async def negative_statement(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
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
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, List):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    if isinstance(item["NotAction"], str):
                        action = [item["NotAction"]]
                    else:
                        action = item["NotAction"]

                    if item["Effect"] == "Allow" and not _is_action_permissive(
                        action
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        (
                                            "/Document/Statement"
                                            f"/{index}/NotAction"
                                        ),
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=policy_statements[index][
                                        "NotAction"
                                    ],
                                    description=t(
                                        "src.lib_path."
                                        "f031.iam_has_full_access_to_ssm"
                                    ),
                                )
                            ],
                        ]

                    if (
                        item["Effect"] == "Allow"
                        and item["NotResource"] != "*"
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        (
                                            "/Document/Statement"
                                            f"/{index}/NotResource"
                                        ),
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=policy_statements[index][
                                        "NotResource"
                                    ],
                                    description=t(
                                        "src.lib_path."
                                        "f031_aws.negative_statement"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_NEGATIVE_STATEMENT),
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
    open_passrole,
    public_buckets,
    permissive_policy,
    negative_statement,
    full_access_to_ssm,
    group_with_inline_policies,
    user_with_inline_policies,
)
