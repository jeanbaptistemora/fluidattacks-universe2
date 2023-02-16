from lib_root.utilities.javascript import (
    get_default_alias,
)
from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
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


def is_vuln(graph: Graph, method: MethodsEnum, n_id: NId) -> NId | None:
    for path in get_backward_paths(graph, n_id):
        if evaluation := evaluate(method, graph, path, n_id):
            if "custom_function" in evaluation.triggers:
                return None
            if "algorithm" not in evaluation.triggers:
                return n_id
            if "gzip" in evaluation.triggers:
                evaluation.triggers.difference_update({"algorithm", "gzip"})
                alg_n_id = next(iter(evaluation.triggers))
                return alg_n_id
    return None


def webpack_insecure_compression(
    graph: Graph, method: MethodsEnum
) -> set[NId]:
    vuln_nodes: set[NId] = set()
    if dangerous_library := get_default_alias(
        graph, "compression-webpack-plugin"
    ):
        for n_id in g.matching_nodes(
            graph, label_type="ObjectCreation", name=dangerous_library
        ):
            if (
                parameters_n_id := g.match_ast_d(graph, n_id, "ArgumentList")
            ) and (vuln_n_id := is_vuln(graph, method, parameters_n_id)):
                vuln_nodes.add(vuln_n_id)
    return vuln_nodes
