import botocore
from collections.abc import (
    Callable,
    Coroutine,
)
import csv
from dast.aws.types import (
    Location,
)
from dast.aws.utils import (
    build_vulnerabilities,
    run_boto3_fun,
)
from io import (
    StringIO,
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


async def iam_has_mfa_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    await run_boto3_fun(
        credentials, service="iam", function="generate_credential_report"
    )
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )
    vulns: core_model.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))
    for user in credentials_report:
        locations: list[Location] = []
        user_arn = user["arn"]
        user_config = user["password_enabled"]
        user_has_mfa = user["mfa_active"]

        if user_config == "true" and user_has_mfa == "false":
            locations = [
                Location(
                    access_patterns=("/mfa_active",),
                    arn=(f"{user_arn}"),
                    values=(user_has_mfa,),
                    description=("lib_path.f081.iam_has_mfa_disabled"),
                ),
            ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_IAM_HAS_MFA_DISABLED),
                aws_response=user,
            ),
        )

    return vulns


async def root_without_mfa(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_summary"
    )
    vulns: core_model.Vulnerabilities = ()
    summary = response.get("SummaryMap", [])
    if summary["AccountMFAEnabled"] != 1:
        locations = [
            Location(
                access_patterns=("/AccountMFAEnabled",),
                arn=("arn:aws:iam::RootAccount"),
                values=(summary["AccountMFAEnabled"],),
                description=("lib_path.f081.root_without_mfa"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_IAM_ROOT_HAS_MFA_DISABLED),
                aws_response=summary,
            ),
        )

    return vulns


async def mfa_disabled_for_users_with_console_password(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="list_users"
    )
    method = (
        core_model.MethodsEnum.AWS_MFA_DISABLED_FOR_USERS_WITH_CONSOLE_PASSWD
    )
    vulns: core_model.Vulnerabilities = ()
    users = response.get("Users", []) if response else []
    if users:
        for user in users:
            try:
                await run_boto3_fun(
                    credentials,
                    service="iam",
                    function="get_login_profile",
                    parameters={"UserName": str(user["UserName"])},
                )
            except botocore.exceptions.ClientError:
                continue

            locations: list[Location] = []
            user_policies: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_mfa_devices",
                parameters={"UserName": str(user["UserName"])},
            )
            mfa_devices = user_policies.get("MFADevices", [])
            if len(mfa_devices) < 1:
                locations = [
                    Location(
                        access_patterns=("/MFADevices",),
                        arn=(f"{user['Arn']}"),
                        values=(mfa_devices,),
                        description=(
                            "lib_path.f081."
                            "mfa_disabled_for_users_with_console_password"
                        ),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=user_policies,
                ),
            )

    return vulns


async def get_paginated_items(
    credentials: AwsCredentials,
) -> list:
    """Get all items in paginated API calls."""
    pools = []
    args: dict[str, Any] = {
        "credentials": credentials,
        "service": "cognito-idp",
        "function": "list_user_pools",
        "parameters": {"MaxResults": 50},
    }
    data = await run_boto3_fun(**args)
    object_name = "UserPools"
    pools += data.get(object_name, [])

    next_token = data.get("NextToken", None)
    while next_token:
        args["parameters"]["NextToken"] = next_token
        data = await run_boto3_fun(**args)
        pools += data.get(object_name, [])
        next_token = data.get("NextToken", None)

    return pools


async def cognito_mfa_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    vulns: core_model.Vulnerabilities = ()
    pools = await get_paginated_items(credentials)
    method = core_model.MethodsEnum.AWS_COGNITO_HAS_MFA_DISABLED
    for pool in pools:
        response: dict[str, Any] = await run_boto3_fun(
            credentials,
            service="cognito-idp",
            function="get_user_pool_mfa_config",
            parameters={"UserPoolId": str(pool["Id"])},
        )
        mfa = response.get("MfaConfiguration", "")
        locations: list[Location] = []
        if mfa != "ON":
            locations = [
                Location(
                    access_patterns=("/MfaConfiguration",),
                    arn=(pool["Id"]),
                    values=(mfa,),
                    description=("lib_path.f081.cognito_mfa_disabled"),
                ),
            ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=response,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    cognito_mfa_disabled,
    iam_has_mfa_disabled,
    root_without_mfa,
    mfa_disabled_for_users_with_console_password,
)
