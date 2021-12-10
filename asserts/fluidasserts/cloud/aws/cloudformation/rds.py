"""
AWS CloudFormation checks for ``RDS`` (Relational Database Service).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""


import contextlib
from fluidasserts import (
    LOW,
    MEDIUM,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_ref_nodes,
    get_resources,
    get_templates,
    get_type,
    Vulnerability,
)
from fluidasserts.helper.aws import (
    CloudFormationInvalidTypeError,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from networkx import (
    DiGraph,
)
from networkx.algorithms import (
    dfs_preorder_nodes,
)
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_publicly_accessible(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
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
    clusters: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "RDS", "DBCluster", "DBInstance"},
        info=True,
        num_labels=3,
    )
    vulnerable: bool = False
    vulnerabilities: List[Vulnerability] = []
    for cluster, resource, template in clusters:
        line = resource["line"]
        _public: List[int] = [
            node
            for node in dfs_preorder_nodes(graph, cluster, 3)
            if "PubliclyAccessible" in graph.nodes[node]["labels"]
        ]

        if _public:
            public: int = _public[0]
            line = graph.nodes[public]["line"]
            with contextlib.suppress(CloudFormationInvalidTypeError):
                is_public: List[int] = get_ref_nodes(
                    graph,
                    public,
                    lambda x: x in (True, "true", "True", "1", 1),
                )
                if is_public:
                    line = graph.nodes[is_public[0]]["line"]
                    vulnerable = True
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=get_type(graph, public, {"DBInstance"}),
                    identifier=resource["name"],
                    line=line,
                    reason="is publicly accessible",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="RDS instances are publicly accessible",
        msg_closed="RDS instances are not publicly accessible",
    )


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def is_not_inside_a_db_subnet_group(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
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
    clusters: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "RDS", "DBCluster", "DBInstance"},
        info=True,
        num_labels=3,
    )
    vulnerabilities: List[Vulnerability] = []
    for cluster, resource, template in clusters:
        _subnet: List[int] = [
            node
            for node in dfs_preorder_nodes(graph, cluster, 3)
            if "DBSubnetGroupName" in graph.nodes[node]["labels"]
        ]

        if not _subnet:
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=get_type(
                        graph, cluster, {"DBCluster", "DBInstance"}
                    ),
                    identifier=resource["name"],
                    line=resource["line"],
                    reason="is not inside a DB Subnet Group",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="RDS Cluster or Instances are not inside a DB Subnet Group",
        msg_closed="RDS Cluster or Instances are inside a DB Subnet Group",
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_termination_protection(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
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
    clusters: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "RDS", "DBCluster", "DBInstance"},
        info=True,
        num_labels=3,
    )
    vulnerable: bool = False
    vulnerabilities: List[Vulnerability] = []
    for cluster, resource, template in clusters:
        line = resource["line"]
        _termination_protection: List[int] = [
            node
            for node in dfs_preorder_nodes(graph, cluster, 3)
            if "DeletionProtection" in graph.nodes[node]["labels"]
        ]

        if _termination_protection:
            termination_protection: int = _termination_protection[0]
            line = graph.nodes[termination_protection]["line"]
            with contextlib.suppress(CloudFormationInvalidTypeError):
                no_protection: List[int] = get_ref_nodes(
                    graph,
                    termination_protection,
                    lambda x: x not in (True, "true", "True", "1", 1),
                )
                if no_protection:
                    line = graph.nodes[no_protection[0]]["line"]
                    vulnerable = True
        else:
            vulnerable = True
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=get_type(
                        graph, cluster, {"DBCluster", "DBInstance"}
                    ),
                    identifier=resource["name"],
                    line=line,
                    reason="has not deletion protection",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="RDS instances or clusters have not deletion protection",
        msg_closed="RDS instances or clusters have deletion protection",
    )


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def not_uses_iam_authentication(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
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
    clusters: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates),
        {"AWS", "RDS", "DBCluster", "DBInstance"},
        info=True,
        num_labels=3,
    )
    vulnerable: bool = False
    vulnerabilities: List[Vulnerability] = []
    for cluster, resource, template in clusters:
        line = resource["line"]
        _iam_authentication: List[int] = [
            node
            for node in dfs_preorder_nodes(graph, cluster, 3)
            if "EnableIAMDatabaseAuthentication" in graph.nodes[node]["labels"]
        ]

        if _iam_authentication:
            iam_authentication: int = _iam_authentication[0]
            line = graph.nodes[iam_authentication]["line"]
            with contextlib.suppress(CloudFormationInvalidTypeError):
                no_protection: List[int] = get_ref_nodes(
                    graph,
                    iam_authentication,
                    lambda x: x not in (True, "true", "True", "1", 1),
                )
                if no_protection:
                    line = graph.nodes[no_protection[0]]["line"]
                    vulnerable = True
        else:
            vulnerable = True
        if vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=get_type(
                        graph, cluster, {"DBCluster", "DBInstance"}
                    ),
                    identifier=resource["name"],
                    line=line,
                    reason="does not have IAM authentication",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="RDS instances or clusters do not use IAM authentication",
        msg_closed="RDS instances or clusters use IAM authentication",
    )
