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


# Pending for finding creation
async def has_unencrypted_logs(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudtrail", function="describe_trails"
    )
    method = core_model.MethodsEnum.AWS_EBS_USES_DEFAULT_KMS_KEY
    trails = response.get("trailList", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    locations: List[Location] = []
    if trails:
        for trail in trails:
            trail_arn = trail["TrailARN"]
            if not trail.get("KmsKeyId"):
                locations = [
                    *locations,
                    Location(
                        arn=(trail_arn),
                        description=t(
                            "lib_path.f411.ebs_uses_default_kms_key"
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
                    aws_response=trail,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (has_unencrypted_logs,)
