from contextlib import (
    suppress,
)
import csv
from dast.aws.types import (
    Location,
)
from dast.aws.utils import (
    build_vulnerabilities,
    run_boto3_fun,
)
from datetime import (
    datetime,
    timedelta,
)
from dateutil import (
    parser,
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
import pytz
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
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


async def not_requires_numbers(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:

    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core_model.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", [])
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
    password_policy = response.get("PasswordPolicy", [])
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


async def have_old_creds_enabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    await run_boto3_fun(
        credentials, service="iam", function="generate_credential_report"
    )
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )

    three_months_ago = datetime.now() - timedelta(days=90)
    three_months_ago = three_months_ago.replace(tzinfo=pytz.UTC)
    vulns: core_model.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))
    for user in credentials_report:
        if user["password_enabled"] != "true":
            continue

        get_user: Dict[str, Any] = await run_boto3_fun(
            credentials,
            service="iam",
            function="get_user",
            parameters={"UserName": user["user"]},
        )
        with suppress(KeyError):
            user_pass_last_used = get_user["User"]["PasswordLastUsed"]
            user_arn = user["arn"]
            vulnerable = user_pass_last_used < three_months_ago
            if vulnerable:
                locations = [
                    Location(
                        access_patterns=("/User/PasswordLastUsed",),
                        arn=(f"{user_arn}"),
                        values=(user_pass_last_used,),
                        description=(
                            "src.lib_path.f363.have_old_creds_enabled"
                        ),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_IAM_HAS_OLD_CREDS_ENABLED
                    ),
                    aws_response=get_user,
                ),
            )

    return vulns


async def have_old_access_keys(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    await run_boto3_fun(
        credentials, service="iam", function="generate_credential_report"
    )
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )

    three_months_ago = datetime.now() - timedelta(days=90)
    three_months_ago = three_months_ago.replace(tzinfo=pytz.UTC)
    vulns: core_model.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))

    for user in credentials_report:
        locations: List[Location] = []
        if any(
            (
                user["access_key_1_active"] != "true",
                user["access_key_2_active"] != "true",
            )
        ):
            continue

        key_names = ("access_key_1_last_rotated", "access_key_2_last_rotated")
        with suppress(KeyError):
            for index, name in enumerate(key_names):
                if (
                    parser.parse(user[name]).replace(tzinfo=pytz.UTC)
                    < three_months_ago
                ):
                    user_arn = user["arn"]
                    locations = [
                        *locations,
                        Location(
                            access_patterns=(f"/{key_names[index]}",),
                            arn=(f"{user_arn}"),
                            values=(user[key_names[index]],),
                            description=(
                                "src.lib_path.f363.have_old_access_keys"
                            ),
                        ),
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_IAM_HAS_OLD_ACCESS_KEYS
                    ),
                    aws_response=user,
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
    password_policy = response.get("PasswordPolicy", [])
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
    have_old_creds_enabled,
    have_old_access_keys,
)
