from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
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
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def is_argument_vuln(
    graph: Graph,
    n_id: NId,
) -> bool:
    method = MethodsEnum.TS_REMOTE_COMMAND_EXECUTION
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def remote_command_execution(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    typescript = GraphLanguage.TYPESCRIPT
    danger_methods = {"command", "execSync"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(typescript):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, danger_methods):
                if (
                    is_argument_vuln(graph, n_id)
                    and (args_id := graph.nodes[n_id].get("arguments_id"))
                    and (args := g.match_ast(graph, args_id))
                    and (len(args) == 1)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.TS_REMOTE_COMMAND_EXECUTION,
    )
