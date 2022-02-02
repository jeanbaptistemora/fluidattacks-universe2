from concurrent.futures.process import (
    ProcessPoolExecutor,
)
from ctx import (
    CTX,
)
from functools import (
    partial,
)
import inspect
from itertools import (
    chain,
)
from model import (
    core_model,
    graph_model,
)
import os
from pathlib import (
    Path,
)
from sast_symbolic_evaluation.evaluate import (
    get_all_possible_syntax_steps,
    get_possible_syntax_steps_for_finding,
    get_possible_syntax_steps_for_n_id,
    PossibleSyntaxStepsForFinding,
    PossibleSyntaxStepsForUntrustedNId,
)
from symbolic_eval.analyze import (
    analyze as symbolic_analyze,
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
    graph_shard: graph_model.GraphShard,
    n_id: str,
    source_method: str,
    method: core_model.MethodsEnum,
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
        finding=method.value.finding,
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
            developer=method.value.developer,
        ),
    )


def get_vulnerabilities_from_n_ids(
    *,
    cwe: Tuple[str, ...],
    desc_key: str,
    desc_params: Dict[str, str],
    graph_shard_nodes: graph_model.GraphShardNodes,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    source = cast(
        FrameType, cast(FrameType, inspect.currentframe()).f_back
    ).f_code
    return tuple(
        get_vulnerability_from_n_id(
            cwe=cwe,
            desc_key=desc_key,
            desc_params=desc_params,
            graph_shard=graph_shard,
            n_id=n_id,
            source_method=(
                f"{Path(source.co_filename).stem}.{source.co_name}"
            ),
            method=method,
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
    shard: graph_model.GraphShard,
    possible_syntax_steps: graph_model.SyntaxSteps,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    params = graph_model.GRAPH_VULNERABILITY_PARAMETERS[method.value.finding]
    return get_vulnerabilities_from_n_ids(
        cwe=params.cwe,
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
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    method: core_model.MethodsEnum,
    possible_steps_finding: Optional[PossibleSyntaxStepsForFinding] = None,
) -> Iterator[core_model.Vulnerabilities]:

    if possible_steps_finding is None:
        possible_steps_finding = get_possible_syntax_steps_for_finding(
            graph_db, method.value.finding, shard
        )

    for steps_n_id in possible_steps_finding.values():
        yield from shard_n_id_query_lazy(shard, steps_n_id, method)


def shard_n_id_query(
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    n_id: str,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    steps = get_possible_syntax_steps_for_n_id(
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
    graph_db: graph_model.GraphDB,
    shard: graph_model.GraphShard,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    return tuple(
        chain.from_iterable(shard_query_lazy(graph_db, shard, method))
    )


def query_lazy(
    graph_db: graph_model.GraphDB,
    method: core_model.MethodsEnum,
) -> Iterator[core_model.Vulnerabilities]:
    if CTX.debug:
        all_possible_steps = get_all_possible_syntax_steps(
            graph_db, method.value.finding
        )

    for shard in graph_db.shards:
        yield from shard_query_lazy(
            graph_db,
            shard,
            method,
            all_possible_steps[shard.path] if CTX.debug else None,
        )


def _partial_symbolic_analyze(function: partial) -> core_model.Vulnerabilities:
    return function()


def analyze_lazy(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> Iterator[core_model.Vulnerabilities]:
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for vulnerabilities in executor.map(
            _partial_symbolic_analyze,
            (
                partial(symbolic_analyze, shard, finding)
                for shard in graph_db.shards
                if shard.syntax_graph
            ),
            chunksize=48,
        ):
            yield vulnerabilities


def query(
    graph_db: graph_model.GraphDB,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    return tuple(chain.from_iterable(query_lazy(graph_db, method)))


def analyze(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> core_model.Vulnerabilities:
    return tuple(chain.from_iterable(analyze_lazy(graph_db, finding)))


def query_f001(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F001)


def query_f004(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F004)


def query_f008(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F008)


def analyze_f008(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return analyze(graph_db, core_model.FindingEnum.F008)


def query_f021(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F021)


def query_f034(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F034)


def query_f042(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F042)


def query_f052(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F052)


def query_f063(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F063)


def query_f089(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F089)


def query_f100(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:

    return query(graph_db, method=core_model.MethodsEnum.QUERY_F100)


def analyze_f100(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return analyze(graph_db, core_model.FindingEnum.F100)


def query_f107(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F107)


def query_f112(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F112)


def query_f127(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F127)


def query_f320(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return query(graph_db, method=core_model.MethodsEnum.QUERY_F320)


QUERIES: graph_model.Queries = (
    (core_model.FindingEnum.F001, query_f001),
    (core_model.FindingEnum.F004, query_f004),
    (core_model.FindingEnum.F008, query_f008),
    (core_model.FindingEnum.F021, query_f021),
    (core_model.FindingEnum.F034, query_f034),
    (core_model.FindingEnum.F042, query_f042),
    (core_model.FindingEnum.F052, query_f052),
    (core_model.FindingEnum.F063, query_f063),
    (core_model.FindingEnum.F089, query_f089),
    (core_model.FindingEnum.F100, query_f100),
    (core_model.FindingEnum.F107, query_f107),
    (core_model.FindingEnum.F112, query_f112),
    (core_model.FindingEnum.F127, query_f127),
    (core_model.FindingEnum.F320, query_f320),
)
