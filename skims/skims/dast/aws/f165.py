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


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (users_with_multiple_access_keys,)
