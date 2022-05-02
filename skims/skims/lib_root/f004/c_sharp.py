from lib_root.utilities.c_sharp import (
    get_first_member,
    get_object_identifiers,
)
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


def remote_command_execution(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_REMOTE_COMMAND_EXECUTION
    finding = method.value.finding
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            executors_objs = get_object_identifiers(
                shard, graph_db, {"Executor"}
            )
            syntax_graph = shard.syntax_graph
            executors = list(
                search_method_invocation_naive(syntax_graph, {"Execute"})
            )
            danger_meths = set(
                search_method_invocation_naive(syntax_graph, {"Start"})
            )
            methods = [
                executor
                if (
                    (member := get_first_member(shard, executor))
                    and shard.graph.nodes[member]["label_text"]
                    in executors_objs
                )
                else None
                for executor in executors
            ]
            danger_meths.update(filter(None, methods))
            for n_id in danger_meths:
                for path in get_backward_paths(syntax_graph, n_id):
                    if evaluate(c_sharp, finding, syntax_graph, path, n_id):
                        yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
