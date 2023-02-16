from collections.abc import (
    Iterator,
)
from lib_root.utilities.c_sharp import (
    yield_syntax_graph_object_creation,
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
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)


def eval_hashes_salt(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_CHECK_HASHES_SALT
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def check_hashes_salt(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in yield_syntax_graph_object_creation(
                graph, {"Rfc2898DeriveBytes"}
            ):
                if eval_hashes_salt(graph, member):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.338.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_CHECK_HASHES_SALT,
    )
