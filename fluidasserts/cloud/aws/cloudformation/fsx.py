"""AWS CloudFormation checks for ``FSx`` (Amazon FSx file systems)."""

# Standard imports
from typing import List, Optional, Tuple, Dict

# Treed imports
from networkx import DiGraph

# Local imports
from fluidasserts import SAST, MEDIUM
from fluidasserts.cloud.aws.cloudformation import (
    Vulnerability,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.aws.cloudformation import get_templates
from fluidasserts.cloud.aws.cloudformation import get_graph
from fluidasserts.cloud.aws.cloudformation import get_resources


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unencrypted_volumes(
        path: str, exclude: Optional[List[str]] = None) -> tuple:
    """
    Check if ``FileSystem`` entities are encrypted with a **KmsKeyId**.

    :param path: Location of CloudFormation's template file.
    :param exclude: Paths that contains any string from this list are ignored.
    :returns: - ``OPEN`` if **KmsKeyId** attribute is not present.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    graph: DiGraph = get_graph(path, exclude)
    templates: List[Tuple[int, Dict]] = get_templates(graph, path, exclude)
    files: List[int] = get_resources(
        graph,
        map(lambda x: x[0], templates), {'AWS', 'FSx', 'FileSystem'},
        info=True)
    for file, resource, template in files:
        is_vulnerable: bool = not bool(get_resources(graph, file, 'KmsKeyId'))
        if is_vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=template['path'],
                    entity='AWS::FSx::FileSystem',
                    identifier=resource['name'],
                    line=resource['line'],
                    reason='volume is not encrypted'))

    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='FSx File Systems are not encrypted',
        msg_closed='FSx File Systems are encrypted')
