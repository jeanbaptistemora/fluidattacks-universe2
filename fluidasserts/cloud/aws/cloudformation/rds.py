"""
AWS CloudFormation checks for ``RDS`` (Relational Database Service).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""

# Standard imports
import contextlib
from typing import List, Optional, Tuple, Dict

# Treed imports
from networkx import DiGraph
from networkx.algorithms import dfs_preorder_nodes

# Local imports
from fluidasserts import SAST, LOW, MEDIUM
from fluidasserts.helper.aws import CloudFormationInvalidTypeError
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    get_templates,
    get_graph,
    get_predecessor,
    get_ref_nodes,
    get_type,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unencrypted_storage(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``DBCluster`` or ``DBInstance`` use unencrypted storage.

    The following checks are performed:

    * F26 RDS DBCluster should have StorageEncrypted enabled
    * F27 RDS DBInstance should have StorageEncrypted enabled

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **StorageEncrypted** attribute is set to **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    clusters: List[int] = [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if len(graph.nodes[node]['labels'].intersection(
            {'AWS', 'RDS', 'DBCluster', 'DBInstance'})) > 2
    ]
    vulnerable: bool = False
    vulnerabilities: List[Vulnerability] = []
    for cluster in clusters:
        template: Dict = graph.nodes[get_predecessor(graph, cluster,
                                                     'CloudFormationTemplate')]
        resource: Dict = graph.nodes[cluster]
        _encryption: List[int] = [
            node for node in dfs_preorder_nodes(graph, cluster, 3)
            if 'StorageEncrypted' in graph.nodes[node]['labels']
        ]

        if _encryption:
            encryption: int = _encryption[0]
            with contextlib.suppress(CloudFormationInvalidTypeError):
                un_encryption: List[int] = get_ref_nodes(
                    graph, encryption,
                    lambda x: x not in (True, 'true', 'True', '1', 1))
                if un_encryption:
                    vulnerable = True
        else:
            vulnerable = True
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=get_type(graph, encryption, {'DBCluster',
                                                        'DBInstance'}),
                    identifier=resource['name'],
                    line=graph.nodes[un_encryption[0]]['line'],
                    reason='is not encrypted'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS clusters are not encrypted',
        msg_closed='RDS clusters are encrypted')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_automated_backups(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``DBCluster`` or ``DBInstance`` have not automated backups.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **BackupRetentionPeriod** attribute is set to 0.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    clusters: List[int] = [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if len(graph.nodes[node]['labels'].intersection(
            {'AWS', 'RDS', 'DBCluster', 'DBInstance'})) > 2
    ]
    vulnerable: bool = False
    vulnerabilities: List[Vulnerability] = []
    for cluster in clusters:
        template: Dict = graph.nodes[get_predecessor(graph, cluster,
                                                     'CloudFormationTemplate')]
        resource: Dict = graph.nodes[cluster]
        _retention: List[int] = [
            node for node in dfs_preorder_nodes(graph, cluster, 3)
            if 'BackupRetentionPeriod' in graph.nodes[node]['labels']
        ]

        if _retention:
            retention: int = _retention[0]
            with contextlib.suppress(CloudFormationInvalidTypeError):
                no_retention: List[int] = get_ref_nodes(
                    graph, retention,
                    lambda x: x in ('0', 0))
                if no_retention:
                    vulnerable = True
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=get_type(graph, retention, {'DBCluster',
                                                       'DBInstance'}),
                    identifier=resource['name'],
                    line=graph.nodes[no_retention[0]]['line'],
                    reason='has not automated backups enabled'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS cluster or instances have not automated backups enabled',
        msg_closed='RDS cluster or instances have automated backups enabled')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_publicly_accessible(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if any ``RDS::DBInstance`` is Internet facing (a.k.a. public).

    The following checks are performed:

    * F22 RDS instance should not be publicly accessible

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **PubliclyAccessible** attribute is set to
                **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    clusters: List[int] = [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if len(graph.nodes[node]['labels'].intersection(
            {'AWS', 'RDS', 'DBInstance'})) > 2
    ]
    vulnerable: bool = False
    vulnerabilities: List[Vulnerability] = []
    for cluster in clusters:
        template: Dict = graph.nodes[get_predecessor(graph, cluster,
                                                     'CloudFormationTemplate')]
        resource: Dict = graph.nodes[cluster]
        _public: List[int] = [
            node for node in dfs_preorder_nodes(graph, cluster, 3)
            if 'PubliclyAccessible' in graph.nodes[node]['labels']
        ]

        if _public:
            public: int = _public[0]
            with contextlib.suppress(CloudFormationInvalidTypeError):
                is_public: List[int] = get_ref_nodes(
                    graph, public,
                    lambda x: x in (True, 'true', 'True', '1', 1))
                if is_public:
                    vulnerable = True
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=get_type(graph, public, {'DBInstance'}),
                    identifier=resource['name'],
                    line=graph.nodes[is_public[0]]['line'],
                    reason='is publicly accessible'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS instances are publicly accessible',
        msg_closed='RDS instances are not publicly accessible')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_not_inside_a_db_subnet_group(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``DBInstance`` or ``DBCluster`` are not inside a DB Subnet Group.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **DBSubnetGroupName** attribute is not set.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """

    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    clusters: List[int] = [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if len(graph.nodes[node]['labels'].intersection(
            {'AWS', 'RDS', 'DBCluster', 'DBInstance'})) > 2
    ]
    vulnerabilities: List[Vulnerability] = []
    for cluster in clusters:
        template: Dict = graph.nodes[get_predecessor(graph, cluster,
                                                     'CloudFormationTemplate')]
        resource: Dict = graph.nodes[cluster]
        _subnet: List[int] = [
            node for node in dfs_preorder_nodes(graph, cluster, 3)
            if 'DBSubnetGroupName' in graph.nodes[node]['labels']
        ]

        if not _subnet:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=get_type(graph, cluster, {'DBCluster',
                                                     'DBInstance'}),
                    identifier=resource['name'],
                    line=resource['line'],
                    reason='is not inside a DB Subnet Group'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS Cluster or Instances are not inside a DB Subnet Group',
        msg_closed='RDS Cluster or Instances are inside a DB Subnet Group')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_termination_protection(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``RDS`` clusters and instances have termination protection.

    By default RDS Clusters and Instances can be terminated using the
    Amazon EC2 console, CLI, or API.

    This is not desirable if the termination is done unintentionally
    because DB Snapshots and Automated Backups are deleted
    automatically after some time (or immediately in some cases)
    which make cause data lost and service interruption.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance or cluster have not the
                **DeletionProtection** parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """

    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    clusters: List[int] = [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if len(graph.nodes[node]['labels'].intersection(
            {'AWS', 'RDS', 'DBCluster', 'DBInstance'})) > 2
    ]
    vulnerable: bool = False
    vulnerabilities: List[Vulnerability] = []
    for cluster in clusters:
        template: Dict = graph.nodes[get_predecessor(graph, cluster,
                                                     'CloudFormationTemplate')]
        resource: Dict = graph.nodes[cluster]
        _termination_protection: List[int] = [
            node for node in dfs_preorder_nodes(graph, cluster, 3)
            if 'DeletionProtection' in graph.nodes[node]['labels']
        ]

        if _termination_protection:
            termination_protection: int = _termination_protection[0]
            with contextlib.suppress(CloudFormationInvalidTypeError):
                no_protection: List[int] = get_ref_nodes(
                    graph, termination_protection,
                    lambda x: x not in (True, 'true', 'True', '1', 1))
                if no_protection:
                    vulnerable = True
        else:
            vulnerable = True
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=get_type(graph, cluster,
                                    {'DBCluster',
                                     'DBInstance'}),
                    identifier=resource['name'],
                    line=resource['line'],
                    reason='has not deletion protection'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS instances or clusters have not deletion protection',
        msg_closed='RDS instances or clusters have deletion protection')


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def not_uses_iam_authentication(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``RDS`` clusters and instances have termination protection.

    By default RDS Clusters and Instances can be terminated using the
    Amazon EC2 console, CLI, or API.

    This is not desirable if the termination is done unintentionally
    because DB Snapshots and Automated Backups are deleted
    automatically after some time (or immediately in some cases)
    which make cause data lost and service interruption.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if the instance or cluster have not the
                **DeletionProtection** parameter set to **true**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """

    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    clusters: List[int] = [
        node
        for template, _ in templates
        for node in dfs_preorder_nodes(graph, template, 2)
        if len(graph.nodes[node]['labels'].intersection(
            {'AWS', 'RDS', 'DBCluster', 'DBInstance'})) > 2
    ]
    vulnerable: bool = False
    vulnerabilities: List[Vulnerability] = []
    for cluster in clusters:
        template: Dict = graph.nodes[get_predecessor(graph, cluster,
                                                     'CloudFormationTemplate')]
        resource: Dict = graph.nodes[cluster]
        _iam_authentication: List[int] = [
            node for node in dfs_preorder_nodes(graph, cluster, 3)
            if 'EnableIAMDatabaseAuthentication' in graph.nodes[node]['labels']
        ]

        if _iam_authentication:
            iam_authentication: int = _iam_authentication[0]
            with contextlib.suppress(CloudFormationInvalidTypeError):
                no_protection: List[int] = get_ref_nodes(
                    graph, iam_authentication,
                    lambda x: x not in (True, 'true', 'True', '1', 1))
                if no_protection:
                    vulnerable = True
        else:
            vulnerable = True
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity=get_type(graph, cluster,
                                    {'DBCluster',
                                     'DBInstance'}),
                    identifier=resource['name'],
                    line=resource['line'],
                    reason='does not have IAM authentication'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS instances or clusters do not use IAM authentication',
        msg_closed='RDS instances or clusters use IAM authentication')
