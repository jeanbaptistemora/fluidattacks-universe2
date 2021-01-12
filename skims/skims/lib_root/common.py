# Standard library
import os
from typing import (
    Dict,
    Iterable,
    Tuple,
)

# Local libraries
from utils.ctx import (
    CTX,
)
from utils.encodings import (
    serialize_namespace_into_vuln,
)
from utils.graph import (
    NAttrs,
    NId,
)
from utils.model import (
    FindingEnum,
    GraphShard,
    SkimsVulnerabilityMetadata,
    Vulnerabilities,
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

# Constants
GraphShardNode = Tuple[GraphShard, NId]
GraphShardNodes = Iterable[GraphShardNode]


def get_vulnerability_from_n_id(
    *,
    cwe: Tuple[str, ...],
    desc_key: str,
    desc_params: Dict[str, str],
    finding: FindingEnum,
    graph_shard: GraphShard,
    n_id: str,
) -> Vulnerability:
    # Root -> meta -> file graph
    meta_attrs_label_path = graph_shard.path

    n_attrs: NAttrs = graph_shard.graph.nodes[n_id]
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
            cwe=cwe,
            description=t(
                key=desc_key,
                path=meta_attrs_label_path,
                **desc_params,
            ),
            snippet=to_snippet_blocking(
                column=int(n_attrs_label_column),
                content=content,
                line=int(n_attrs_label_line),
            )
        )
    )


def get_vulnerabilities_from_n_ids(
    cwe: Tuple[str, ...],
    desc_key: str,
    desc_params: Dict[str, str],
    finding: FindingEnum,
    graph_shard_nodes: GraphShardNodes,
) -> Vulnerabilities:
    return tuple(
        get_vulnerability_from_n_id(
            cwe=cwe,
            desc_key=desc_key,
            desc_params=desc_params,
            finding=finding,
            graph_shard=graph_shard,
            n_id=n_id,
        )
        for graph_shard, n_id in graph_shard_nodes
    )
