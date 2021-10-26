"""AWS CloudFormation checks for ``CloudFront`` (Content Delivery Network)."""


from fluidasserts import (
    LOW,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_ref_nodes,
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


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_geo_restrictions(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
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
        map(lambda x: x[0], templates),
        {"AWS", "CloudFront", "Distribution"},
        info=True,
    )
    for dist, resource, template in distributions:
        line = resource["line"]
        found_issues: list = []
        restrictions = helper.get_index(
            get_resources(graph, dist, "GeoRestriction", 4), 0
        )
        if restrictions:
            line = graph.nodes[restrictions]["line"]
        rest_type = helper.get_index(
            get_resources(graph, dist, "RestrictionType", 5), 0
        )

        res_value = None
        if rest_type:
            rest_node = helper.get_index(get_ref_nodes(graph, rest_type), 0)
            res_value = graph.nodes[rest_node]["value"]
        if not rest_type or (res_value and res_value == "none"):
            found_issues.append(("GeoRestriction", restrictions))

        for issue in found_issues:
            locations_node = helper.get_index(
                get_resources(graph, issue[1], "Item"), 0
            )
            locations = None
            if locations_node:
                value = helper.get_index(
                    get_ref_nodes(
                        graph, locations_node, lambda x: isinstance(x, str)
                    ),
                    0,
                )
                locations = value["value"] if value else None

            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=(
                        f"AWS::CloudFront::Distribution"
                        f"/DistributionConfig"
                        f"/Restrictions"
                        f"/GeoRestriction/"
                        f"{locations}"
                    ),
                    identifier=resource["name"],
                    line=line,
                    reason="has no GeoRestriction",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="Distributions have no geo restrictions",
        msg_closed="Distributions have geo restrictions",
    )
