# -*- coding: utf-8 -*-
"""AWS cloud checks (CloudTrail)."""


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


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def trails_not_multiregion(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if trails are multiregion.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    trails = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="cloudtrail",
        func="describe_trails",
        param="trailList",
        retry=retry,
    )

    msg_open: str = "Trails are not multiregion"
    msg_closed: str = "All trails are multiregion"

    vulns, safes = [], []

    if trails:
        for trail in trails:
            trail_arn = trail["TrailARN"]

            (vulns if not trail["IsMultiRegionTrail"] else safes).append(
                (trail_arn, "Must be multi-region")
            )

    return _get_result_as_tuple(
        service="CloudTrail",
        objects="trails",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unencrypted_logs(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if trail logs are encrypted.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    trails = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="cloudtrail",
        func="describe_trails",
        param="trailList",
        retry=retry,
    )

    msg_open: str = "Trails logs are not encrypted"
    msg_closed: str = "KMS key found in trails"

    vulns, safes = [], []

    if trails:
        for trail in trails:
            trail_arn = trail["TrailARN"]

            (vulns if not trail.get("KmsKeyId") else safes).append(
                (trail_arn, "Logs must be encrypted")
            )

    return _get_result_as_tuple(
        service="CloudTrail",
        objects="trails",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
