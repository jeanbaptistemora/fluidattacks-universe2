"""AWS CloudFormation checks for ``CloudFront`` (Content Delivery Network)."""

# Standard imports
from typing import List, Optional, Tuple, Dict

# Treed imports
from networkx import DiGraph
from networkx.algorithms import dfs_preorder_nodes

# Local imports
from fluidasserts import SAST, MEDIUM, LOW
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import get_graph
from fluidasserts.cloud.aws.cloudformation import get_resources
from fluidasserts.cloud.aws.cloudformation import get_ref_nodes


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def serves_content_over_http(path: str,
                             exclude: Optional[List[str]] = None) -> tuple:
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
    vulnerable_protocol_policy = ('allow-all', )
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    distributions: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates), {'AWS', 'CloudFront', 'Distribution'},
        info=True)
    for dist, resource, template in distributions:
        default = get_resources(graph, dist, 'DefaultCacheBehavior', 3)
        view_policy = helper.get_index(
            get_resources(graph, default, 'ViewerProtocolPolicy'), 0)
        found_issues: list = []
        if view_policy:
            view_policy_node = get_ref_nodes(graph, view_policy,
                                             lambda x: isinstance(x, str))[0]
            value = graph.nodes[view_policy_node]
            if any(map(value['value'].__eq__, vulnerable_protocol_policy)):
                found_issues.append(('DefaultCacheBehavior', value['value'],
                                     value['line']))

        behaviors = get_resources(graph, dist, 'CacheBehaviors', 3)
        view_policies = get_resources(graph, behaviors, 'ViewerProtocolPolicy',
                                      4)
        for policy in view_policies:
            policy_node = get_ref_nodes(graph, policy,
                                        lambda x: isinstance(x, str))[0]
            value = graph.nodes[policy_node]
            if any(map(value['value'].__eq__, vulnerable_protocol_policy)):
                found_issues.append(('CacheBehaviors', value['value'],
                                     value['line']))

        for cache, policy, line in found_issues:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=(f'AWS::CloudFront::Distribution'
                            f'/DistributionConfig'
                            f'/{cache}'
                            f'/ViewerProtocolPolicy'
                            f'/{policy}'),
                    identifier=resource['name'],
                    line=line,
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
    vulnerabilities: List[Vulnerability] = []
    vulnerable_origin_ssl_protocols = ('SSLv3', 'TLSv1', 'TLSv1.1')
    vulnerable_min_prot_versions = ('SSLv3', 'TLSv1', 'TLSv1_2016',
                                    'TLSv1.1_2016')
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    distributions: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates), {'AWS', 'CloudFront', 'Distribution'},
        info=True)
    for dist, resource, template in distributions:
        version = helper.get_index(
            get_resources(graph, dist, 'MinimumProtocolVersion', depth=4), 0)
        if version:
            version_node = helper.get_index(
                get_ref_nodes(graph, version,
                              lambda x: x in vulnerable_min_prot_versions), 0)
            if version_node:
                value = graph.nodes[version_node]
                vulnerabilities.append(
                    Vulnerability(
                        path=template['path'],
                        entity=(f'AWS::CloudFront::Distribution'
                                f'/DistributionConfig'
                                f'/ViewerCertificate'
                                f'/MinimumProtocolVersion'
                                f'/{value["value"]}'),
                        identifier=resource['line'],
                        line=value['line'],
                        reason='is not the strongest protocol provided by AWS')
                )

        origins_nodes = helper.get_index(
            get_resources(graph, dist, 'OriginSSLProtocols', 7), 0)
        if origins_nodes:
            for origin_ssl_protocol in filter(
                    lambda x: 'value' in graph.nodes[x],
                    dfs_preorder_nodes(graph, origins_nodes, 4)):
                value = graph.nodes[origin_ssl_protocol]
                if value['value'] in vulnerable_origin_ssl_protocols:
                    vulnerabilities.append(
                        Vulnerability(
                            path=template['path'],
                            entity=(f'AWS::CloudFront::Distribution'
                                    f'/DistributionConfig'
                                    f'/Origins'
                                    f'/CustomOriginConfig'
                                    f'/OriginSSLProtocols'
                                    f'/{value["value"]}'),
                            identifier=resource['name'],
                            line=value['line'],
                            reason=('is not the strongest protocol '
                                    'provided by AWS')))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Distributions are using weak protocols',
        msg_closed='Distributions use the strongest protocol provided by AWS')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_geo_restrictions(path: str,
                             exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``Distributions`` has geo restrictions.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **GeoRestriction** attribute is set
                to **none**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    distributions: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates), {'AWS', 'CloudFront', 'Distribution'},
        info=True)
    for dist, resource, template in distributions:
        line = resource['line']
        found_issues: list = []
        restrictions = helper.get_index(
            get_resources(graph, dist, 'GeoRestriction', 4), 0)
        if restrictions:
            line = graph.nodes[restrictions]['line']
        rest_type = helper.get_index(
            get_resources(graph, dist, 'RestrictionType', 5), 0)

        res_value = None
        if rest_type:
            rest_node = helper.get_index(get_ref_nodes(graph, rest_type), 0)
            res_value = graph.nodes[rest_node]['value']
        if not rest_type or (res_value and res_value == 'none'):
            found_issues.append(('GeoRestriction', restrictions))

        for issue in found_issues:
            locations_node = helper.get_index(
                get_resources(graph, issue[1], 'Item'), 0)
            locations = None
            if locations_node:
                value = helper.get_index(
                    get_ref_nodes(graph, locations_node,
                                  lambda x: isinstance(x, str)), 0)
                locations = value['value'] if value else None

            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=(f'AWS::CloudFront::Distribution'
                            f'/DistributionConfig'
                            f'/Restrictions'
                            f'/GeoRestriction/'
                            f'{locations}'),
                    identifier=resource['name'],
                    line=line,
                    reason='has no GeoRestriction'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Distributions have no geo restrictions',
        msg_closed='Distributions have geo restrictions')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_logging_disabled(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``Distributions`` have logging disabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **GeoRestriction** attribute is set
                to **none**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    distributions: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates), {'AWS', 'CloudFront', 'Distribution'},
        info=True)
    for dist, resource, template in distributions:
        line = resource['line']
        logging = get_resources(graph, dist, 'Logging', 4)
        if not logging:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=(f'AWS::CloudFront::Distribution'
                            f'/DistributionConfig'
                            f'/Logging'),
                    identifier=resource['name'],
                    line=line,
                    reason='has no GeoRestriction'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='Distributions have no geo restrictions',
        msg_closed='Distributions have geo restrictions')
