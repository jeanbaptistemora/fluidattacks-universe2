# Standard library
from itertools import (
    chain,
)
import os
from typing import (
    Dict,
    Iterator,
    Tuple,
)

# Local libraries
from model import (
    core_model,
    graph_model,
)
from sast.symeval import (
    get_possible_syntax_steps,
)
from utils.ctx import (
    CTX,
)
from utils.encodings import (
    serialize_namespace_into_vuln,
)
from utils.string import (
    to_snippet_blocking,
)
from zone import (
    t,
)


def get_vulnerability_from_n_id(
    *,
    cwe: Tuple[str, ...],
    desc_key: str,
    desc_params: Dict[str, str],
    finding: core_model.FindingEnum,
    graph_shard: graph_model.GraphShard,
    n_id: str,
) -> core_model.Vulnerability:
    # Root -> meta -> file graph
    meta_attrs_label_path = graph_shard.path

    n_attrs: graph_model.NAttrs = graph_shard.graph.nodes[n_id]
    n_attrs_label_column = n_attrs['label_c']
    n_attrs_label_line = n_attrs['label_l']

    with open(
        file=os.path.join(CTX.config.working_dir, meta_attrs_label_path),
        encoding='latin-1',
    ) as handle:
        content: str = handle.read()

    return core_model.Vulnerability(
        finding=finding,
        kind=core_model.VulnerabilityKindEnum.LINES,
        state=core_model.VulnerabilityStateEnum.OPEN,
        what=serialize_namespace_into_vuln(
            kind=core_model.VulnerabilityKindEnum.LINES,
            namespace=CTX.config.namespace,
            what=meta_attrs_label_path,
        ),
        where=n_attrs_label_line,
        skims_metadata=core_model.SkimsVulnerabilityMetadata(
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
    *,
    cwe: Tuple[str, ...],
    desc_key: str,
    desc_params: Dict[str, str],
    finding: core_model.FindingEnum,
    graph_shard_nodes: graph_model.GraphShardNodes,
) -> core_model.Vulnerabilities:
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


def query_lazy(
    graph_db: graph_model.GraphDB,
) -> Iterator[core_model.Vulnerabilities]:
    for possible_syntax_steps_for_shard_path in (
        get_possible_syntax_steps(graph_db).values()
    ):
        for finding_str, possible_syntax_steps_for_finding in (
            possible_syntax_steps_for_shard_path.items()
        ):
            for possible_syntax_steps_for_untrusted_n_id in (
                possible_syntax_steps_for_finding.values()
            ):
                for _ in (
                    possible_syntax_steps_for_untrusted_n_id.values()
                ):
                    fin = core_model.FINDING_ENUM_FROM_STR[finding_str]
                    params = graph_model.GRAPH_VULNERABILITY_PARAMETERS[fin]

                    yield get_vulnerabilities_from_n_ids(
                        cwe=params.cwe,
                        desc_key=params.desc_key,
                        desc_params=params.desc_params,
                        finding=fin,
                        graph_shard_nodes=iter([]),  # Pending to implement
                    )


def query(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return tuple(chain.from_iterable(query_lazy(graph_db)))
