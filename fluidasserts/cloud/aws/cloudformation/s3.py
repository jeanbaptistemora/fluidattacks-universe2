"""AWS CloudFormation checks for ``S3`` (Simple Storage Service)."""

# Standard imports
from typing import List, Optional, Set, Dict, Tuple

# Treed imports
from networkx import DiGraph

# Local imports
from fluidasserts import SAST, HIGH, LOW, MEDIUM
from fluidasserts.helper import aws as helper
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import get_graph
from fluidasserts.cloud.aws.cloudformation import get_list_node_items
from fluidasserts.cloud.aws.cloudformation import get_resources
from fluidasserts.cloud.aws.cloudformation import get_ref_nodes
from fluidasserts.cloud.aws.cloudformation import has_values

#: A set of available S3 Access Controls
ACCESS_CONTROLS = {
    'Private',
    'PublicRead',
    'PublicReadWrite',
    'AuthenticatedRead',
    'BucketOwnerRead',
    'BucketOwnerFullControl',
}


@unknown_if(FileNotFoundError)
def _has_not_access_control_in_list(
        path: str,
        msg_open: str,
        msg_closed: str,
        vulnerability_reason: str,
        safe_access_controls: Set[str],
        exclude: Optional[List[str]] = None) -> list:
    safe_access_controls = set(safe_access_controls)
    helper.validate_access_controls(safe_access_controls, ACCESS_CONTROLS)
    vulnerable_access_controls = ACCESS_CONTROLS - safe_access_controls
    vulnerabilities: List[Vulnerability] = []

    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    buckets: List[int] = get_resources(graph, map(lambda x: x[0], templates),
                                       {'AWS', 'S3', 'Bucket'}, info=True)
    for bucket, resource, template in buckets:
        line: int = resource['line']
        access_control: str = 'Private'
        access_control_node: int = helper.get_index(
            get_resources(graph, bucket, 'AccessControl'), 0)

        if access_control_node:
            access_control_value_node: int = get_ref_nodes(
                graph, access_control_node, lambda x: isinstance(x, str))[0]
            access_control = graph.nodes[access_control_value_node]['value']
            line = graph.nodes[access_control_value_node]['line']

        if not isinstance(access_control, str):
            continue
        if access_control in vulnerable_access_controls:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=(f'AWS::S3::Bucket/'
                            f'AccessControl/'
                            f'{access_control}'),
                    identifier=resource['name'],
                    line=line,
                    reason=vulnerability_reason))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open=msg_open,
        msg_closed=msg_closed)


@api(risk=HIGH, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_private_access_control(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``S3::Bucket`` has an **AccessControl** that is not **Private**.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the **S3 Bucket** has the **AccessControl**
                attribute set to **PublicRead**, **PublicReadWrite**,
                **AuthenticatedRead**, **BucketOwnerRead** or
                **BucketOwnerFullControl**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    return _has_not_access_control_in_list(
        path=path,
        msg_open='S3 Bucket has not Private Access Control',
        msg_closed='S3 Bucket has Private Access Control',
        vulnerability_reason='is not Private',
        safe_access_controls={
            'Private',
        },
        exclude=exclude,
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_access_logging_disabled(path: str,
                                exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``S3 Bucket`` has **Logging** disabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **AccessLoggingPolicy/Enabled** attribute is not
                set or set to **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[int] = get_templates(graph, path, exclude)
    buckets: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {'AWS', 'S3', 'Bucket'},
        num_labels=3,
        info=True)
    for bucket, resource, template in buckets:
        _logging: int = helper.get_index(
            get_resources(graph, bucket, 'LoggingConfiguration', depth=4), 0)

        if not _logging:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=(f'AWS::S3::Bucket/'
                            f'LoggingConfiguration/'),
                    identifier=resource['name'],
                    line=resource['line'],
                    reason='has logging disabled.'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='S3 buckets have logging disabled',
        msg_closed='S3 Buckets have logging enabled')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_encryption_disabled(path: str,
                            exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``S3 Bucket`` has **Encryption** disabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **BucketEncryption** attribute is not
                set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[int] = get_templates(graph, path, exclude)
    buckets: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {'AWS', 'S3', 'Bucket'},
        num_labels=3,
        info=True)
    for bucket, resource, template in buckets:
        _encryption: int = helper.get_index(
            get_resources(graph, bucket, 'BucketEncryption', depth=4), 0)

        if not _encryption:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=(f'AWS::S3::Bucket/'
                            f'BucketEncryption/'),
                    identifier=resource['name'],
                    line=resource['line'],
                    reason='has encryption disabled.'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='S3 buckets have encryption disabled',
        msg_closed='S3 Buckets have encryption enabled')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def allows_unauthorized_public_access(path: str,
                                      exclude: Optional[List[str]] =
                                      None) -> tuple:
    """
    Check if S3 buckets allow unauthorized public access via bucket policies.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if policies allow unauthorized public access.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[int] = get_templates(graph, path, exclude)
    bucket_policies: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {'AWS', 'S3', 'BucketPolicy'},
        num_labels=3,
        info=True)
    for bucket_policy, resource, template in bucket_policies:
        stmts = get_list_node_items(graph, bucket_policy, 'Statement', depth=8)
        for stmt in stmts:
            vulnerable: List = has_values(graph, stmt, 'Principal', ['*'],
                                          depth=12)
            if has_values(graph, stmt, 'Effect', 'Allow'):
                vulnerabilities.extend(
                    Vulnerability(
                        path=template['path'],
                        entity=(f'AWS::S3::BucketPolicy/'
                                f'PolicyDocument/Statement/Principal'),
                        identifier=resource['name'],
                        line=graph.nodes.get(vuln)['line'],
                        reason='allows public access.') for vuln in vulnerable)

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='S3 bucket policy allows public access',
        msg_closed='S3 bucket policy allows public access')
