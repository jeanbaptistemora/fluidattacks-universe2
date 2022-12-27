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
