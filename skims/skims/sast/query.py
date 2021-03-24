# Standard library
from itertools import (
    chain,
)
import os
from typing import (
    Dict,
    Iterator,
    Set,
    Tuple,
)

# Local libraries
from model import (
    core_model,
    graph_model,
)
from sast.symeval import (
    get_possible_syntax_steps_linear,
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
        where=str(n_attrs_label_line),
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


def _is_vulnerable(
    finding: core_model.FindingEnum,
    syntax_step: graph_model.SyntaxStep,
    syntax_step_n_attrs: graph_model.NAttrs,
    untrusted_n_attrs: graph_model.NAttrs,
) -> bool:
    sinks: Set[str] = \
        set(syntax_step_n_attrs.get('label_sink_type', '').split(','))

    return syntax_step.meta.danger is True and (
        (untrusted_n_attrs['label_input_type'] in sinks) or
        (
            finding.name in sinks and
            bool(sinks.intersection(core_model.ALLOW_UNTRUSTED_NODES_STR)) and
            core_model.UNTRUSTED_NODE == untrusted_n_attrs['label_input_type']
        )
    )


def query_lazy(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> Iterator[core_model.Vulnerabilities]:
    for syntax_steps in get_possible_syntax_steps_linear(
        graph_db,
        finding,
    ):
        params = graph_model.GRAPH_VULNERABILITY_PARAMETERS[finding]

        yield get_vulnerabilities_from_n_ids(
            cwe=params.cwe,
            desc_key=params.desc_key,
            desc_params=params.desc_params,
            finding=finding,
            graph_shard_nodes=[
                (graph_shard, syntax_step.meta.n_id)
                for graph_shard in [
                    graph_db.shards[
                        graph_db.shards_by_path[syntax_steps.shard_path]
                    ],
                ]
                for syntax_step in syntax_steps.syntax_steps
                if _is_vulnerable(
                    finding,
                    syntax_step,
                    graph_shard.graph.nodes[syntax_step.meta.n_id],
                    graph_shard.graph.nodes[syntax_steps.untrusted_n_id],
                )
            ],
        )


def query(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> core_model.Vulnerabilities:
    return tuple(chain.from_iterable(query_lazy(graph_db, finding)))


def query_f004(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F004)


def query_f034(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F034)


def query_f042(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F042)


def query_f063_pt(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F063_PATH_TRAVERSAL)


def query_f073(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F073)


QUERIES: graph_model.Queries = (
    query_f004,
    query_f034,
    query_f042,
    query_f063_pt,
    query_f073,
)
