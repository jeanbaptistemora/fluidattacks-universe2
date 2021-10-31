from contextlib import (
    suppress,
)
from model.graph_model import (
    Graph,
)
from more_itertools import (
    pairwise,
)
from sast_transformations.control_flow.common import (
    get_next_id,
    propagate_next_id_from_parent,
    set_next_id,
    try_statement as common_try_statement,
)
from sast_transformations.control_flow.types import (
    CfgArgs,
    Stack,
)
from typing import (
    List,
    Optional,
)
from utils import (
    graph as g,
)


def _nested_method_invocation(
    graph: Graph,
    n_id: str,
) -> List[str]:
    keys: List[str] = [n_id]
    match = g.match_ast(graph, n_id, "method_invocation")
    if next_method := match["method_invocation"]:
        keys.extend(_nested_method_invocation(graph, next_method))
    return keys


def method_invocation(args: CfgArgs, stack: Stack) -> None:
    nested_methods = list(
        reversed(_nested_method_invocation(args.graph, args.n_id))
    )
    for method_id in nested_methods:
        method_attrs = args.graph.nodes[method_id]
        for node in g.adj_ast(
            args.graph, method_attrs["label_field_arguments"]
        )[1:-1]:
            args.generic(args.fork_n_id(node), [])
    with suppress(IndexError):
        if next_id := get_next_id(stack):
            args.graph.add_edge(args.n_id, next_id, **g.ALWAYS)


def lambda_expression(args: CfgArgs, stack: Stack) -> None:
    node_attrs = args.graph.nodes[args.n_id]
    block_id = node_attrs["label_field_body"]
    args.graph.add_edge(args.n_id, block_id, **g.ALWAYS)
    args.generic(args.fork_n_id(block_id), stack)


def switch_expression(args: CfgArgs, stack: Stack) -> None:
    # switch parenthesized_expression switch_block
    node_attrs = args.graph.nodes[args.n_id]
    switch_body = node_attrs["label_field_body"]
    switch_cases = g.adj_ast(args.graph, switch_body)[1:-1]

    groups_withot_statements = []
    for switch_group in switch_cases:
        childrens = g.adj_ast(args.graph, switch_group)
        args.graph.add_edge(args.n_id, switch_group, **g.MAYBE)
        statements_ids = childrens[2:]
        if not statements_ids:
            groups_withot_statements.append(switch_group)
            continue

        for _group_withot_statement in groups_withot_statements:
            args.graph.add_edge(
                _group_withot_statement, statements_ids[0], **g.ALWAYS
            )
        groups_withot_statements = []

        args.graph.add_edge(switch_group, statements_ids[0], **g.ALWAYS)

        for stmt_a_id, stmt_b_id in pairwise(statements_ids):
            # Mark as next_id the next statement in chain
            set_next_id(stack, stmt_b_id)
            args.generic(args.fork_n_id(stmt_a_id), stack)

        # Link recursively the last statement in the block
        propagate_next_id_from_parent(stack)
        args.generic(args.fork_n_id(statements_ids[-1]), stack)


def try_with_resources_statement(args: CfgArgs, stack: Stack) -> None:
    node_attrs = args.graph.nodes[args.n_id]
    _resources = node_attrs["label_field_resources"]

    args.graph.add_edge(args.n_id, _resources, **g.ALWAYS)
    match_resources = g.match_ast_group(args.graph, _resources, "resource")
    last_resource: Optional[str] = None
    for resource in match_resources.get("resource", set()):
        args.graph.add_edge(last_resource or _resources, resource, **g.ALWAYS)
        last_resource = resource

    common_try_statement(args, stack, last_node=last_resource)
