# -*- coding: utf-8 -*-
# pylint: disable=too-many-lines
"""AWS cloud checks (IAM)."""


from botocore.exceptions import (
    BotoCoreError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
)
from contextlib import (
    suppress,
)
from datetime import (
    datetime,
    timedelta,
)
from dateutil import (
    parser,
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
import pytz


def _any_to_list(_input):
    """Convert anything to list."""
    if isinstance(_input, str):
        res = [_input]
    else:
        res = list(_input)
    return res


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_not_support_role(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if there is a support role.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    policies = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="iam",
        func="list_policies",
        param="Policies",
        retry=retry,
    )

    msg_open: str = (
        "There are not entities attached to the AWSSupportAccess policy"
    )
    msg_closed: str = (
        "There are entities attached to the AWSSupportAccess policy"
    )

    vulns, safes = [], []

    support_policies = [
        p
        for p in policies
        if p["PolicyName"] == "AWSSupportAccess" and p["AttachmentCount"] > 0
    ]

    for policy in support_policies:
        policy_arn = policy["Arn"]

        entities = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="iam",
            func="list_entities_for_policy",
            PolicyArn=policy_arn,
            retry=retry,
        )

        attached_times = (
            len(list(filter(None, entities["PolicyUsers"])))
            + len(list(filter(None, entities["PolicyGroups"])))
            + len(list(filter(None, entities["PolicyRoles"])))
        )

        (vulns if attached_times == 0 else safes).append(
            (policy_arn, "Must have entities attached")
        )

    (safes if support_policies else vulns).append(
        ("Policies/AWSSupportAccess", "Must be present")
    )

    return _get_result_as_tuple(
        service="IAM",
        objects="Support Access policies",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_root_active_signing_certificates(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if user root has activated signing certificates.

    To comply with the best security practices, make sure that the root user
    is not using X.590 certificates to make requests through the SOAP protocol
    to AWS. Disable any x.590 certificate for the root user, since it is used
    for daily tasks it is not a recommended practice.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    users = aws.credentials_report(
        key_id,
        secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        retry=retry,
    )

    msg_open: str = "Root user has activated signing certificates"
    msg_closed: str = "Root user does not have activated signing certificates"

    vulns, safes = [], []

    # Root user is always the first retrieved
    root_user = users[0]
    root_arn = root_user["arn"]

    root_has_active_signing_certs: bool = any(
        (
            root_user["cert_1_active"] == "true",
            root_user["cert_2_active"] == "true",
        )
    )

    (vulns if root_has_active_signing_certs else safes).append(
        (root_arn, "Must not have activate signing certificates")
    )

    return _get_result_as_tuple(
        service="IAM",
        objects="Credentials",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def users_with_password_and_access_keys(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if there are users with password and access keys activated.

    Make sure your IAM users do not access the API and console with the
    same account, in order to reduce the risk of unauthorized access in case
    the access keys or passwords are compromised.

    See https://nvd.nist.gov/800-53/Rev4/control/AC-5

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    vulns, safes = [], []

    msg_open: str = (
        "Users have access keys and password " "assigned for authentication."
    )
    msg_closed: str = (
        "Users have only keys or password "
        "assigned for authentication, but not both."
    )

    users = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="iam",
        func="list_users",
        param="Users",
        retry=retry,
    )

    client = aws.get_aws_client("iam", key_id, secret)

    for user in users:
        access_keys = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="iam",
            func="list_access_keys",
            param="AccessKeyMetadata",
            retry=retry,
            UserName=user["UserName"],
        )
        access_keys_activated: bool = any(
            map(lambda x: x["Status"], access_keys)
        )

        login_profile = None
        with suppress(client.exceptions.NoSuchEntityException):
            login_profile = aws.client_get_login_profile(
                client, user["UserName"]
            )

        (
            vulns
            if access_keys_activated and login_profile is not None
            else safes
        ).append(
            (
                user["Arn"],
                "User must have only password or access keys, but not both.",
            )
        )

    return _get_result_as_tuple(
        service="IAM",
        objects="Users",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def mfa_disabled_for_users_with_console_password(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if IAM Users with console password are not protected by MFA.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` .
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "Users with console password are not protected by MFA."
    msg_closed: str = "Users with console password are protected by MFA."
    vulns, safes = [], []

    users = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="iam",
        func="list_users",
        param="Users",
        retry=retry,
    )

    for user in users:
        try:
            aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={"aws_session_token": session_token},
                service="iam",
                func="get_login_profile",
                UserName=user["UserName"],
                param="LoginProfile",
                retry=retry,
                retry_times=3,
            )
        except aws.ClientErr:
            continue

        mfa_devices = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="iam",
            func="list_mfa_devices",
            UserName=user["UserName"],
            param="MFADevices",
            retry=retry,
        )
        (vulns if not mfa_devices else safes).append(
            (user["Arn"], "Enable MFA access protection for IAM user.")
        )

    return _get_result_as_tuple(
        service="IAM",
        objects="Users",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_old_ssh_public_keys(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Find IAM users keep any outdated (older than 90 days) SSH public keys.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are users with outdated SSH public keys.
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = (
        "There are users with old SSH public keys (older than 90 days)."
    )
    msg_closed: str = "Users have updated SSH public keys."
    vulns, safes = [], []

    three_months_ago = datetime.now() - timedelta(days=90)
    three_months_ago = three_months_ago.replace(tzinfo=pytz.UTC)

    users = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="iam",
        func="list_users",
        param="Users",
        retry=retry,
    )
    for user in users:
        keys = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={"aws_session_token": session_token},
            service="iam",
            func="list_ssh_public_keys",
            UserName=user["UserName"],
            param="SSHPublicKeys",
            retry=retry,
        )

        vulnerable = any(
            map(lambda x: x["UploadDate"] < three_months_ago, keys)
        )
        (vulns if vulnerable else safes).append(
            (user["Arn"], "Update old SSH public keys.")
        )

    return _get_result_as_tuple(
        service="IAM",
        objects="Users",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def allows_priv_escalation_by_policies_versions(
    key_id: str,
    secret: str,
    session_token: str = None,
    retry: bool = True,
    **boto3_kwargs,
):
    """
    Check if there are policy documents that allow privilege escalation.

    A policy document with both iam:CreatePolicyVersion and
    iam:SetDefaultPolicyVersion allows grantees to get full administrative
    access over the AWS tenant.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are policy documents that allow insecure
                permissions.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open = "Allows privilege escalation by policies versions."
    msg_closed = "Avoids privilege escalation by policies versions."
    vulns, safes = [], []
    policies = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={
            "aws_session_token": session_token,
            **boto3_kwargs,
        },
        service="iam",
        func="list_policies",
        Scope="Local",
        OnlyAttached=True,
    )["Policies"]

    for policy in policies:
        policy_version = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={
                "aws_session_token": session_token,
                **boto3_kwargs,
            },
            service="iam",
            func="get_policy_version",
            param="PolicyVersion",
            PolicyArn=policy["Arn"],
            VersionId=policy["DefaultVersionId"],
            retry=retry,
        )

        for stm in aws.force_list(policy_version["Document"]["Statement"]):
            vulnerable = (
                stm["Effect"] == "Allow"
                and "Resource" in stm
                and "iam:CreatePolicyVersion" in stm["Action"]
                and "iam:SetDefaultPolicyVersion" in stm["Action"]
            )
            (vulns if vulnerable else safes).append(
                (policy["Arn"], "allows privilege escalation")
            )
    return _get_result_as_tuple(
        service="IAM",
        objects="Policies",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def allows_priv_escalation_by_attach_policy(
    key_id: str,
    secret: str,
    session_token: str = None,
    retry: bool = True,
    **boto3_kwargs,
):
    """
    Check if there are policy documents that allow privilege escalation.

    A policy document with both iam:AttachUserPolicy allows grantees to
    attach any policy to the designed users, including a policy with full
    administrator rights
    access over the AWS tenant.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are policy documents that allow attaching
                policies.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open = "Allows privilege escalation by policies versions."
    msg_closed = "Avoids privilege escalation by policies versions."
    vulns, safes = [], []
    policies = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={
            "aws_session_token": session_token,
            **boto3_kwargs,
        },
        service="iam",
        func="list_policies",
        Scope="Local",
        OnlyAttached=True,
    )["Policies"]

    for policy in policies:
        policy_version = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            boto3_client_kwargs={
                "aws_session_token": session_token,
                **boto3_kwargs,
            },
            service="iam",
            func="get_policy_version",
            param="PolicyVersion",
            PolicyArn=policy["Arn"],
            VersionId=policy["DefaultVersionId"],
            retry=retry,
        )

        for stm in aws.force_list(policy_version["Document"]["Statement"]):
            vulnerable = (
                stm["Effect"] == "Allow"
                and "Resource" in stm
                and "iam:AttachUserPolicy" in stm["Action"]
            )
            (vulns if vulnerable else safes).append(
                (policy["Arn"], "allows privilege escalation")
            )
    return _get_result_as_tuple(
        service="IAM",
        objects="Policies",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
