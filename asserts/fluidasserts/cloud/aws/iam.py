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
