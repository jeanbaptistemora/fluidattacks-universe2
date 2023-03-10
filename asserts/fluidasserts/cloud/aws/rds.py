# -*- coding: utf-8 -*-
"""AWS cloud checks (RDS)."""


from botocore.exceptions import (
    BotoCoreError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
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


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_public_snapshots(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check for snapshots that allow public access.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are snapshots that allow public access.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "Snapshots are publicly accessible."
    msg_closed: str = "Snapshots are not publicly accessible."

    vulns, safes = [], []
    snapshots = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="rds",
        func="describe_db_snapshots",
        param="DBSnapshots",
        retry=retry,
    )
    for snapshot in snapshots:
        snapshot = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="rds",
            func="describe_db_snapshot_attributes",
            param="DBSnapshotAttributesResult",
            DBSnapshotIdentifier=snapshot["DBSnapshotIdentifier"],
            retry=retry,
        )
        vulnerable = any(
            list(
                map(
                    lambda x: "all" in x["AttributeValues"],
                    snapshot["DBSnapshotAttributes"],
                )
            )
        )

        (vulns if vulnerable else safes).append(
            (
                snapshot["DBSnapshotIdentifier"],
                "Disable public access from the snapshot.",
            )
        )

    return _get_result_as_tuple(
        service="RDS",
        objects="Snapshots",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_uses_iam_authentication(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if the BD instances are not using IAM database authentication.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are instances that do not use IAM database
                 authentication.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "Instances do not use IAM database authentication."
    msg_closed: str = "Instances use IAM database authentication."

    vulns, safes = [], []
    instances = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="rds",
        func="describe_db_instances",
        param="DBInstances",
        retry=retry,
    )

    for instance in instances:
        (
            vulns
            if not instance["IAMDatabaseAuthenticationEnabled"]
            else safes
        ).append(
            (instance["DBInstanceArn"], "Use IAM database authentication.")
        )

    return _get_result_as_tuple(
        service="RDS",
        objects="Instances",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def unrestricted_db_security_groups(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if the database security groups allow unrestricted access.

    AWS RDS DB security groups should not allow access from 0.0.0.0/0.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are instances that do not use IAM database
                 authentication.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = (
        "RDS DB security groups allow unrestricted access (0.0.0.0/0)"
    )
    msg_closed: str = "RDS DB security groups have restricted access."

    vulns, safes = [], []
    instances = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="rds",
        func="describe_db_instances",
        param="DBInstances",
        retry=retry,
    )
    for instance in instances:
        security_groups_ids = list(
            map(
                lambda x: x["VpcSecurityGroupId"],
                instance["VpcSecurityGroups"],
            )
        )
        security_groups = aws.run_boto3_func(
            key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="ec2",
            func="describe_security_groups",
            param="SecurityGroups",
            GroupIds=security_groups_ids,
            retry=retry,
        )
        vulnerable = []
        for group in security_groups:
            ip_permissions = (
                group["IpPermissions"] + group["IpPermissionsEgress"]
            )

            is_vulnerable: bool = any(
                ip_range["CidrIp"] == "0.0.0.0/0"
                for ip_permission in ip_permissions
                for ip_range in ip_permission["IpRanges"]
            )

            vulnerable.append(is_vulnerable)

        (vulns if any(vulnerable) else safes).append(
            (
                instance["DBInstanceArn"],
                "Restrict access to the required IP addresses only.",
            )
        )

    return _get_result_as_tuple(
        service="RDS",
        objects="instances",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
