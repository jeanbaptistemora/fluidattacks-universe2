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


async def users_with_multiple_access_keys(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.AWS_USER_WITH_MULTIPLE_ACCESS_KEYS
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_users",
    )
    vulns: core_model.Vulnerabilities = ()

    users = response.get("Users", [])

    if users:
        for user in users:
            access_keys: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_access_keys",
                parameters={
                    "UserName": user["UserName"],
                },
            )
            access_key_metadata = access_keys["AccessKeyMetadata"]
            locations: List[Location] = []
            access_keys_activated = list(
                filter(
                    lambda y: y == "Active",
                    list(map(lambda x: x["Status"], access_key_metadata)),
                )
            )
            if len(access_keys_activated) > 1:
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(f"arn:aws:iam:::{user['UserName']}"),
                        values=(),
                        description=(
                            "src.lib_path.f165.users_with_multiple_access_keys"
                        ),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=access_key_metadata,
                ),
            )

    return vulns


async def root_has_access_keys(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    await run_boto3_fun(
        credentials, service="iam", function="generate_credential_report"
    )
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )
    locations: List[Location] = []
    vulns: core_model.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))
    root_user = credentials_report[0]
    root_arn = root_user["arn"]

    key_names = ("access_key_1_active", "access_key_2_active")
    with suppress(KeyError):
        for index, name in enumerate(key_names):
            if root_user[name] == "true":
                locations = [
                    *locations,
                    Location(
                        access_patterns=(f"/{key_names[index]}",),
                        arn=(f"{root_arn}"),
                        values=(root_user[key_names[index]],),
                        description=("src.lib_path.f165.root_has_access_keys"),
                    ),
                ]
    vulns = (
        *vulns,
        *build_vulnerabilities(
            locations=locations,
            method=(core_model.MethodsEnum.AWS_IAM_ROOT_HAS_ACCESS_KEYS),
            aws_response=root_user,
        ),
    )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    users_with_multiple_access_keys,
    root_has_access_keys,
)
