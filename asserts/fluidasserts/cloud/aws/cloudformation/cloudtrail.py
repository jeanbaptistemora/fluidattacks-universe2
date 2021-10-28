"""AWS CloudFormation checks for ``S3`` (Simple Storage Service)."""


from fluidasserts import (
    LOW,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_resources,
    get_templates,
    has_values,
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
    List,
    Optional,
)


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def trails_not_multiregion(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if any ``CloudTrail Trails`` have **MultiRegion** enabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **MultiRegion** attribute is not
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
        {"AWS", "CloudTrail", "Trail"},
        num_labels=3,
        info=True,
    )
    for trail, resource, template in buckets:
        _multiregion: int = helper.get_index(
            has_values(
                graph,
                trail,
                "IsMultiRegionTrail",
                ["true", "True", True, "1", 1],
                depth=4,
            ),
            0,
        )

        if not _multiregion:
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=(f"AWS::CloudTrail::Trail/" f"IsMultiRegionTrail/"),
                    identifier=resource["name"],
                    line=resource["line"],
                    reason="is not enabled.",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="Trail has multiregion disabled",
        msg_closed="Trail has multiregion enabled",
    )
