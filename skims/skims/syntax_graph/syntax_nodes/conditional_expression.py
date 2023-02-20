from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_conditional_expression_node(
    args: SyntaxGraphArgs,
    condition_node: str | None,
    true_block: str,
    false_block: str,
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        label_type="ConditionalExpression",
        true_block_id=true_block,
        false_block_id=false_block,
    )

    if condition_node:
        args.syntax_graph.nodes[args.n_id]["conditional_id"] = condition_node

        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(condition_node)),
            label_ast="AST",
        )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(true_block)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(false_block)),
        label_ast="AST",
    )

    return args.n_id
