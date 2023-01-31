import botocore
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
    Callable,
    Coroutine,
    Dict,
    List,
    Tuple,
)


async def has_mfa_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    await run_boto3_fun(
        credentials, service="iam", function="generate_credential_report"
    )
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )
    vulns: core_model.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))
    for user in credentials_report:
        locations: List[Location] = []
        user_arn = user["arn"]
        user_has_mfa: bool = user["mfa_active"] == "false"
        user_has_pass: bool = user["password_enabled"] == "true"
        if user_has_pass and not user_has_mfa:
            locations = [
                Location(
                    access_patterns=("/mfa_active",),
                    arn=(f"{user_arn}"),
                    values=(user_has_mfa,),
                    description=("lib_path.f081.has_mfa_disabled"),
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

    response: Dict[str, Any] = await run_boto3_fun(
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

    response: Dict[str, Any] = await run_boto3_fun(
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

            locations: List[Location] = []
            user_policies: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_mfa_devices",
                parameters={"UserName": str(user["UserName"])},
            )
            mfa_devices = user_policies.get("MFADevices", [])
            if not mfa_devices:
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


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    has_mfa_disabled,
    root_without_mfa,
    mfa_disabled_for_users_with_console_password,
)
