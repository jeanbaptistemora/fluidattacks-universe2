"""
AWS CloudFormation checks for ``KMS`` (Key Management Service).

Some rules were taken from `CFN_NAG <https://github.com/
stelligent/cfn_nag/blob/master/LICENSE.md>`_
"""


import contextlib
from fluidasserts import (
    MEDIUM,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_resources,
    get_templates,
    Vulnerability,
)
from fluidasserts.helper import (
    aws as helper,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from networkx import (
    DiGraph,
)
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_master_keys_exposed_to_everyone(
    path: str, exclude: Optional[List[str]] = None
) -> Tuple:
    """
    Check if Amazon KMS master keys are exposed to everyone.

    Allowing anonymous access to your AWS KMS keys is considered bad practice
    and can lead to sensitive data leakage.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if any of the referenced rules is not followed.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    keys: List[int] = get_resources(
        graph, map(lambda x: x[0], templates), {"AWS", "KMS", "Key"}, info=True
    )
    for key, resource, template in keys:
        key_policy_node: int = helper.get_index(
            get_resources(graph, key, "KeyPolicy", depth=3), 0
        )
        statements: List[int] = get_resources(
            graph, key_policy_node, "Statement", depth=3
        )
        principals: List[int] = get_resources(
            graph, statements, "Principal", depth=3
        )

        for principal in principals:
            line = graph.nodes[principal]["line"]
            vulnerable: bool = False
            father = list(graph.predecessors(principal))[0]
            condition: int = get_resources(graph, father, "Condition")
            aws_node: int = helper.get_index(
                get_resources(graph, principal, "AWS"), 0
            )

            if aws_node:
                node: int = graph.nodes[aws_node]
                line = node["line"]
                if node["value"] == "*" and not condition:
                    vulnerable = True

            if vulnerable:
                vulnerabilities.append(
                    Vulnerability(
                        path=template["path"],
                        entity=f"AWS::KMS::Key",
                        identifier=resource["name"],
                        line=line,
                        reason=(
                            "AWS KMS master key must not be "
                            "publicly accessible,"
                        ),
                    )
                )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="Amazon KMS master keys are accessible to all users.",
        msg_closed="Amazon KMS master keys are not accessible to all users.",
    )
