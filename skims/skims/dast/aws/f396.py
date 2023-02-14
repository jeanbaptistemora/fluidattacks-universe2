from collections.abc import (
    Callable,
    Coroutine,
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
from typing import (
    Any,
)
from zone import (
    t,
)


async def kms_key_is_key_rotation_absent_or_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="kms", function="list_keys"
    )
    method = core_model.MethodsEnum.AWS_KMS_IS_KEY_ROTATION_DISABLED
    keys = response.get("Keys", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if keys:
        for key in keys:
            locations: list[Location] = []
            key_rotation: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="kms",
                function="get_key_rotation_status",
                parameters={"KeyId": str(key["KeyId"])},
            )
            key_rotation_status = key_rotation.get("KeyRotationEnabled", "")

            if str(key_rotation_status) == "False":
                locations = [
                    *locations,
                    Location(
                        arn=(key["KeyArn"]),
                        description=t(
                            "src.lib_path.f396."
                            "kms_key_is_key_rotation_absent_or_disabled"
                        ),
                        values=(key_rotation["KeyRotationEnabled"],),
                        access_patterns=("/KeyRotationEnabled",),
                    ),
                ]
            elif not key_rotation_status:
                locations = [
                    *locations,
                    Location(
                        arn=(key["KeyArn"]),
                        description=t(
                            "src.lib_path.f396."
                            "kms_key_is_key_rotation_absent_or_disabled"
                        ),
                        values=(),
                        access_patterns=(),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=key_rotation,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (kms_key_is_key_rotation_absent_or_disabled,)
