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
    users_csv = StringIO(response["Content"].decode())
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


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (has_mfa_disabled,)
