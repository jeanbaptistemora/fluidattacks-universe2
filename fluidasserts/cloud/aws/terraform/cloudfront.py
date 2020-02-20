"""AWS CloudFormation checks for ``terraform`` (Content Delivery Network)."""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.terraform import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def serves_content_over_http(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if a ``aws_cloudfront_distribution`` is serving content over HTTP.

    :param path: Location of Terraform template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **ViewerProtocolPolicy** attribute is set
                to **allow-all**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: list = []
    vulnerable_protocol_policy = 'allow-all'
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_cloudfront_distribution',
            ],
            exclude=exclude):
        found_issues: list = []

        default_protocol_policy = res_props.get(
            'default_cache_behavior', {}).get('viewer_protocol_policy', "")
        if default_protocol_policy == vulnerable_protocol_policy:
            found_issues.append(('default_cache_behavior',
                                 default_protocol_policy))

        for cache_behavior in helper.force_list(res_props.get(
                'ordered_cache_behavior', [])):
            protocol_policy = cache_behavior.get('viewer_protocol_policy', "")
            if protocol_policy == vulnerable_protocol_policy:
                found_issues.append(('ordered_cache_behaviors',
                                     protocol_policy))

        for cache, policy in found_issues:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'aws_cloudfront_distribution'
                            f'/{cache}'
                            f'/viewer_protocol_policy'
                            f'/{policy}'),
                    identifier=res_name,
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
    Check if ``cf_distributions`` are using the strongest protocol from AWS.

    :param path: Location of Terraform template file.
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
    for yaml_path, res_name, res_props in helper.iterate_rsrcs_in_tf_template(
            starting_path=path,
            resource_types=[
                'aws_cloudfront_distribution',
            ],
            exclude=exclude):
        minimum_protocol_version = res_props.get(
            'viewer_certificate', {}).get('minimum_protocol_version', "TLSv1")
        if minimum_protocol_version in vulnerable_min_prot_versions:
            vulnerabilities.append(
                Vulnerability(
                    path=yaml_path,
                    entity=(f'aws_cloudfront_distribution'
                            f'/viewer_certificate'
                            f'/minimum_protocol_version'
                            f'/{minimum_protocol_version}'),
                    identifier=res_name,
                    reason='is not the strongest protocol provided by AWS'))
        origins = helper.force_list(res_props.get('origin', []))
        for origin in origins:
            protocols = helper.force_list(origin.get(
                'custom_origin_config', {}).get('origin_ssl_protocols', []))
            for origin_ssl_protocol in protocols:
                if origin_ssl_protocol in vulnerable_origin_ssl_protocols:
                    vulnerabilities.append(
                        Vulnerability(
                            path=yaml_path,
                            entity=(f'aws_cloudfront_distribution'
                                    f'/origin'
                                    f'/custom_origin_config'
                                    f'/origin_ssl_protocols'
                                    f'/{origin_ssl_protocol}'),
                            identifier=res_name,
                            reason=('is not the strongest protocol '
                                    'provided by AWS')))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Distributions are using weak protocols',
        msg_closed='Distributions use the strongest protocol provided by AWS')
