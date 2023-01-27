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


async def allows_priv_escalation_by_policies_versions(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
    method = (
        core_model.MethodsEnum.AWS_ALLOWS_PRIV_ESCALATION_BY_POLICIES_VERSIONS
    )
    vulns: core_model.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: List[Location] = []
            pol_ver: Dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": str(policy["Arn"]),
                    "VersionId": str(policy["DefaultVersionId"]),
                },
            )
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, List):
                policy_statements = [policy_statements]

            for index, stm in enumerate(policy_statements):
                with suppress(KeyError):
                    vulnerable = (
                        stm["Effect"] == "Allow"
                        and "Resource" in stm
                        and "iam:CreatePolicyVersion" in stm["Action"]
                        and "iam:SetDefaultPolicyVersion" in stm["Action"]
                    )

                    if vulnerable:
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/Document/Statement/{index}/Effect",
                                        (
                                            f"/Document/Statement/{index}"
                                            "/Resource"
                                        ),
                                        f"/Document/Statement/{index}/Action",
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Effect"],
                                        policy_statements[index]["Resource"],
                                        policy_statements[index]["Action"],
                                    ),
                                    description=t(
                                        "src.lib_path."
                                        "f031_aws.permissive_policy"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=policy_names,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (allows_priv_escalation_by_policies_versions,)
