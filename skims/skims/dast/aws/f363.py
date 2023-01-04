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
    password_policy = response.get("PasswordPolicy", [])
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
    password_policy = response.get("PasswordPolicy", [])
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
    password_policy = response.get("PasswordPolicy", [])
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


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    not_requires_uppercase,
    not_requires_lowercase,
    not_requires_symbols,
)
