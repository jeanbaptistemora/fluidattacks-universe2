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


async def admin_policy_attached(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="list_policies"
    )
    policies: List[Dict[str, Any]] = response.get("Policies", [])
    elevated_policies = {
        "arn:aws:iam::aws:policy/PowerUserAccess",
        "arn:aws:iam::aws:policy/IAMFullAccess",
        "arn:aws:iam::aws:policy/AdministratorAccess",
    }
    vulns: core_model.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: List[Location] = []
            if (
                policy["Arn"] in elevated_policies
                and policy["AttachmentCount"] != 0
            ):
                locations = [
                    *[
                        Location(
                            access_patterns=("/Arn", "/AttachmentCount"),
                            arn=(
                                f"{policy['Arn']}: "
                                f"AttachmentCount/{policy['AttachmentCount']}"
                            ),
                            values=(
                                policy["Arn"],
                                policy["AttachmentCount"],
                            ),
                            description=t(
                                "src.lib_path.f031_aws.permissive_policy"
                            ),
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_ADMIN_POLICY_ATTACHED),
                    aws_response=policy,
                ),
            )

    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (admin_policy_attached,)
