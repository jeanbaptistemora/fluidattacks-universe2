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


def is_danger_yaml_loader(
    graph: Graph, n_ids: list[NId], method: MethodsEnum
) -> bool:
    for _id in n_ids:
        n_attrs = graph.nodes[_id]
        if n_attrs["label_type"] != "NamedArgument":
            continue
        if n_attrs["argument_name"] != "Loader":
            continue
        val_id = n_attrs["value_id"]
        return get_eval_danger(graph, val_id, {"dangerloader"}, method)

    return False


def is_danger_expression(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    n_attrs = graph.nodes[n_id]
    expr = n_attrs["expression"]
    al_id = n_attrs.get("arguments_id")
    if not al_id:
        return False

    args_ids = list(g.adj_ast(graph, al_id))
    if len(args_ids) < 1:
        return False

    if (
        expr == "pickle.load"
        or (
            expr == "yaml.load"
            and len(args_ids) > 1
            and is_danger_yaml_loader(graph, args_ids[1:], method)
        )
    ) and get_eval_danger(graph, args_ids[0], {"userparams"}, method):
        return True

    return False


def python_deserialization_injection(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_DESERIALIZATION_INJECTION

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.PYTHON,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                if is_danger_expression(graph, n_id, method):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.insecure_deserialization",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
