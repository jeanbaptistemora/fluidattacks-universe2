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


async def ec2_has_terminate_shutdown_behavior(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_instances",
    )
    reservations = response.get("Reservations", []) if response else []
    method = core_model.MethodsEnum.AWS_EC2_HAS_TERMINATE_SHUTDOWN_BEHAVIOR
    vulns: core_model.Vulnerabilities = ()
    if reservations:
        for instances in reservations:
            locations: List[Location] = []
            for instance in instances["Instances"]:
                shutdown_behavior: Dict[str, Any] = await run_boto3_fun(
                    credentials,
                    service="ec2",
                    function="describe_instance_attribute",
                    parameters={
                        "Attribute": "instanceInitiatedShutdownBehavior",
                        "InstanceId": instance["InstanceId"],
                    },
                )
                value = shutdown_behavior["InstanceInitiatedShutdownBehavior"][
                    "Value"
                ]
                if value == "terminate":
                    locations = [
                        *locations,
                        Location(
                            access_patterns=(
                                (
                                    "/InstanceInitiatedShutdownBehavior/"
                                    "Value"
                                ),
                            ),
                            arn=(
                                f"arn:aws:ec2::{instances['OwnerId']}:"
                                f"instance-id/{instance['InstanceId']}"
                            ),
                            values=(
                                shutdown_behavior[
                                    "InstanceInitiatedShutdownBehavior"
                                ]["Value"],
                            ),
                            description=t(
                                "lib_path.f333.cfn_ec2_allows_shutdown_command"
                            ),
                        ),
                    ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=shutdown_behavior,
                ),
            )

    return vulns


def iterate_ec2_has_associate_public_ip_address(
    instance: Dict[str, Any], instances: Dict[str, Any]
) -> List[Location]:
    locations: List[Location] = []
    for index, interface in enumerate(instance["NetworkInterfaces"]):
        if "Association" in interface and interface["Association"]["PublicIp"]:
            locations = [
                *locations,
                Location(
                    access_patterns=(
                        (
                            f"/NetworkInterfaces/{index}"
                            "/Association/PublicIp"
                        ),
                    ),
                    arn=(
                        f"arn:aws:ec2::{instances['OwnerId']}:"
                        f"instance-id/{instance['InstanceId']}"
                    ),
                    values=(interface["Association"]["PublicIp"],),
                    description=t(
                        "lib_path.f333.cfn_ec2_associate_public_ip_address"
                    ),
                ),
            ]
    return locations


async def ec2_has_associate_public_ip_address(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_instances",
    )
    reservations = response.get("Reservations", []) if response else []
    method = core_model.MethodsEnum.AWS_EC2_HAS_ASSOCIATE_PUBLIC_IP_ADDRESS
    vulns: core_model.Vulnerabilities = ()
    if reservations:
        for instances in reservations:
            for instance in instances["Instances"]:
                locations = iterate_ec2_has_associate_public_ip_address(
                    instance, instances
                )
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=instance,
                    ),
                )

    return vulns


async def ec2_iam_instances_without_profile(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_instances"
    )
    instances = response.get("Reservations", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    for instance in instances:
        locations: List[Location] = []
        for config in instance["Instances"]:
            if (
                "IamInstanceProfile" not in config.keys()
                and config["State"]["Name"] != "terminated"
            ):
                locations = [
                    *locations,
                    Location(
                        arn=(
                            f"arn:aws:ec2::{instance['OwnerId']}:"
                            f"instance-id/{config['InstanceId']}"
                        ),
                        description=t(
                            "src.lib_path.f333."
                            "ec2_has_not_an_iam_instance_profile"
                        ),
                        values=(),
                        access_patterns=(),
                    ),
                ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(
                    core_model.MethodsEnum.AWS_EC2_IAM_INSTANCE_WITHOUT_PROFILE
                ),
                aws_response=instance,
            ),
        )
    return vulns


async def has_unused_ec2_key_pairs(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_key_pairs"
    )
    key_pairs = response.get("KeyPairs", []) if response else []

    vulns: core_model.Vulnerabilities = ()

    for key in key_pairs:
        locations: List[Location] = []
        filters = [
            {"Name": "instance-state-name", "Values": ["running"]},
            {"Name": "key-name", "Values": [key["KeyName"]]},
        ]
        instances: Dict[str, Any] = await run_boto3_fun(
            credentials,
            service="ec2",
            function="describe_instances",
            parameters={"Filters": filters},
        )
        reservations = instances["Reservations"]
        if not reservations:
            locations = [
                *locations,
                Location(
                    arn=(f"arn:aws:ec2::keyPairIs:{key['KeyPairId']}"),
                    description=t("lib_path.f333.has_unused_ec2_key_pairs"),
                    values=(),
                    access_patterns=(),
                ),
            ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_EC2_HAS_UNUSED_KEY_PAIRS),
                aws_response=instances,
            ),
        )
    return vulns


CHECKS: Tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, Tuple[Vulnerability, ...]]],
    ...,
] = (
    ec2_has_terminate_shutdown_behavior,
    ec2_has_associate_public_ip_address,
    ec2_iam_instances_without_profile,
    has_unused_ec2_key_pairs,
)
