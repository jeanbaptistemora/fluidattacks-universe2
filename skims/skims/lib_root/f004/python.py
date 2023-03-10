from collections.abc import (
    Iterator,
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
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def is_danger_shell(
    graph: Graph, n_ids: list[NId], method: MethodsEnum
) -> bool:
    for _id in n_ids:
        if graph.nodes[_id]["argument_name"] != "shell":
            continue
        val_id = graph.nodes[_id]["value_id"]
        return get_node_evaluation_results(method, graph, val_id, set())
    return False


def is_danger_expression(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    m_attrs = graph.nodes[n_id]
    expr: str = m_attrs["expression"]
    al_id = m_attrs.get("arguments_id")
    if not al_id:
        return False
    args_ids = list(g.adj_ast(graph, al_id))

    if (
        expr.startswith("os.")
        and get_node_evaluation_results(
            method, graph, args_ids[0], {"userparams"}
        )
    ) or (
        len(args_ids) > 1
        and is_danger_shell(graph, args_ids[1:], method)
        and get_node_evaluation_results(
            method, graph, args_ids[0], {"userparams"}
        )
    ):
        return True
    return False


def python_remote_command_execution(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_REMOTE_COMMAND_EXECUTION
    danger_set = {"os.popen", "subprocess.Popen"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.PYTHON,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                if graph.nodes[n_id][
                    "expression"
                ] in danger_set and is_danger_expression(graph, n_id, method):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
