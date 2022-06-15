from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNodes,
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


def insec_addheader_write(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSEC_ADDHEADER_WRITE
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        danger_methods = {"AddHeader", "Write"}

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            graph = shard.syntax_graph
            for n_id in search_method_invocation_naive(graph, danger_methods):
                for path in get_backward_paths(graph, n_id):
                    if (
                        evaluation := evaluate(method, graph, path, n_id)
                    ) and evaluation.danger:
                        yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f008.insec_addheader_write.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
