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
from zone import (
    t,
)


async def bucket_has_object_lock_disabled(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets = response.get("Buckets", []) if response else []
    method = core_model.MethodsEnum.AWS_S3_BUCKETS_HAS_OBJECT_LOCK_DISABLED
    vulns: core_model.Vulnerabilities = ()
    if buckets:
        for bucket in buckets:
            locations: List[Location] = []
            bucket_name = bucket["Name"]
            bucket_grants: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_object_lock_configuration",
                parameters={"Bucket": str(bucket_name)},
            )
            conf = bucket_grants.get("ObjectLockConfiguration", {})
            if conf.get("ObjectLockEnabled") != "Enabled":
                locations = [
                    *[
                        Location(
                            access_patterns=(
                                "/ObjectLockConfiguration/ObjectLockEnabled",
                            ),
                            arn=(f"arn:aws:s3:::{bucket_name}"),
                            values=(conf.get("ObjectLockEnabled"),),
                            description=t(
                                "src.lib_path.f101."
                                "bucket_has_object_lock_disabled"
                            ),
                        )
                    ],
                ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=method,
                        aws_response=bucket_grants,
                    ),
                )
            if not conf:
                locations = [
                    *[
                        Location(
                            access_patterns=(),
                            arn=(f"arn:aws:s3:::{bucket_name}"),
                            values=(),
                            description=t(
                                "src.lib_path.f101."
                                "bucket_has_object_lock_disabled"
                            ),
                        )
                    ],
                ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=method,
                        aws_response=bucket,
                    ),
                )
    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (bucket_has_object_lock_disabled,)
