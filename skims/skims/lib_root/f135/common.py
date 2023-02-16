from lib_root.utilities.c_sharp import (
    yield_syntax_graph_object_creation,
)
from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)


def is_insecure_header(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def insecure_http_headers(graph: Graph, method: MethodsEnum) -> list[str]:
    vuln_nodes: list[str] = []
    for n_id in yield_syntax_graph_object_creation(graph, {"HttpHeaders"}):
        if is_insecure_header(graph, n_id, method):
            vuln_nodes.append(n_id)

    return vuln_nodes
