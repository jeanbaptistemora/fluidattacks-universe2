# -*- coding: utf-8 -*-

# pylint: disable=too-many-lines
"""AWS cloud checks (EC2)."""


from botocore.exceptions import (
    BotoCoreError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
)
from contextlib import (
    suppress,
)
from fluidasserts import (
    DAST,
    HIGH,
    LOW,
    MEDIUM,
)
from fluidasserts.cloud.aws import (
    _get_result_as_tuple,
)
from fluidasserts.helper import (
    aws,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)


def _check_port_in_seggroup(port: int, group: dict) -> list:
    """Check if port is open according to security group."""
    vuln = []
    for perm in group["IpPermissions"]:
        with suppress(KeyError):
            if perm["FromPort"] <= port <= perm["ToPort"]:
                vuln += [
                    perm
                    for x in perm["IpRanges"]
                    if x["CidrIp"] == "0.0.0.0/0"
                ]
                vuln += [
                    perm for x in perm["Ipv6Ranges"] if x["CidrIp"] == "::/0"
                ]
    return vuln


def _flatten(elements, aux_list=None):
    aux_list = aux_list if aux_list is not None else []
    for i in elements:
        if isinstance(i, list):
            _flatten(i, aux_list)
        else:
            aux_list.append(i)
    return aux_list


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unencrypted_volumes(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if there are unencrypted volumes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    volumes = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="ec2",
        func="describe_volumes",
        param="Volumes",
        retry=retry,
    )

    msg_open: str = "Account have non-encrypted volumes"
    msg_closed: str = "All volumes are encrypted"

    vulns, safes = [], []

    if volumes:
        for volume in volumes:
            volume_id = volume["VolumeId"]
            (vulns if not volume["Encrypted"] else safes).append(
                (volume_id, "Must be encrypted")
            )

    return _get_result_as_tuple(
        service="EC2",
        objects="volumes",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unencrypted_snapshots(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if there are unencrypted snapshots.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    identity = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="sts",
        func="get_caller_identity",
        retry=retry,
    )
    snapshots = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="ec2",
        func="describe_snapshots",
        param="Snapshots",
        OwnerIds=[identity["Account"]],
        retry=retry,
    )

    msg_open: str = "Account have non-encrypted snapshots"
    msg_closed: str = "All snapshots are encrypted"

    vulns, safes = [], []

    if snapshots:
        for snapshot in snapshots:
            snapshot_id = snapshot["SnapshotId"]
            (vulns if not snapshot["Encrypted"] else safes).append(
                (snapshot_id, "Must be encrypted")
            )

    return _get_result_as_tuple(
        service="EC2",
        objects="snapshots",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unused_seggroups(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if there are unused security groups.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    security_groups = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="ec2",
        func="describe_security_groups",
        param="SecurityGroups",
        retry=retry,
    )

    msg_open: str = "Some security groups are not being used"
    msg_closed: str = "All security groups are being used"

    vulns, safes = [], []

    if security_groups:
        for group in security_groups:
            group_id = group["GroupId"]
            net_interfaces = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={"aws_session_token": session_token},
                service="ec2",
                func=("describe_" "network_interfaces"),
                param="NetworkInterfaces",
                Filters=[
                    {
                        "Name": "group-id",
                        "Values": [
                            group["GroupId"],
                        ],
                    }
                ],
                retry=retry,
            )

            (vulns if not net_interfaces else safes).append(
                (group_id, "Must be used or deleted")
            )

    return _get_result_as_tuple(
        service="EC2",
        objects="security groups",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def vpcs_without_flowlog(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if VPCs have flow logs.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    virtual_clouds = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="ec2",
        func="describe_vpcs",
        param="Vpcs",
        Filters=[{"Name": "state", "Values": ["available"]}],
        retry=retry,
    )

    msg_open: str = "No Flow Logs found for VPC"
    msg_closed: str = "Flow Logs found for VPC"

    vulns, safes = [], []

    if virtual_clouds:
        for cloud in virtual_clouds:
            cloud_id = cloud["VpcId"]
            net_interfaces = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={"aws_session_token": session_token},
                service="ec2",
                func="describe_flow_logs",
                param="FlowLogs",
                Filters=[
                    {
                        "Name": "resource-id",
                        "Values": [cloud_id],
                    }
                ],
                retry=retry,
            )

            (vulns if not net_interfaces else safes).append(
                (cloud_id, "Must be used or deleted")
            )

    return _get_result_as_tuple(
        service="EC2",
        objects="virtual private clouds",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_instances_using_unapproved_amis(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if there are instances using approved Amazon Machine Images.

    To follow best practices use gold AMIs to create new instances of EC2.
    A golden AMI is an AMI that contains the latest security patches, software,
    configuration, security maintenance, and performance monitoring.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    """
    msg_open: str = (
        "Instances are being launched using "
        "unapproved Amazon Machine Images."
    )
    msg_closed: str = (
        "Instances are being launched using " "approved Amazon Machine Images."
    )
    vulns, safes = [], []

    instances = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="ec2",
        func="describe_instances",
        param="Reservations",
        retry=retry,
    )

    for instance in _flatten(map(lambda x: x["Instances"], instances)):
        images = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_images",
            param="Images",
            retry=retry,
            ImageIds=[instance["ImageId"]],
        )
        (
            vulns
            if images
            and "ImageOwnerAlias" in images[0].keys()
            and images[0]["ImageOwnerAlias"] != "amazon"
            else safes
        ).append(
            (instance["InstanceId"], "Base image must be approved by Amazon.")
        )

    return _get_result_as_tuple(
        service="EC2",
        objects="Instances",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unused_ec2_key_pairs(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if there are unused EC2 key pairs.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are unused EC2 key pairs.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "There are unused EC2 key pairs."
    msg_closed: str = "All EC2 key pairs are in use."
    vulns, safes = [], []

    key_pairs = map(
        lambda x: x["KeyName"],
        aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_key_pairs",
            param="KeyPairs",
            retry=retry,
        ),
    )
    for key in key_pairs:
        filters = [
            {"Name": "instance-state-name", "Values": ["running"]},
            {"Name": "key-name", "Values": [key]},
        ]

        instances = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_instances",
            param="Reservations",
            retry=retry,
            Filters=filters,
        )
        (vulns if not instances else safes).append(
            (key, "The EC2 key pair is not in use, it must be removed.")
        )
    return _get_result_as_tuple(
        service="EC2",
        objects="Key Pairs",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_default_security_groups_in_use(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if default security groups are in use.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are default security groups in use.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "Default security groups are in use."
    msg_closed: str = "Default security groups are not in use."
    vulns, safes = [], []

    instances = map(
        lambda x: x["Instances"],
        aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_instances",
            param="Reservations",
            retry=retry,
        ),
    )

    for instance in _flatten(list(instances)):
        security_groups = map(
            lambda x: x["GroupName"], instance["SecurityGroups"]
        )
        (vulns if "default" in security_groups else safes).append(
            (
                instance["InstanceId"],
                (
                    "This instance use a default security"
                    " group, specify a custom security group."
                ),
            )
        )

    return _get_result_as_tuple(
        service="EC2",
        objects="Instances",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unencrypted_amis(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if there are unencrypted AMIs.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are unencrypted AMIs.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "Amazon Machine Images (AMIs) are not encrypted."
    msg_closed: str = "Amazon Machine Images (AMIs) are encrypted."
    vulns, safes = [], []
    images = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="ec2",
        func="describe_images",
        param="Images",
        retry=retry,
        Owners=["self"],
    )

    for image in images:
        vulnerable = []
        for block in image["BlockDeviceMappings"]:
            with suppress(KeyError):
                vulnerable.append(not block["Ebs"]["Encrypted"])
        (vulns if any(vulnerable) else safes).append(
            (image["ImageId"], "This AMI must be encrypted.")
        )

    return _get_result_as_tuple(
        service="EC2",
        objects="AMIs",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_publicly_shared_amis(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if there are any publicly accessible AMIs within AWS account.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are any publicly accessible AMIs.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = (
        "There are any publicly accessible AMIs within AWS account."
    )
    msg_closed: str = (
        "There are not any publicly accessible AMIs within AWS account."
    )
    vulns, safes = [], []
    images = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="ec2",
        func="describe_images",
        param="Images",
        retry=retry,
        Owners=["self"],
    )

    for image in images:
        (vulns if image["Public"] else safes).append(
            (image["ImageId"], "The AMI must be private access.")
        )

    return _get_result_as_tuple(
        service="EC2",
        objects="AMIS",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_not_deletion_protection(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Verify if EC2 instance has not deletion protection enabled.

    By default EC2 Instances can be terminated using the Amazon EC2 console,
    CLI, or API.

    This is not desirable, as terminated instances are deleted from the account
    automatically after some time,
    personal may take-down the service without intention,
    and volumes attached to the instance may be lost and therefore wiped.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if the instance has not the **DisableApiTermination**
                parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "EC2 instances has API termination enabled."
    msg_closed: str = "EC2 instances has API termination disabled."
    vulns, safes = [], []

    instances = map(
        lambda x: x["Instances"],
        aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_instances",
            param="Reservations",
            retry=retry,
        ),
    )

    for instance in _flatten(list(instances)):
        disable_api_termination = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_instance_attribute",
            param="DisableApiTermination",
            Attribute="disableApiTermination",
            InstanceId=instance["InstanceId"],
            retry=retry,
        )["Value"]
        (vulns if not disable_api_termination else safes).append(
            (instance["InstanceId"], "must disabled api termination.")
        )

    return _get_result_as_tuple(
        service="EC2",
        objects="Instances",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_terminate_shutdown_behavior(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Verify if ``EC2::instance`` has **Terminate** as Shutdown Behavior.

    By default EC2 Instances can be terminated using the shutdown command,
    from the underlying operative system.

    This is not desirable, as terminated instances are deleted from the account
    automatically after some time,
    personal may take-down the service without intention,
    and volumes attached to the instance may be lost and therefore wiped.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if the instance has not the
                **InstanceInitiatedShutdownBehavior** attribute set to
                **terminate**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = (
        "EC2 instances allows the shutdown command to terminate the instance"
    )
    msg_closed: str = (
        "EC2 instances disallow the shutdown command to"
        " terminate the instance"
    )
    vulns, safes = [], []

    instances = map(
        lambda x: x["Instances"],
        aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_instances",
            param="Reservations",
            retry=retry,
        ),
    )

    for instance in _flatten(list(instances)):
        shutdown_behavior = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_instance_attribute",
            param="InstanceInitiatedShutdownBehavior",
            Attribute="instanceInitiatedShutdownBehavior",
            InstanceId=instance["InstanceId"],
            retry=retry,
        )["Value"]
        (vulns if shutdown_behavior == "terminate" else safes).append(
            (
                instance["InstanceId"],
                "do not set terminate as shutdown behavior",
            )
        )

    return _get_result_as_tuple(
        service="EC2",
        objects="Instances",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_associate_public_ip_address(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if ``EC2::Instance`` has associated public IP address.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are instances with associated public IPs.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "EC2 instances has associated public ip addresses."
    msg_closed: str = "EC2 instances has not associated public ip addresses."
    vulns, safes = [], []

    instances = map(
        lambda x: x["Instances"],
        aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_instances",
            param="Reservations",
            retry=retry,
        ),
    )

    for instance in _flatten(list(instances)):
        for interface in instance["NetworkInterfaces"]:
            (
                vulns
                if "Association" in interface
                and interface["Association"]["PublicIp"]
                else safes
            ).append(
                (
                    instance["InstanceId"],
                    "do not associate public IP addresses.",
                )
            )

    return _get_result_as_tuple(
        service="EC2",
        objects="Instances",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_defined_user_data(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Verify if ``EC2::instance`` has defined **userData** attribute.

    The **userData** attribute is a place on where attackers can inject
    commands that will be executed everytime during the instance startup.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if the instance has the
                **userData** attribute set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "EC2 instances has custom userData defined"
    msg_closed: str = "EC2 instances has not userData defined"
    vulns, safes = [], []

    instances = map(
        lambda x: x["Instances"],
        aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_instances",
            param="Reservations",
            retry=retry,
        ),
    )

    for instance in _flatten(list(instances)):
        user_data = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_instance_attribute",
            param="UserData",
            Attribute="userData",
            InstanceId=instance["InstanceId"],
            retry=retry,
        )
        (vulns if user_data else safes).append(
            (instance["InstanceId"], "userData defined")
        )

    return _get_result_as_tuple(
        service="EC2",
        objects="Instances",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
