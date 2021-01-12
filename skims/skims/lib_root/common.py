# Standard library
import os
from typing import (
    Set,
)

# Local libraries
from utils import (
    graph as g,
)
from utils.ctx import (
    CTX,
)
from utils.encodings import (
    serialize_namespace_into_vuln,
)
from utils.graph import (
    NAttrs,
)
from utils.model import (
    FindingEnum,
    Graph,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    to_snippet_blocking,
)
from zone import (
    t,
)


def get_vulnerability_from_n_id(
    *,
    cwe: Set[str],
    desc_key: str,
    finding: FindingEnum,
    graph: Graph,
    n_id: str,
) -> Vulnerability:
    # Root -> meta -> file graph
    meta_id = g.pred(graph, n_id, depth=-1)[1]
    meta_attrs = graph.nodes[meta_id]
    meta_attrs_label_path = meta_attrs['label_path']

    n_attrs: NAttrs = graph.nodes[n_id]
    n_attrs_label_column = n_attrs['label_c']
    n_attrs_label_line = n_attrs['label_l']

    with open(
        file=os.path.join(CTX.config.working_dir, meta_attrs_label_path),
        encoding='latin-1',
    ) as handle:
        content: str = handle.read()

    return Vulnerability(
        finding=finding,
        kind=VulnerabilityKindEnum.LINES,
        state=VulnerabilityStateEnum.OPEN,
        what=serialize_namespace_into_vuln(
            kind=VulnerabilityKindEnum.LINES,
            namespace=CTX.config.namespace,
            what=meta_attrs_label_path,
        ),
        where=n_attrs_label_line,
        skims_metadata=SkimsVulnerabilityMetadata(
            cwe=tuple(cwe),
            description=t(
                key=desc_key,
                path=meta_attrs_label_path,
            ),
            snippet=to_snippet_blocking(
                column=int(n_attrs_label_column),
                content=content,
                line=int(n_attrs_label_line),
            )
        )
    )
