from ctx import (
    CTX,
)
from itertools import (
    chain,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
import os
from sast_symbolic_evaluation.evaluate import (
    get_all_possible_syntax_steps,
    get_possible_syntax_steps_for_finding,
    get_possible_syntax_steps_for_n_id,
    PossibleSyntaxStepsForFinding,
    PossibleSyntaxStepsForUntrustedNId,
)
from serializers import (
    make_snippet,
    SnippetViewport,
)
from typing import (
    Any,
    Dict,
    Iterator,
    Optional,
    Set,
)
from vulnerabilities import (
    build_lines_vuln,
    build_metadata,
)
from zone import (
    t,
)


def get_vulnerability_from_n_id(
    *,
    desc_key: str,
    desc_params: Dict[str, str],
    graph_shard: graph_model.GraphShard,
    n_id: str,
    method: core_model.MethodsEnum,
    metadata: Optional[Dict[str, Any]] = None,
) -> core_model.Vulnerability:
    # Root -> meta -> file graph
    what_data = meta_attrs_label_path = graph_shard.path

    n_attrs: graph_model.NAttrs = graph_shard.graph.nodes[n_id]
    n_attrs_label_column = n_attrs["label_c"]
    n_attrs_label_line = n_attrs["label_l"]

    with open(
        file=os.path.join(CTX.config.working_dir, meta_attrs_label_path),
        encoding="latin-1",
    ) as handle:
        content: str = handle.read()

    if metadata:
        what_data = (
            f"{meta_attrs_label_path} ({meta_what})"
            if (meta_what := metadata.get("what"))
            else what_data
        )
        desc_params = (
            meta_desc_params
            if (meta_desc_params := metadata.get("desc_params"))
            else desc_params
        )

    return build_lines_vuln(
        method=method,
        what=what_data,
        where=str(n_attrs_label_line),
        metadata=build_metadata(
            method=method,
            description=(
                f"{t(key=desc_key, **desc_params)} {t(key='words.in')} "
                f"{CTX.config.namespace}/{meta_attrs_label_path}"
            ),
            snippet=make_snippet(
                content=content,
                viewport=SnippetViewport(
                    column=int(n_attrs_label_column),
                    line=int(n_attrs_label_line),
                ),
            ).content,
        ),
    )


def get_vulnerabilities_from_n_ids_metadata(
    *,
    desc_key: str,
    desc_params: Dict[str, str],
    graph_shard_nodes: graph_model.MetadataGraphShardNodes,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:

    return tuple(
        get_vulnerability_from_n_id(
            desc_key=desc_key,
            desc_params=desc_params,
            graph_shard=graph_shard,
            n_id=n_id,
            method=method,
            metadata=metadata,
        )
        for graph_shard, n_id, metadata in graph_shard_nodes
    )


def get_vulnerabilities_from_n_ids(
    *,
    desc_key: str,
    desc_params: Dict[str, str],
    graph_shard_nodes: graph_model.GraphShardNodes,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    return tuple(
        get_vulnerability_from_n_id(
            desc_key=desc_key,
            desc_params=desc_params,
            graph_shard=graph_shard,
            n_id=n_id,
            method=method,
        )
        for graph_shard, n_id in graph_shard_nodes
    )


def _is_vulnerable(
    finding: core_model.FindingEnum,
    syntax_step: graph_model.SyntaxStep,
    syntax_step_n_attrs: graph_model.NAttrs,
) -> bool:
    sinks: Set[str] = set(syntax_step_n_attrs.get("label_sink_type", {}))

    return syntax_step.meta.danger is True and finding.name in sinks


def get_vulnerabilities_from_syntax(
    shard: graph_model.GraphShard,
    possible_syntax_steps: graph_model.SyntaxSteps,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    params = graph_model.GRAPH_VULNERABILITY_PARAMETERS[method.value.finding]
    return get_vulnerabilities_from_n_ids(
        desc_key=params.desc_key,
        desc_params=params.desc_params,
        graph_shard_nodes=[
            (shard, syntax_step.meta.n_id)
            for syntax_step in possible_syntax_steps
            if _is_vulnerable(
                method.value.finding,
                syntax_step,
                shard.graph.nodes[syntax_step.meta.n_id],
            )
        ],
        method=method,
    )


def shard_n_id_query_lazy(
    shard: graph_model.GraphShard,
    syntax_steps_n_id: PossibleSyntaxStepsForUntrustedNId,
    method: core_model.MethodsEnum,
) -> Iterator[core_model.Vulnerabilities]:
    for steps in syntax_steps_n_id.values():
        yield get_vulnerabilities_from_syntax(shard, steps, method)


def shard_query_lazy(
    shard_db: ShardDb,
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    method: core_model.MethodsEnum,
    possible_steps_finding: Optional[PossibleSyntaxStepsForFinding] = None,
) -> Iterator[core_model.Vulnerabilities]:

    if possible_steps_finding is None:
        possible_steps_finding = get_possible_syntax_steps_for_finding(
            shard_db, graph_db, method.value.finding, shard
        )

    for steps_n_id in possible_steps_finding.values():
        yield from shard_n_id_query_lazy(shard, steps_n_id, method)


def shard_n_id_query(
    shard_db: ShardDb,
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    n_id: str,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    steps = get_possible_syntax_steps_for_n_id(
        shard_db,
        graph_db,
        finding=method.value.finding,
        n_id=n_id,
        shard=shard,
        only_sinks=True,
    )
    return tuple(
        chain.from_iterable(shard_n_id_query_lazy(shard, steps, method))
    )


def shard_query(
    shard_db: ShardDb,
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    return tuple(
        chain.from_iterable(
            shard_query_lazy(shard_db, graph_db, shard, method)
        )
    )


def query_lazy(
    shard_db: ShardDb,
    graph_db: graph_model.GraphDB,
    method: core_model.MethodsEnum,
) -> Iterator[core_model.Vulnerabilities]:
    if CTX.debug:
        all_possible_steps = get_all_possible_syntax_steps(
            shard_db, graph_db, method.value.finding
        )

    for shard in graph_db.shards:
        yield from shard_query_lazy(
            shard_db,
            graph_db,
            shard,
            method,
            all_possible_steps[shard.path] if CTX.debug else None,
        )


def query(
    shard_db: ShardDb,
    graph_db: graph_model.GraphDB,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    return tuple(chain.from_iterable(query_lazy(shard_db, graph_db, method)))
