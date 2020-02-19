"""AWS CloudFormation checks for ``terraform`` (Content Delivery Network)."""

# Standard imports
from typing import List, Optional

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
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

        for cache_behavior in res_props.get('ordered_cache_behavior', []):
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
