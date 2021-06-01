import copy
from model.graph_model import (
    Graph,
)
from typing import (
    Dict,
    Optional,
)
from utils import (
    graph as g,
)
from utils.graph.transformation import (
    build_member_access_expression_key,
)


def _local_declaration_statement(
    graph: Graph,
    n_id: str,
    stack: Dict[str, str],
) -> None:
    variable_declaration_id = g.match_ast(
        graph,
        n_id,
        "variable_declaration",
    )["variable_declaration"]
    variable_declarator_id = g.match_ast(
        graph,
        variable_declaration_id,
        "variable_declarator",
    )["variable_declarator"]
    identifier_id = g.match_ast(
        graph,
        variable_declarator_id,
        "identifier",
    )["identifier"]
    stack[graph.nodes[identifier_id]["label_text"]] = variable_declaration_id
    _generic(graph, variable_declarator_id, stack)


def _assignment_expression(
    graph: Graph,
    n_id: str,
    stack: Dict[str, str],
) -> None:
    match = g.match_ast(
        graph,
        n_id,
        "__0__",
        "__1__",  # assignment_operator
        "__2__",
    )
    _generic(graph, match["__2__"], stack)  # right statement
    identifier = match["__0__"]

    key: Optional[str] = None
    if graph.nodes[identifier]["label_type"] == "identifier":
        key = graph.nodes[identifier]["label_text"]
    elif graph.nodes[identifier]["label_type"] == "member_access_expression":
        key = build_member_access_expression_key(graph, identifier)

    if key:
        is_in_cfg = False
        for pred in g.pred_cfg_lazy(graph, n_id, depth=-1):
            childs = g.adj_cfg(
                graph,
                pred,
            )
            if len(childs) > 1:
                is_in_cfg = True
                break
        stack[key] = n_id
        if is_in_cfg and (next_statement := g.adj_cfg(graph, n_id)):
            # create a new evaluation branch if it is inside a control
            # structure
            new_stack = copy.deepcopy(stack)
            _generic(graph, next_statement[0], new_stack)


def _identifier(
    graph: Graph,
    n_id: str,
    stack: Dict[str, str],
) -> None:
    if assignment_id := stack.get(graph.nodes[n_id]["label_text"]):
        parent_a = g.lookup_first_cfg_parent(graph, assignment_id)
        parent_b = g.lookup_first_cfg_parent(graph, n_id)
        identifier_name = graph.nodes[n_id]["label_text"]
        for adj in g.adj_cfg_lazy(graph, parent_a, depth=-1):
            if adj == parent_b:
                if graph.nodes[assignment_id]["label_type"] in {"parameter"}:
                    parent_a = assignment_id
                graph.add_edge(
                    parent_a,
                    parent_b,
                    dependence=identifier_name,
                    label_pdg="PDG",
                )
                break


def _generic_search_identifier_usage(
    graph: Graph,
    n_id: str,
    stack: Dict[str, str],
) -> None:
    statemet_identifiers = g.filter_nodes(
        graph,
        g.adj_ast(graph, n_id, depth=-1, strict=True),
        g.pred_has_labels(
            label_type="identifier",
        ),
    )
    for identifier_id in statemet_identifiers:
        if assignment_id := stack.get(
            graph.nodes[identifier_id]["label_text"]
        ):
            parent_a = g.lookup_first_cfg_parent(graph, assignment_id)
            parent_b = g.lookup_first_cfg_parent(graph, identifier_id)
            identifier_name = graph.nodes[identifier_id]["label_text"]
            for adj in g.adj_cfg_lazy(graph, parent_a, depth=-1):
                if adj == parent_b:
                    if graph.nodes[assignment_id]["label_type"] in {
                        "parameter"
                    }:
                        parent_a = assignment_id
                    graph.add_edge(
                        parent_a,
                        parent_b,
                        dependence=identifier_name,
                        label_pdg="PDG",
                    )
                    break


def _method_declaration(
    graph: Graph,
    n_id: str,
    stack: Dict[str, str],
) -> None:
    parameters = g.filter_nodes(
        graph,
        g.adj_ast(graph, n_id, depth=-1, strict=True),
        g.pred_has_labels(label_type="parameter"),
    )
    for parameter_id in parameters:
        if identifier_id := g.match_ast_group(
            graph,
            parameter_id,
            "__0__",
            "__1__",
        )["__1__"]:
            stack[graph.nodes[identifier_id]["label_text"]] = parameter_id
    _generic(graph, g.adj_cfg(graph, n_id)[-1], stack)


def _generic(
    graph: Graph,
    n_id: str,
    stack: Dict[str, str],
) -> None:
    walkers = {
        "local_declaration_statement": _local_declaration_statement,
        "using_statement": _local_declaration_statement,
        "assignment_expression": _assignment_expression,
        "constructor_declaration": _method_declaration,
        "method_declaration": _method_declaration,
        "identifier": _identifier,
    }
    high_nodes = {
        "constructor_body",
        "body",
        "block",
        "expression_statement",
    }
    n_id_attrs = graph.nodes[n_id]
    label_type = n_id_attrs["label_type"]

    if walker := walkers.get(label_type):
        walker(graph, n_id, stack)
    else:
        _generic_search_identifier_usage(graph, n_id, stack)
        for statement_id in g.adj_cfg_lazy(graph, n_id, depth=-1):
            label_type = graph.nodes[statement_id]["label_type"]
            if walker := walkers.get(label_type):
                walker(graph, statement_id, stack)
            elif stack and label_type not in high_nodes:
                _generic_search_identifier_usage(graph, statement_id, stack)


def add(graph: Graph) -> None:
    def _predicate(n_id: str) -> bool:
        return (
            g.pred_has_labels(
                label_type="method_declaration",
            )(n_id)
            or g.pred_has_labels(label_type="constructor_declaration")(n_id)
        )

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=_predicate,
    ):
        _generic(graph, n_id, stack=dict())
