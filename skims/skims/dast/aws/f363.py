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
    Tuple,
)


async def not_requires_uppercase(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core_model.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    if not password_policy["RequireUppercaseCharacters"]:
        locations = [
            Location(
                access_patterns=("/RequireUppercaseCharacters",),
                arn=(f"{user['User']['Arn']}"),
                values=(password_policy["RequireUppercaseCharacters"],),
                description=("src.lib_path.f363.not_requires_uppercase"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_IAM_NOT_REQUIRES_UPPERCASE),
                aws_response=password_policy,
            ),
        )

    return vulns


async def not_requires_lowercase(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core_model.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    if not password_policy["RequireLowercaseCharacters"]:
        locations = [
            Location(
                access_patterns=("/RequireLowercaseCharacters",),
                arn=(f"{user['User']['Arn']}"),
                values=(password_policy["RequireLowercaseCharacters"],),
                description=("src.lib_path.f363.not_requires_lowercase"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_IAM_NOT_REQUIRES_LOWERCASE),
                aws_response=password_policy,
            ),
        )

    return vulns


async def not_requires_symbols(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core_model.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    if not password_policy["RequireSymbols"]:
        locations = [
            Location(
                access_patterns=("/RequireSymbols",),
                arn=(f"{user['User']['Arn']}"),
                values=(password_policy["RequireSymbols"],),
                description=("src.lib_path.f363.not_requires_symbols"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_IAM_NOT_REQUIRES_SYMBOLS),
                aws_response=password_policy,
            ),
        )

    return vulns


async def not_requires_numbers(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core_model.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    if not password_policy["RequireNumbers"]:
        locations = [
            Location(
                access_patterns=("/RequireNumbers",),
                arn=(f"{user['User']['Arn']}"),
                values=(password_policy["RequireNumbers"],),
                description=("src.lib_path.f363.not_requires_numbers"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_IAM_NOT_REQUIRES_NUMBERS),
                aws_response=password_policy,
            ),
        )

    return vulns


async def min_password_len_unsafe(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    min_length: int = 14
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core_model.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    if password_policy["MinimumPasswordLength"] < min_length:
        locations = [
            Location(
                access_patterns=("/MinimumPasswordLength",),
                arn=(f"{user['User']['Arn']}"),
                values=(password_policy["MinimumPasswordLength"],),
                description=("src.lib_path.f363.min_password_len_unsafe"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_MIN_PASSWORD_LEN_UNSAFE),
                aws_response=password_policy,
            ),
        )

    return vulns


async def password_reuse_unsafe(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core_model.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", [])
    password_reuse: int = password_policy.get("PasswordReusePrevention", 0)
    min_reuse = 24
    if password_reuse < min_reuse:
        locations = [
            Location(
                access_patterns=("/PasswordReusePrevention",),
                arn=(f"{user['User']['Arn']}"),
                values=(password_policy["PasswordReusePrevention"],),
                description=("src.lib_path.f363.password_reuse_unsafe"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_IAM_PASSWORD_REUSE_UNSAFE),
                aws_response=password_policy,
            ),
        )

    return vulns


async def password_expiration_unsafe(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core_model.Vulnerabilities = ()
    method = core_model.MethodsEnum.AWS_IAM_PASSWORD_EXPIRATION_UNSAFE
    password_policy = response.get("PasswordPolicy", {})
    max_days = 90
    pasword_max_age: int = password_policy.get("MaxPasswordAge", max_days + 1)
    if pasword_max_age > max_days:
        locations = [
            Location(
                access_patterns=("/MaxPasswordAge",),
                arn=(f"{user['User']['Arn']}"),
                values=(password_policy["MaxPasswordAge"],),
                description=("src.lib_path.f363.password_expiration_unsafe"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=method,
                aws_response=password_policy,
            ),
        )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    not_requires_uppercase,
    not_requires_lowercase,
    not_requires_symbols,
    not_requires_numbers,
    min_password_len_unsafe,
    password_reuse_unsafe,
    password_expiration_unsafe,
)
