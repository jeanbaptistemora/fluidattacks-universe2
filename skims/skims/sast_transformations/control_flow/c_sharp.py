from more_itertools import (
    pairwise,
)
from sast_transformations.control_flow.common import (
    link_to_last_node as common_link_to_last_node,
    propagate_next_id_from_parent,
    set_next_id,
)
from sast_transformations.control_flow.types import (
    CfgArgs,
    Stack,
)
from utils import (
    graph as g,
)


def switch_statement(args: CfgArgs, stack: Stack) -> None:
    # switch parenthesized_expression switch_block
    try:
        switch_block, *_ = g.adj_ast(
            args.graph, args.n_id, label_type="switch_body"
        )
    except IndexError as exc:
        raise NotImplementedError() from exc

    switch_sections = tuple(
        c_id
        for c_id in g.adj_ast(
            args.graph, switch_block, label_type="switch_section"
        )
    )

    switch_flows = []
    for c_id in switch_sections:
        case_label, *cases_statements = g.adj_ast(args.graph, c_id)
        switch_flows.append([case_label])
        for c_c_id in cases_statements:
            switch_flows[-1].append(c_c_id)
            if args.graph.nodes[c_c_id]["label_type"] == "break_statement":
                break

    for stmt_ids in switch_flows:
        # Link to the first statement in the block
        args.graph.add_edge(args.n_id, stmt_ids[0], **g.MAYBE)

        # Walk pairs of elements
        for stmt_a_id, stmt_b_id in pairwise(stmt_ids):
            # Mark as next_id the next statement in chain
            set_next_id(stack, stmt_b_id)
            args.generic(args.fork_n_id(stmt_a_id), stack)

        # Link recursively the last statement in the block
        propagate_next_id_from_parent(stack)
        args.generic(args.fork_n_id(stmt_ids[-1]), stack)


def using_statement(args: CfgArgs, stack: Stack) -> None:
    match = g.match_ast(args.graph, args.n_id, "block")
    if block_id := match["block"]:
        args.graph.add_edge(args.n_id, block_id, **g.ALWAYS)
        args.generic(args.fork_n_id(block_id), stack)
    propagate_next_id_from_parent(stack)
    common_link_to_last_node(args, stack)


def lambda_expression(args: CfgArgs, stack: Stack) -> None:
    node_attrs = args.graph.nodes[args.n_id]
    if "label_field_body" not in node_attrs:
        return

    body_id = node_attrs["label_field_body"]
    args.graph.add_edge(args.n_id, body_id, **g.ALWAYS)
    args.generic(args.fork_n_id(body_id), stack)
