from collections.abc import (
    Iterator,
)
from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
import re
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def param_is_safe(graph: Graph, p_id: NId, expression: str) -> bool:
    method = MethodsEnum.JS_HAS_REVERSE_TABNABBING
    matcher = re.compile(expression)

    for path in get_backward_paths(graph, p_id):
        evaluation = evaluate(method, graph, path, p_id)
        return bool(
            evaluation
            and evaluation.danger
            and evaluation.triggers
            and matcher.match(next(iter(evaluation.triggers)))
        )
    return True


def node_is_vulnerable(graph: Graph, params: Iterator[NId]) -> bool:
    url: NId = next(params)
    if param_is_safe(graph, url, r"(?!^https?://)"):
        return False
    try:
        name: NId = next(params)
        if param_is_safe(graph, name, r"(?!^_blank$)"):
            return False
    except StopIteration:
        return True
    try:
        window_features: NId = next(params)
        if param_is_safe(
            graph, window_features, r"(?=.*noopener)(?=.*noreferrer)"
        ):
            return False
    except StopIteration:
        return True
    return True


def get_vulns_n_ids(graph: Graph) -> Iterator[NId]:
    for n_id in g.matching_nodes(
        graph, label_type="MethodInvocation", expression="window.open"
    ):
        if (n_attrs := g.match_ast_d(graph, n_id, "ArgumentList")) and (
            (parameters := g.adj_ast(graph, n_attrs))
            and node_is_vulnerable(graph, iter(parameters))
        ):
            yield n_id
