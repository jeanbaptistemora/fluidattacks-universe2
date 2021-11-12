"""AWS CloudFormation checks for ``S3`` (Simple Storage Service)."""


from fluidasserts import (
    LOW,
    MEDIUM,
    SAST,
)
from fluidasserts.cloud.aws.cloudformation import (
    _get_result_as_tuple,
    get_graph,
    get_list_node_items,
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

#: A set of available S3 Access Controls
ACCESS_CONTROLS = {
    "Private",
    "PublicRead",
    "PublicReadWrite",
    "AuthenticatedRead",
    "BucketOwnerRead",
    "BucketOwnerFullControl",
}


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_object_lock_disabled(
    path: str, exclude: Optional[List[str]] = None
) -> tuple:
    """
    Check if any ``S3 Bucket`` has **Object Lock** disabled.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **ObjectLockConfiguration** attribute is not set or
    set to false.
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
        {"AWS", "S3", "Bucket"},
        num_labels=3,
        info=True,
    )
    for bucket, resource, template in buckets:
        if not has_values(
            graph,
            bucket,
            "ObjectLockEnabled",
            ["true", "True", True, "1", 1],
            depth=5,
        ):
            vulnerabilities.append(
                Vulnerability(
                    path=template["path"],
                    entity=(f"AWS::S3::Bucket/" f"ObjectLockEnabled/"),
                    identifier=resource["name"],
                    line=resource["line"],
                    reason="has object lock disabled.",
                )
            )

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open="S3 buckets have object lock disabled",
        msg_closed="S3 Buckets have object lock enabled",
    )
