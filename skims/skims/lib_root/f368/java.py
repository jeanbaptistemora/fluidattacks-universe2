from lib_root.utilities.common import (
    search_method_invocation_naive,
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
    List,
    Tuple,
)
from utils import (
    graph as g,
)


def is_object_vuln(
    graph: Graph,
    n_id: NId,
) -> bool:
    method = MethodsEnum.JAVA_HOST_KEY_CHECKING
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def is_config_vuln(
    graph: Graph,
    config_ids: Tuple[NId, ...],
) -> bool:
    method = MethodsEnum.JAVA_HOST_KEY_CHECKING
    conditions: List[str] = []
    for n_id in config_ids:
        for path in get_backward_paths(graph, n_id):
            evaluation = evaluate(method, graph, path, n_id)
            if evaluation and evaluation.triggers in [{"hostkey"}, {"no"}]:
                conditions = conditions + list(evaluation.triggers)

    if conditions == ["hostkey", "no"]:
        return True
    return False


def is_session_vuln(
    graph: Graph,
    session_args: Tuple[NId, ...],
) -> bool:
    if len(session_args) == 1 and is_object_vuln(graph, session_args[0]):
        return True
    if len(session_args) == 2 and is_config_vuln(graph, session_args):
        return True
    return False


def host_key_checking(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    java = GraphLanguage.JAVA
    danger_methods = {"setConfig"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(java):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, danger_methods):
                if (
                    (al_list := graph.nodes[n_id].get("arguments_id"))
                    and (args_nodes := g.adj_ast(graph, al_list))
                    and len(args_nodes) > 0
                    and is_session_vuln(graph, args_nodes)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f368.insecure_host_key_checking",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_HOST_KEY_CHECKING,
    )
