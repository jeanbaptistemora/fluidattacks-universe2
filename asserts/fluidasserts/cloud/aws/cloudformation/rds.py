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
