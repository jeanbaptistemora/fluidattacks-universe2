# -*- coding: utf-8 -*-

"""AWS cloud checks (Cloudfront)."""

# standard imports
from typing import List

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, LOW
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_not_geo_restrictions(key_id: str, secret: str,
                             retry: bool = True) -> tuple:
    """
    Check if distributions has geo restrictions.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    distributions = aws.run_boto3_func(key_id=key_id,
                                       secret=secret,
                                       service='cloudfront',
                                       func='list_distributions',
                                       param='DistributionList',
                                       retry=retry)

    msg_open: str = 'There are distributions without geo-restrictions'
    msg_closed: str = 'All distributions have geo-restrictions'

    vuln_distribution_ids: List[str] = []
    safe_distribution_ids: List[str] = []

    if distributions:
        for dist in distributions['Items']:
            dist_id = dist['Id']
            config = aws.run_boto3_func(key_id=key_id,
                                        secret=secret,
                                        service='cloudfront',
                                        func='get_distribution_config',
                                        param='DistributionConfig',
                                        retry=retry,
                                        Id=dist_id)
            restrictions = config['Restrictions']
            geo_restriction = restrictions['GeoRestriction']
            geo_restriction_type = geo_restriction['RestrictionType']

            (vuln_distribution_ids
             if geo_restriction_type == 'none'
             else safe_distribution_ids).append(f'Distribution {dist_id}')

    else:
        msg_closed = 'No distributions were found'

    return _get_result_as_tuple(
        service='CloudFront',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vuln_distribution_ids, safes=safe_distribution_ids)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_logging_disabled(key_id: str, secret: str,
                         retry: bool = True) -> tuple:
    """
    Check if distributions has logging enabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    distributions = aws.run_boto3_func(key_id=key_id,
                                       secret=secret,
                                       service='cloudfront',
                                       func='list_distributions',
                                       param='DistributionList',
                                       retry=retry)

    msg_open: str = 'There are distributions without logging enabled'
    msg_closed: str = 'All distributions have logging enabled'

    vuln_distribution_ids: List[str] = []
    safe_distribution_ids: List[str] = []

    if distributions:
        for dist in distributions['Items']:
            dist_id = dist['Id']
            config = aws.run_boto3_func(key_id=key_id,
                                        secret=secret,
                                        service='cloudfront',
                                        func='get_distribution',
                                        param='Distribution',
                                        retry=retry,
                                        Id=dist_id)

            distribution_config = config['DistributionConfig']
            is_logging_enabled = distribution_config['Logging']['Enabled']

            (vuln_distribution_ids
             if not is_logging_enabled
             else safe_distribution_ids).append(f'Distribution {dist_id}')

    else:
        msg_closed = 'No distributions were found'

    return _get_result_as_tuple(
        service='CloudFront',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vuln_distribution_ids, safes=safe_distribution_ids)
