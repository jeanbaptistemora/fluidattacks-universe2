from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from typing import (
    Tuple,
)
from utils import (
    graph as g,
)


def java_switch_without_default(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            for syntax_steps in shard.syntax.values():
                for index, syntax_step in enumerate(syntax_steps):
                    if isinstance(syntax_step, graph_model.SyntaxStepSwitch):
                        cases = get_dependencies(index, syntax_steps)[1:]
                        has_default = any(
                            isinstance(
                                case, graph_model.SyntaxStepSwitchLabelDefault
                            )
                            for case in cases
                        )
                        if not has_default:
                            yield shard, syntax_step.meta.n_id

    return get_vulnerabilities_from_n_ids(
        cwe=("478",),
        desc_key="src.lib_path.f073.switch_no_default",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def javascript_switch_without_default(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in [
            *graph_db.shards_by_language(
                graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            ),
            *graph_db.shards_by_language(
                graph_model.GraphShardMetadataLanguage.TSX,
            ),
        ]:
            for switch_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="switch_statement"),
            ):
                if not g.filter_nodes(
                    shard.graph,
                    nodes=g.adj_ast(shard.graph, switch_id, depth=2),
                    predicate=g.pred_has_labels(label_type="switch_default"),
                ):
                    yield shard, switch_id

    return get_vulnerabilities_from_n_ids(
        cwe=("478",),
        desc_key="src.lib_path.f073.switch_no_default",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def c_sharp_switch_without_default(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for switch_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="switch_statement"),
            ):
                if not g.filter_nodes(
                    shard.graph,
                    nodes=g.adj_cfg(shard.graph, switch_id, depth=1),
                    predicate=g.pred_has_labels(
                        label_type="default_switch_label"
                    ),
                ):
                    yield shard, switch_id

    return get_vulnerabilities_from_n_ids(
        cwe=("478",),
        desc_key="src.lib_path.f073.switch_no_default",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def go_switch_without_default(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        def _predicate(n_id: str) -> bool:
            return g.pred_has_labels(label_type="type_switch_statement")(
                n_id
            ) or g.pred_has_labels(label_type="expression_switch_statement")(
                n_id
            )

        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.GO,
        ):
            for switch_id in g.filter_nodes(
                shard.graph, nodes=shard.graph.nodes, predicate=_predicate
            ):
                if not g.filter_nodes(
                    shard.graph,
                    nodes=g.adj_ast(shard.graph, switch_id, depth=1),
                    predicate=g.pred_has_labels(label_type="default_case"),
                ):
                    yield shard, switch_id

    return get_vulnerabilities_from_n_ids(
        cwe=("478",),
        desc_key="src.lib_path.f073.switch_no_default",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def kotlin_when_without_else(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.KOTLIN
        ):
            for when_id in g.filter_nodes(
                shard.graph,
                shard.graph.nodes,
                g.pred_has_labels(label_type="when_expression"),
            ):
                cases_ids = g.get_ast_childs(
                    shard.graph, when_id, "when_entry"
                )
                else_id: Tuple[str, ...] = tuple(
                    case_id
                    for case_id in cases_ids
                    if shard.graph.nodes[
                        str(
                            shard.graph.nodes[case_id][
                                "label_field_conditions"
                            ]
                        )
                    ]["label_type"]
                    == "when_entry_else"
                )
                empty_else: bool = False
                if else_id:
                    else_body = g.adj_ast(
                        shard.graph,
                        str(shard.graph.nodes[else_id[0]]["label_field_body"]),
                    )
                    empty_else = all(
                        shard.graph.nodes[n_id]["label_type"]
                        in {"{", "}", "comment"}
                        for n_id in else_body
                    )
                if not else_id or empty_else:
                    yield shard, when_id

    return get_vulnerabilities_from_n_ids(
        cwe=("478",),
        desc_key="src.lib_path.f073.when_no_else",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F073
QUERIES: graph_model.Queries = (
    (FINDING, java_switch_without_default),
    (FINDING, javascript_switch_without_default),
    (FINDING, c_sharp_switch_without_default),
    (FINDING, go_switch_without_default),
    (FINDING, kotlin_when_without_else),
)
