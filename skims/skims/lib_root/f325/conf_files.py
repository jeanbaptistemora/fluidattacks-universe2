from collections.abc import (
    Iterator,
)
from lib_root.utilities.json import (
    get_attribute,
    is_parent,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def is_in_path(graph: Graph, nid: NId) -> Iterator[NId]:
    correct_parents = ["Statement"]
    effect, effect_val, _ = get_attribute(graph, nid, "Effect")
    principal, principa_val, principal_id = get_attribute(
        graph, nid, "Principal"
    )
    if (
        effect
        and principal
        and principa_val == "*"
        and effect_val == "Allow"
        and is_parent(graph, principal_id, correct_parents)
    ):
        yield principal_id


def principal_wildcard(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JSON_PRINCIPAL_WILDCARD

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JSON):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="Object"):
                for report in is_in_path(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f325.json_principal_wildcard",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
