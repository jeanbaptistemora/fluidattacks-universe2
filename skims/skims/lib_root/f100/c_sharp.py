from collections.abc import (
    Iterator,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)
from utils.string import (
    build_attr_paths,
)


def insec_create(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_INSEC_CREATE
    paths = build_attr_paths("System", "Net", "WebRequest", "Create")

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, {"Create"}):
                if (
                    (member := g.match_ast_d(graph, n_id, "MemberAccess"))
                    and (n_attrs := graph.nodes[member])
                    and f'{n_attrs["expression"]}.{n_attrs["member"]}' in paths
                    and get_node_evaluation_results(method, graph, n_id, set())
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f100.insec_create.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
