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
    developer: core_model.DeveloperEnum,
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
            developer=developer,
        ),
    )


def get_vulnerabilities_from_n_ids(
    *,
    cwe: Tuple[str, ...],
    desc_key: str,
    desc_params: Dict[str, str],
    finding: core_model.FindingEnum,
    graph_shard_nodes: graph_model.GraphShardNodes,
    developer: core_model.DeveloperEnum,
) -> core_model.Vulnerabilities:
    source = cast(
        FrameType, cast(FrameType, inspect.currentframe()).f_back
    ).f_code
    return tuple(
        get_vulnerability_from_n_id(
            cwe=cwe,
            desc_key=desc_key,
            desc_params=desc_params,
            finding=finding,
            graph_shard=graph_shard,
            n_id=n_id,
            source_method=(
                f"{Path(source.co_filename).stem}.{source.co_name}"
            ),
            developer=developer,
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
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    possible_syntax_steps: graph_model.SyntaxSteps,
    developer: core_model.DeveloperEnum,
) -> core_model.Vulnerabilities:
    params = graph_model.GRAPH_VULNERABILITY_PARAMETERS[finding]
    return get_vulnerabilities_from_n_ids(
        cwe=params.cwe,
        desc_key=params.desc_key,
        desc_params=params.desc_params,
        finding=finding,
        graph_shard_nodes=[
            (shard, syntax_step.meta.n_id)
            for syntax_step in possible_syntax_steps
            if _is_vulnerable(
                finding,
                syntax_step,
                shard.graph.nodes[syntax_step.meta.n_id],
            )
        ],
        developer=developer,
    )


def shard_n_id_query_lazy(
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    syntax_steps_n_id: PossibleSyntaxStepsForUntrustedNId,
    developer: core_model.DeveloperEnum,
) -> Iterator[core_model.Vulnerabilities]:
    for steps in syntax_steps_n_id.values():
        yield get_vulnerabilities_from_syntax(finding, shard, steps, developer)


def shard_query_lazy(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    developer: core_model.DeveloperEnum,
    possible_steps_finding: Optional[PossibleSyntaxStepsForFinding] = None,
) -> Iterator[core_model.Vulnerabilities]:

    if possible_steps_finding is None:
        possible_steps_finding = get_possible_syntax_steps_for_finding(
            graph_db, finding, shard
        )

    for steps_n_id in possible_steps_finding.values():
        yield from shard_n_id_query_lazy(finding, shard, steps_n_id, developer)


def shard_n_id_query(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    n_id: str,
    developer: core_model.DeveloperEnum,
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
            shard_n_id_query_lazy(finding, shard, steps, developer)
        )
    )


def shard_query(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    shard: graph_model.GraphShard,
    developer: core_model.DeveloperEnum,
) -> core_model.Vulnerabilities:
    return tuple(
        chain.from_iterable(
            shard_query_lazy(graph_db, finding, shard, developer)
        )
    )


def query_lazy(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    developer: core_model.DeveloperEnum,
) -> Iterator[core_model.Vulnerabilities]:
    if CTX.debug:
        all_possible_steps = get_all_possible_syntax_steps(graph_db, finding)

    for shard in graph_db.shards:
        yield from shard_query_lazy(
            graph_db,
            finding,
            shard,
            developer,
            all_possible_steps[shard.path] if CTX.debug else None,
        )


def analyze_lazy(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> Iterator[core_model.Vulnerabilities]:
    for shard in graph_db.shards:
        if shard.syntax_graph:
            yield symbolic_analyze(shard, finding)


def query(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
    developer: core_model.DeveloperEnum,
) -> core_model.Vulnerabilities:
    return tuple(chain.from_iterable(query_lazy(graph_db, finding, developer)))


def analyze(
    graph_db: graph_model.GraphDB,
    finding: core_model.FindingEnum,
) -> core_model.Vulnerabilities:
    return tuple(chain.from_iterable(analyze_lazy(graph_db, finding)))


def query_f001(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F001, developer)


def query_f004(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F004, developer)


def query_f008(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F008, developer)


def analyze_f008(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return analyze(graph_db, core_model.FindingEnum.F008)


def query_f021(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F021, developer)


def query_f034(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F034, developer)


def query_f042(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F042, developer)


def query_f052(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F052, developer)


def query_f063(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F063, developer)


def query_f089(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F089, developer)


def query_f100(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F100, developer)


def analyze_f100(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    return analyze(graph_db, core_model.FindingEnum.F100)


def query_f107(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F107, developer)


def query_f112(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F112, developer)


def query_f127(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F127, developer)


def query_f320(graph_db: graph_model.GraphDB) -> core_model.Vulnerabilities:
    developer = core_model.DeveloperEnum.DIEGO_RESTREPO
    return query(graph_db, core_model.FindingEnum.F320, developer)


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
