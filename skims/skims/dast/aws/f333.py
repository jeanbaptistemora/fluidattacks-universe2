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


async def has_unused_seggroups(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = response.get("SecurityGroups", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations: List[Location] = []
            net_interfaces = await run_boto3_fun(
                credentials,
                service="ec2",
                function="describe_network_interfaces",
                parameters={
                    "Filters": [
                        {
                            "Name": "group-id",
                            "Values": [
                                group["GroupId"],
                            ],
                        }
                    ]
                },
            )
            network_interfaces = (
                net_interfaces.get("NetworkInterfaces", []) if response else []
            )
            if not network_interfaces:
                locations = [
                    *[
                        Location(
                            access_patterns=(),
                            arn=(
                                f"arn:aws:ec2::{group['OwnerId']}:"
                                f"security-group/{group['GroupId']}"
                            ),
                            values=(network_interfaces,),
                            description=t(
                                "lib_path.f333.has_unused_secgroups"
                            ),
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_EC2_HAS_UNUSED_SEGGROUPS
                    ),
                    aws_response=net_interfaces,
                ),
            )
    return vulns


async def has_unencrypted_amis(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_images",
        parameters={"Owners": ["self"]},
    )
    images = response.get("Images", []) if response else []
    vulns: core_model.Vulnerabilities = ()

    if images:
        for image in images:
            locations: List[Location] = []
            for index, block in enumerate(image["BlockDeviceMappings"]):
                with suppress(KeyError):
                    if not block["Ebs"].get("Encrypted", True):
                        locations = [
                            *locations,
                            *[
                                Location(
                                    access_patterns=(
                                        (
                                            f"/BlockDeviceMappings/"
                                            f"{index}/Ebs/Encrypted"
                                        ),
                                    ),
                                    arn=(
                                        "arn:aws:ec2::ImageId:"
                                        f"{image['ImageId']}"
                                    ),
                                    values=(block["Ebs"]["Encrypted"],),
                                    description=t(
                                        "lib_path.f333.has_unencrypted_amis"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(
                        core_model.MethodsEnum.AWS_EC2_HAS_UNENCRYPTED_AMIS
                    ),
                    aws_response=image,
                ),
            )
    return vulns


async def has_publicly_shared_amis(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_images",
        parameters={"Owners": ["self"]},
    )
    images = response.get("Images", []) if response else []
    vulns: core_model.Vulnerabilities = ()
    locations: List[Location] = []
    for image in images:
        if image.get("Public", False):
            locations = [
                Location(
                    arn=(f"arn:aws:ec2::ImageId:{image['ImageId']}"),
                    description=t("lib_path.f333.has_publicly_shared_amis"),
                    values=(image.get("Public"),),
                    access_patterns=("/Public",),
                ),
            ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core_model.MethodsEnum.AWS_HAS_PUBLICLY_SHARED_AMIS),
                aws_response=image,
            ),
        )
    return vulns


async def has_unencrypted_snapshots(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    vulns: core_model.Vulnerabilities = ()
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="sts",
        function="get_caller_identity",
    )

    if not response.get("Account", False):
        return vulns

    describe_snapshots: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_snapshots",
        parameters={"OwnerIds": [response["Account"]]},
    )
    snapshots = describe_snapshots.get("Snapshots", [])
    method = core_model.MethodsEnum.AWS_EC2_HAS_UNENCRYPTED_SNAPSHOTS
    locations: List[Location] = []
    if snapshots:
        for snapshot in snapshots:
            snapshot_id = snapshot["SnapshotId"]
            if not snapshot.get("Encrypted", True):
                locations = [
                    Location(
                        arn=(f"arn:aws:ec2::Snapshot:{snapshot_id}"),
                        description=t(
                            "lib_path.f333.has_unencrypted_snapshots"
                        ),
                        values=(snapshot["Encrypted"],),
                        access_patterns=("/Encrypted",),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=snapshot,
                ),
            )
    return vulns


async def has_defined_user_data(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    """
    Reference:
    https://www.mitiga.io/blog/identifying-userdata-script-manipulation-
    accelerates-investigation
    """
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_instances",
    )
    reservations = response.get("Reservations", []) if response else []
    method = core_model.MethodsEnum.AWS_EC2_HAS_DEFINED_USER_DATA
    vulns: core_model.Vulnerabilities = ()
    if reservations:
        for instances in reservations:
            locations: List[Location] = []
            for instance in instances["Instances"]:
                describe_instance_attribute: Dict[
                    str, Any
                ] = await run_boto3_fun(
                    credentials,
                    service="ec2",
                    function="describe_instance_attribute",
                    parameters={
                        "Attribute": "userData",
                        "InstanceId": instance["InstanceId"],
                    },
                )
                user_data = describe_instance_attribute.get("UserData")
                if not user_data:
                    locations = [
                        *locations,
                        Location(
                            access_patterns=(),
                            arn=(
                                f"arn:aws:ec2::{instances['OwnerId']}:"
                                f"instance-id/{instance['InstanceId']}"
                            ),
                            values=(user_data,),
                            description=t(
                                "lib_path.f333.has_defined_user_data"
                            ),
                        ),
                    ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=describe_instance_attribute,
                    ),
                )

    return vulns


async def has_instances_using_unapproved_amis(
    credentials: AwsCredentials,
) -> core_model.Vulnerabilities:
    response: Dict[str, Any] = await run_boto3_fun(
        credentials,
        service="ec2",
        function="describe_instances",
    )
    reservations = response.get("Reservations", []) if response else []
    method = core_model.MethodsEnum.AWS_EC2_HAS_INSTANCES_USING_UNAPPROVED_AMIS
    vulns: core_model.Vulnerabilities = ()
    if reservations:
        for instances in reservations:
            locations: List[Location] = []
            for instance in instances["Instances"]:
                describe_images: Dict[str, Any] = await run_boto3_fun(
                    credentials,
                    service="ec2",
                    function="describe_images",
                    parameters={
                        "ImageIds": [instance["ImageId"]],
                    },
                )
                images = describe_images.get("Images", [])
                if (
                    images
                    and "ImageOwnerAlias" in images[0].keys()
                    and images[0]["ImageOwnerAlias"] != "amazon"
                ):
                    locations = [
                        Location(
                            access_patterns=("/Images/0/ImageOwnerAlias",),
                            arn=(
                                f"arn:aws:ec2::{instances['OwnerId']}:"
                                f"instance-id/{instance['InstanceId']}"
                            ),
                            values=(images[0]["ImageOwnerAlias"],),
                            description=t(
                                "lib_path.f333."
                                "has_instances_using_unapproved_amis"
                            ),
                        ),
                    ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(method),
                        aws_response=describe_images,
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
    has_publicly_shared_amis,
    has_unencrypted_snapshots,
    has_unused_seggroups,
    has_unencrypted_amis,
    has_defined_user_data,
    has_instances_using_unapproved_amis,
)
