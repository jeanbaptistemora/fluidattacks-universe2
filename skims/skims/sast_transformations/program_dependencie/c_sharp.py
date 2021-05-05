from typing import Dict
import copy
from model.graph_model import Graph
from utils import graph as g


def _expression_statement(
    graph: Graph,
    n_id: str,
    stack: Dict[str, str],
) -> None:
    for next_statement in g.adj_cfg(graph, n_id):
        new_stack = copy.deepcopy(stack)
        _generic(graph, next_statement, new_stack)


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
            parent_assignment = g.pred_ast(graph, assignment_id)[-1]
            parent_identifier = g.pred_ast(graph, identifier_id)[-1]
            if graph.nodes[parent_assignment]["label_type"] in {
                "assignment_expression",
                "variable_declarator",
            }:
                continue
            if graph.nodes[parent_identifier]["label_type"] in {
                "assignment_expression",
                "variable_declarator",
            }:
                continue
            if assignment_id != identifier_id and parent_assignment != n_id:
                graph.add_edge(assignment_id, identifier_id, label_pdg="PDG")


def _generic(
    graph: Graph,
    n_id: str,
    stack: Dict[str, str],
) -> None:
    walkers = {
        "expression_statement": _expression_statement,
    }
    high_nodes = {
        "constructor_body",
        "body",
        "block",
    }
    n_id_attrs = graph.nodes[n_id]
    label_type = n_id_attrs["label_type"]
    if walker := walkers.get(label_type):
        walker(graph, n_id, stack)
    else:
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
