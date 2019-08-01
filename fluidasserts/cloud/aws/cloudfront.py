# -*- coding: utf-8 -*-

"""AWS cloud checks (Cloudfront)."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import track, level, notify
from fluidasserts.helper import aws


@notify
@level('low')
@track
def has_not_geo_restrictions(key_id: str, secret: str,
                             retry: bool = True) -> bool:
    """
    Check if distributions has geo restrictions.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        distros = aws.run_boto3_func(key_id, secret, 'cloudfront',
                                     'list_distributions',
                                     param='DistributionList',
                                     retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not distros:
        show_close('Not distributions were found')
        return False

    result = []

    for distro in distros['Items']:
        config = aws.run_boto3_func(key_id, secret, 'cloudfront',
                                    'get_distribution_config',
                                    param='DistributionConfig',
                                    retry=retry,
                                    Id=distro['Id'])
        if config['Restrictions']['GeoRestriction']['RestrictionType'] == \
                'none':
            result.append(distro['Id'])
    if result:
        show_open('Distributions has not geo restrictions',
                  details=dict(distribution=result))
        return True
    show_close('All distributions has geo restrictions')
    return False


@notify
@level('low')
@track
def has_logging_disabled(key_id: str, secret: str,
                         retry: bool = True) -> bool:
    """
    Check if distributions has logging enabled.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        distros = aws.run_boto3_func(key_id, secret, 'cloudfront',
                                     'list_distributions',
                                     param='DistributionList',
                                     retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not distros:
        show_close('Not distributions were found')
        return False

    result = []

    for distro in distros['Items']:
        config = aws.run_boto3_func(key_id, secret, 'cloudfront',
                                    'get_distribution',
                                    param='Distribution',
                                    retry=retry,
                                    Id=distro['Id'])
        if not config['DistributionConfig']['Logging']['Enabled']:
            result.append(distro['Id'])
    if result:
        show_open('Distributions has not logging enabled',
                  details=dict(distributions=result))
        return True
    show_close('All distributions has logging enabled')
    return False
