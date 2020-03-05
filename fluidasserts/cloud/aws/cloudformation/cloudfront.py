"""AWS CloudFormation checks for ``CloudFront`` (Content Delivery Network)."""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _index,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def serves_content_over_http(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``Distributions`` are serving content over HTTP.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **ViewerProtocolPolicy** attribute is set
                to **allow-all**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    vulnerable_protocol_policy = ('allow-all',)
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::CloudFront::Distribution',
            ],
            exclude=exclude):
        found_issues: list = []

        protocol_policy = _index(
            dictionary=res_props,
            indexes=(
                'DistributionConfig',
                'DefaultCacheBehavior',
                'ViewerProtocolPolicy'))
        if any(map(protocol_policy.__eq__, vulnerable_protocol_policy)):
            found_issues.append(('DefaultCacheBehavior', protocol_policy))

        for cache_behavior in _index(
                dictionary=res_props,
                indexes=(
                    'DistributionConfig',
                    'CacheBehaviors',
                ),
                default=[]):
            protocol_policy = cache_behavior.get('ViewerProtocolPolicy')
            if any(map(protocol_policy.__eq__, vulnerable_protocol_policy)):
                found_issues.append(('CacheBehaviors', protocol_policy))

        for cache, policy in found_issues:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'AWS::CloudFront::Distribution'
                            f'/DistributionConfig'
                            f'/{cache}'
                            f'/ViewerProtocolPolicy'
                            f'/{policy}'),
                    identifier=res_name,
                    line=res_props['line'],
                    reason='allows HTTP traffic'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Distributions serve content over HTTP',
        msg_closed='Distributions serve content over HTTPs')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def serves_content_over_insecure_protocols(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``Distributions`` are using the strongest protocol from AWS.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **MinimumProtocolVersion** attribute is set
                to **SSLv3**, **TLSv1**, **TLSv1_2016**, or **TLSv1.1_2016**
                protocol.
              - ``OPEN`` if **OriginSSLProtocols** attribute is set
                to **SSLv3**, **TLSv1**, or **TLSv1.1** protocol.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    # Map:
    #  MinimumProtocolVersion:
    #    SSLv3 TLSv1
    #          TLSv1_2016
    #          TLSv1.1_2016
    #          TLSv1.2_2018 (best available)
    #  OriginSSLProtocols:
    #    SSLv3 TLSv1
    #          TLSv1.1
    #          TLSv1.2 (best available)
    vulnerabilities: list = []
    vulnerable_origin_ssl_protocols = \
        ('SSLv3', 'TLSv1', 'TLSv1.1')
    vulnerable_min_prot_versions = \
        ('SSLv3', 'TLSv1', 'TLSv1_2016', 'TLSv1.1_2016')
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_cfn_template(
            starting_path=path,
            resource_types=[
                'AWS::CloudFront::Distribution',
            ],
            exclude=exclude):
        minimum_protocol_version = _index(
            dictionary=res_props,
            indexes=(
                'DistributionConfig',
                'ViewerCertificate',
                'MinimumProtocolVersion',
            ),
            default=None)
        if minimum_protocol_version in vulnerable_min_prot_versions:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'AWS::CloudFront::Distribution'
                            f'/DistributionConfig'
                            f'/ViewerCertificate'
                            f'/MinimumProtocolVersion'
                            f'/{minimum_protocol_version}'),
                    identifier=res_name,
                    line=res_props['line'],
                    reason='is not the strongest protocol provided by AWS'))

        for origin in _index(
                dictionary=res_props,
                indexes=(
                    'DistributionConfig',
                    'Origins',
                ),
                default=[]):
            for origin_ssl_protocol in _index(
                    dictionary=origin,
                    indexes=(
                        'CustomOriginConfig',
                        'OriginSSLProtocols',
                    ),
                    default=[]):
                if origin_ssl_protocol in vulnerable_origin_ssl_protocols:
                    vulnerabilities.append(
                        Vulnerability(
                            path=yaml_path,
                            entity=(f'AWS::CloudFront::Distribution'
                                    f'/DistributionConfig'
                                    f'/Origins'
                                    f'/CustomOriginConfig'
                                    f'/OriginSSLProtocols'
                                    f'/{origin_ssl_protocol}'),
                            identifier=res_name,
                            line=res_props['line'],
                            reason=('is not the strongest protocol '
                                    'provided by AWS')))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Distributions are using weak protocols',
        msg_closed='Distributions use the strongest protocol provided by AWS')
