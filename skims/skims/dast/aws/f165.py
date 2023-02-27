from collections.abc import (
    Callable,
    Coroutine,
)
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
)


async def users_with_multiple_access_keys(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.AWS_USER_WITH_MULTIPLE_ACCESS_KEYS
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_users",
    )
    vulns: core_model.Vulnerabilities = ()

    users = response.get("Users", [])

    if users:
        for user in users:
            access_keys: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_access_keys",
                parameters={
                    "UserName": user["UserName"],
                },
            )
            access_key_metadata = access_keys["AccessKeyMetadata"]
            locations: list[Location] = []
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
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )
    locations: list[Location] = []
    vulns: core_model.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))
    root_user = credentials_report[0]
    root_arn = root_user["arn"]

    key_names = ("access_key_1_active", "access_key_2_active")
    with suppress(KeyError):
        for index, name in enumerate(key_names):
            if root_user.get(name) == "true":
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


async def has_not_support_role(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.AWS_IAM_HAS_NOT_SUPPORT_ROLE
    vulns: core_model.Vulnerabilities = ()
    attached_times: int = 0
    policy_arn = "arn:aws:iam::aws:policy/AWSSupportAccess"
    entities: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_entities_for_policy",
        parameters={
            "PolicyArn": policy_arn,
        },
    )

    locations: list[Location] = []
    attached_times = (
        len(list(filter(None, entities["PolicyUsers"])))
        + len(list(filter(None, entities["PolicyGroups"])))
        + len(list(filter(None, entities["PolicyRoles"])))
    )
    if attached_times == 0:
        locations = [
            Location(
                access_patterns=(),
                arn=(f"{policy_arn}"),
                values=(),
                description=("src.lib_path.f165.has_not_support_role"),
            ),
        ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(method),
                aws_response=entities,
            ),
        )

    return vulns


async def has_root_active_signing_certificates(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    method = (
        core_model.MethodsEnum.AWS_IAM_HAS_ROOT_ACTIVE_SIGNING_CERTIFICATES
    )
    await run_boto3_fun(
        credentials, service="iam", function="generate_credential_report"
    )
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )
    vulns: core_model.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))
    root_user = credentials_report[0]
    root_arn = root_user["arn"]
    root_has_active_signing_certs: bool = any(
        (
            root_user.get("cert_1_active") == "true",
            root_user.get("cert_2_active") == "true",
        )
    )
    locations: list[Location] = []
    if root_has_active_signing_certs:
        key_names = ("cert_1_active", "cert_2_active")
        for index, name in enumerate(key_names):
            if root_user.get(name) == "true":
                locations = [
                    *locations,
                    Location(
                        access_patterns=(f"/{key_names[index]}",),
                        arn=(f"{root_arn}"),
                        values=(root_user[key_names[index]],),
                        description=(
                            "src.lib_path.f165."
                            "has_root_active_signing_certificates"
                        ),
                    ),
                ]
    vulns = (
        *vulns,
        *build_vulnerabilities(
            locations=locations,
            method=(method),
            aws_response=root_user,
        ),
    )

    return vulns


async def dynamob_encrypted_with_aws_master_keys(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="dynamodb", function="list_tables"
    )
    table_names = response.get("TableNames", []) if response else []
    method = core_model.MethodsEnum.AWS_DYNAMODB_ENCRYPTED_WITH_AWS_MASTER_KEYS
    vulns: core_model.Vulnerabilities = ()
    if table_names:
        for table_name in table_names:
            locations: list[Location] = []

            describe_table: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="dynamodb",
                function="describe_table",
                parameters={
                    "TableName": table_name,
                },
            )
            table_arn = describe_table["Table"]["TableArn"]
            table = describe_table["Table"]
            try:
                table_ssetype = table["SSEDescription"]["SSEType"]
                if table_ssetype == "AES256":
                    locations = [
                        Location(
                            access_patterns=("/SSEDescription/SSEType",),
                            arn=(table_arn),
                            values=(table_ssetype,),
                            description=(
                                "src.lib_path.f165."
                                "dynamob_encrypted_with_aws_master_keys"
                            ),
                        ),
                    ]
                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=(method),
                            aws_response=table,
                        ),
                    )

            except KeyError:
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(table_arn),
                        values=(),
                        description=(
                            "src.lib_path.f165."
                            "dynamob_encrypted_with_aws_master_keys"
                        ),
                    ),
                ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=table,
                    ),
                )
    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    users_with_multiple_access_keys,
    root_has_access_keys,
    has_not_support_role,
    has_root_active_signing_certificates,
    dynamob_encrypted_with_aws_master_keys,
)
