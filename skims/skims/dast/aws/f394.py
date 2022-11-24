# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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


async def cloudtrail_files_not_validated(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudtrail", function="describe_trails"
    )
    method = core_model.MethodsEnum.AWS_CLOUDTRAIL_FILES_NOT_VALIDATED
    trails = response.get("trailList", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if trails:
        for trail in trails:
            locations: List[Location] = []
            trail_arn = trail["TrailARN"]
            if trail["LogFileValidationEnabled"]:
                locations = [
                    *locations,
                    Location(
                        arn=(trail_arn),
                        description=t(
                            "src.lib_path.f394.cfn_log_files_not_validated"
                        ),
                        values=(trail["LogFileValidationEnabled"],),
                        access_patterns=("/LogFileValidationEnabled",),
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
] = (cloudtrail_files_not_validated,)
