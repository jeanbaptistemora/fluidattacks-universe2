from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
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
            for switch_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="switch_statement"),
            ):
                if not g.filter_nodes(
                    shard.graph,
                    nodes=g.adj_ast(shard.graph, switch_id, depth=3),
                    predicate=g.pred_has_labels(label_type="default"),
                ):
                    yield shard, switch_id

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


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F073
QUERIES: graph_model.Queries = (
    (FINDING, java_switch_without_default),
    (FINDING, javascript_switch_without_default),
    (FINDING, c_sharp_switch_without_default),
    (FINDING, go_switch_without_default),
)
