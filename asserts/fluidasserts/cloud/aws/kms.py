# -*- coding: utf-8 -*-
"""AWS cloud checks (KMS)."""


from botocore.exceptions import (
    BotoCoreError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
)
from fluidasserts import (
    DAST,
    HIGH,
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


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_key_rotation_disabled(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if master keys have Key Rotation disabled.

    See https://docs.aws.amazon.com/es_es/kms/latest/developerguide/
    rotate-keys.html

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :returns: - ``OPEN`` if there are keys with key rotation disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "Master keys have key rotation disabled."
    msg_closed: str = "Master keys have Key Rotation enabled."
    vulns, safes = [], []
    keys = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="kms",
        func="list_keys",
        param="Keys",
        retry=retry,
    )

    for key in keys:
        try:
            key_rotation = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={"aws_session_token": session_token},
                service="kms",
                func="get_key_rotation_status",
                param="KeyRotationEnabled",
                KeyId=key["KeyId"],
                retry=retry,
                retry_times=3,
            )
        except aws.ClientErr:
            continue

        (vulns if not key_rotation else safes).append(
            (key["KeyArn"], "Master Keys rotation must be enabled.")
        )

    return _get_result_as_tuple(
        service="KMS",
        objects="Keys",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
