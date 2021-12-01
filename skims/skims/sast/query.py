import inspect
from itertools import (
    chain,
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
from types import (
    FrameType,
)
from typing import (
    cast,
    Dict,
    Iterator,
    Optional,
    Set,
    Tuple,
)
from utils.ctx import (
    CTX,
)
from utils.string import (
    make_snippet,
    SnippetViewport,
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
    source_method: str,
) -> core_model.Vulnerability:
    # Root -> meta -> file graph
    meta_attrs_label_path = graph_shard.path

    n_attrs: graph_model.NAttrs = graph_shard.graph.nodes[n_id]
    n_attrs_label_column = n_attrs["label_c"]
    n_attrs_label_line = n_attrs["label_l"]

    with open(
        file=os.path.join(CTX.config.working_dir, meta_attrs_label_path),
        encoding="latin-1",
    ) as handle:
        content: str = handle.read()

    return core_model.Vulnerability(
        finding=finding,
        kind=core_model.VulnerabilityKindEnum.LINES,
        namespace=CTX.config.namespace,
        state=core_model.VulnerabilityStateEnum.OPEN,
        what=meta_attrs_label_path,
        where=str(n_attrs_label_line),
        skims_metadata=core_model.SkimsVulnerabilityMetadata(
            cwe=cwe,
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
            ),
            source_method=source_method,
        ),
    )


def get_vulnerabilities_from_n_ids(
    *,
    cwe: Tuple[str, ...],
    desc_key: str,
    desc_params: Dict[str, str],
    finding: core_model.FindingEnum,
    graph_shard_nodes: graph_model.GraphShardNodes,
) -> core_model.Vulnerabilities:
    source_method = cast(
        FrameType, cast(FrameType, inspect.currentframe()).f_back
    ).f_code.co_name
    return tuple(
        get_vulnerability_from_n_id(
            cwe=cwe,
            desc_key=desc_key,
            desc_params=desc_params,
            finding=finding,
            graph_shard=graph_shard,
            n_id=n_id,
            source_method=source_method,
        )
        for graph_shard, n_id in graph_shard_nodes
    )


def _is_vulnerable(
    finding: core_model.FindingEnum,
    syntax_step: graph_model.SyntaxStep,
    syntax_step_n_attrs: graph_model.NAttrs,
) -> bool:
    sinks: Set[str] = syntax_step_n_attrs.get("label_sink_type", {})

    return syntax_step.meta.danger is True and finding.name in sinks


def get_vulnerabilities_from_syntax(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    possible_syntax_steps: graph_model.SyntaxSteps,
) -> core_model.Vulnerabilities:
    params = graph_model.GRAPH_VULNERABILITY_PARAMETERS[finding]
    return get_vulnerabilities_from_n_ids(
        cwe=params.cwe,
        desc_key=params.desc_key,
        desc_params=params.desc_params,
        finding=finding,
        graph_shard_nodes=[
            (graph_shard, syntax_step.meta.n_id)
            for graph_shard in [
                graph_db.shards[graph_db.shards_by_path[shard.path]],
            ]
            for syntax_step in possible_syntax_steps
            if _is_vulnerable(
                finding,
                syntax_step,
                graph_shard.graph.nodes[syntax_step.meta.n_id],
            )
        ],
    )


def shard_n_id_query_lazy(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    syntax_steps_n_id: PossibleSyntaxStepsForUntrustedNId,
) -> Iterator[core_model.Vulnerabilities]:
    for steps in syntax_steps_n_id.values():
        yield get_vulnerabilities_from_syntax(graph_db, finding, shard, steps)


def shard_query_lazy(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    possible_steps_finding: Optional[PossibleSyntaxStepsForFinding] = None,
) -> Iterator[core_model.Vulnerabilities]:

    if possible_steps_finding is None:
        possible_steps_finding = get_possible_syntax_steps_for_finding(
            graph_db, finding, shard
        )

    for steps_n_id in possible_steps_finding.values():
        yield from shard_n_id_query_lazy(graph_db, finding, shard, steps_n_id)


def shard_n_id_query(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    n_id: str,
) -> core_model.Vulnerabilities:
    steps = get_possible_syntax_steps_for_n_id(
        graph_db,
        finding=finding,
        n_id=n_id,
        shard=shard,
        only_sinks=True,
    )
    return tuple(
        chain.from_iterable(
            shard_n_id_query_lazy(graph_db, finding, shard, steps)
        )
    )


def shard_query(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
) -> core_model.Vulnerabilities:
    return tuple(
        chain.from_iterable(shard_query_lazy(graph_db, finding, shard))
    )


def query_lazy(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> Iterator[core_model.Vulnerabilities]:
    if CTX.debug:
        all_possible_steps = get_all_possible_syntax_steps(graph_db, finding)

    for shard in graph_db.shards:
        yield from shard_query_lazy(
            graph_db,
            finding,
            shard,
            all_possible_steps[shard.path] if CTX.debug else None,
        )


def query(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> core_model.Vulnerabilities:
    return tuple(chain.from_iterable(query_lazy(graph_db, finding)))


def query_f001_java_sql(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F112)


def query_f001_c_sharp_sql(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F001)


def query_f004(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F004)


def query_f008(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F008)


def query_f021(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F021)


def query_f034(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F034)


def query_f042(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F042)


def query_f052(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F052)


def query_f063_pt(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F063)


def query_f063_tb(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F089)


def query_f100(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F100)


def query_f107(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F107)


def query_f127_tc(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F127)


def query_f320(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, core_model.FindingEnum.F320)


QUERIES: graph_model.Queries = (
    (core_model.FindingEnum.F112, query_f001_java_sql),
    (core_model.FindingEnum.F001, query_f001_c_sharp_sql),
    (core_model.FindingEnum.F004, query_f004),
    (core_model.FindingEnum.F008, query_f008),
    (core_model.FindingEnum.F021, query_f021),
    (core_model.FindingEnum.F034, query_f034),
    (core_model.FindingEnum.F042, query_f042),
    (core_model.FindingEnum.F052, query_f052),
    (core_model.FindingEnum.F063, query_f063_pt),
    (core_model.FindingEnum.F089, query_f063_tb),
    (core_model.FindingEnum.F100, query_f100),
    (core_model.FindingEnum.F107, query_f107),
    (core_model.FindingEnum.F127, query_f127_tc),
    (core_model.FindingEnum.F320, query_f320),
)
