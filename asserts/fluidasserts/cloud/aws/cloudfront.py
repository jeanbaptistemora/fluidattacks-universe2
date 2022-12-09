# -*- coding: utf-8 -*-
"""AWS cloud checks (Cloudfront)."""


from botocore.exceptions import (
    BotoCoreError,
)
from botocore.vendored.requests.exceptions import (
    RequestException,
)
from fluidasserts import (
    DAST,
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
def has_not_geo_restrictions(
    key_id: str, secret: str, session_token: str = None, retry: bool = True
) -> tuple:
    """
    Check if distributions has geo restrictions.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    distributions = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={"aws_session_token": session_token},
        service="cloudfront",
        func="list_distributions",
        param="DistributionList",
        retry=retry,
    )

    msg_open: str = "There are distributions without geo-restrictions"
    msg_closed: str = "All distributions have geo-restrictions"

    vulns, safes = [], []

    if distributions:
        for dist in distributions["Items"]:
            dist_id = dist["Id"]
            dist_arn = dist["ARN"]
            config = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                boto3_client_kwargs={"aws_session_token": session_token},
                service="cloudfront",
                func="get_distribution_config",
                param="DistributionConfig",
                retry=retry,
                Id=dist_id,
            )
            restrictions = config["Restrictions"]
            geo_restriction = restrictions["GeoRestriction"]
            geo_restriction_type = geo_restriction["RestrictionType"]
            (vulns if geo_restriction_type == "none" else safes).append(
                (dist_arn, "Distribution must be geo-restricted")
            )

    return _get_result_as_tuple(
        service="CloudFront",
        objects="distributions",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
