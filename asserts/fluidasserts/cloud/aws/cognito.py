# -*- coding: utf-8 -*-
"""AWS cloud checks (Cognito)."""


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


def _get_pools(key_id, retry, secret, session_token):
    return aws.get_paginated_items(
        key_id,
        retry,
        secret,
        session_token,
        "cognito-idp",
        "list_user_pools",
        "MaxResults",
        "NextToken",
        "UserPools",
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def advanced_security_disabled(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if Cognito has Advanced Security enabled.

    https://docs.aws.amazon.com/cognito/latest/developerguide/
    managing-security.html

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    vulns, safes = [], []
    pools = _get_pools(key_id, retry, secret, session_token)
    for pool in pools:
        userpool = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service="cognito-idp",
            func="describe_user_pool",
            boto3_client_kwargs={"aws_session_token": session_token},
            param="UserPool",
            UserPoolId=pool["Id"],
            retry=retry,
        )
        addons = userpool.get("UserPoolAddOns", {})

        (
            vulns
            if not (
                addons and (addons.get("AdvancedSecurityMode", "") == "ON")
            )
            else safes
        ).append(
            (pool["Id"], "User Pools must have Advanced " "Security enabled ")
        )

    msg_open: str = f"Advanced Security is not enabled"
    msg_closed: str = f"Advanced Security is enabled"

    return _get_result_as_tuple(
        service="Cognito",
        objects="Advanced Security",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
