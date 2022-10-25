# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import ast
from contextlib import (
    suppress,
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
    Callable,
    Coroutine,
    Dict,
    List,
    Tuple,
)
from zone import (
    t,
)


def service_is_present_action(action: str, service: str) -> bool:
    """Check if a service is present in an action."""
    success = False
    with suppress(KeyError):
        if isinstance(action, List):
            success = service in [act.split(":")[0] for act in action]
        elif action == "*":
            success = True
        else:
            success = action.split(":")[0] == service
    return success


async def iam_has_privileges_over_iam(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
    method = core_model.MethodsEnum.AWS_IAM_HAS_PROVILEGES_OVER_IAM
    vulns: core_model.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: List[Location] = []
            policy_version: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": policy["Arn"],
                    "VersionId": policy["DefaultVersionId"],
                },
            )
            policy_names = policy_version.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, List):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    if item["Effect"] == "Allow" and service_is_present_action(
                        item["Action"], "iam"
                    ):
                        locations = [
                            *locations,
                            Location(
                                access_patterns=(
                                    f"/Document/Statement/{index}/Effect",
                                    f"/Document/Statement/{index}/Action",
                                ),
                                arn=(f"{policy['Arn']}"),
                                values=(
                                    policy_statements[index]["Effect"],
                                    policy_statements[index]["Action"],
                                ),
                                description=t(
                                    "src.lib_path.f325."
                                    "iam_has_privileges_over_iam"
                                ),
                            ),
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=policy_names,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (iam_has_privileges_over_iam,)
