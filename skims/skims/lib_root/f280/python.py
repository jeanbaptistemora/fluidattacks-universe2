from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
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
from utils import (
    graph as g,
)


def get_eval_danger(
    graph: Graph, n_id: NId, danger_set: set[str], method: MethodsEnum
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers == danger_set
        ):
            return True
    return False


def is_danger_member(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    danger_set1 = {
        "httpresponse",
    }
    danger_set2 = {
        "sessionid",
        "userparams",
    }
    parent_id = g.pred_ast(graph, n_id)[0]
    if (
        graph.nodes[n_id]["member"] == "set_cookie"
        and get_eval_danger(graph, n_id, danger_set1, method)
        and graph.nodes[parent_id]["label_type"] == "MethodInvocation"
        and (al_id := graph.nodes[parent_id].get("arguments_id"))
        and get_eval_danger(graph, al_id, danger_set2, method)
    ):
        return True

    return False


def is_danger_access(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    n_attrs = graph.nodes[n_id]
    dng_set1 = {
        "httpresponse",
    }
    dng_set2 = {
        "userparams",
    }
    parent_id = g.pred_ast(graph, n_id)[0]
    if graph.nodes[parent_id]["label_type"] != "Assignment":
        return False

    if (
        (val_str := graph.nodes[n_attrs["arguments_id"]].get("value"))
        and val_str[1:-1] == "Set-Cookie"
        and get_eval_danger(graph, n_attrs["expression_id"], dng_set1, method)
        and (val_id := graph.nodes[parent_id].get("value_id"))
        and get_eval_danger(graph, val_id, dng_set2, method)
    ):
        return True

    return False


def python_xml_parser(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_SESSION_FIXATION

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.PYTHON,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in chain(
                g.matching_nodes(graph, label_type="MemberAccess"),
                g.matching_nodes(graph, label_type="ElementAccess"),
            ):
                if (
                    graph.nodes[n_id]["label_type"] == "MemberAccess"
                    and is_danger_member(graph, n_id, method)
                ) or (
                    graph.nodes[n_id]["label_type"] == "ElementAccess"
                    and is_danger_access(graph, n_id, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f280.non_secure_construction_of_cookies",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
