from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_for_each_statement_node(
    args: SyntaxGraphArgs, var_node: str, iterable_item: str, block: str
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        variable_id=var_node,
        iterable_item_id=iterable_item,
        label_type="ForEachStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(var_node)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(iterable_item)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block)),
        label_ast="AST",
    )

    return args.n_id
