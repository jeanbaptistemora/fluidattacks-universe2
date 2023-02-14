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


async def vpcs_without_flowlog(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_vpcs",
        parameters={"Filters": [{"Name": "state", "Values": ["available"]}]},
    )
    vpcs = response.get("Vpcs", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    if vpcs:
        for vpc in vpcs:
            locations: list[Location] = []
            cloud_id = vpc["VpcId"]
            net_interfaces: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="ec2",
                function="describe_flow_logs",
                parameters={
                    "Filters": [{"Name": "resource-id", "Values": [cloud_id]}]
                },
            )
            if not net_interfaces.get("FlowLogs"):
                locations = [
                    Location(
                        access_patterns=(),
                        arn=(f"arn:aws:vpc:::{cloud_id}"),
                        values=(),
                        description=("src.lib_path.f200.vpcs_without_flowlog"),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core_model.MethodsEnum.AWS_VPC_WITHOUT_FLOWLOG),
                    aws_response=vpc,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (vpcs_without_flowlog,)
