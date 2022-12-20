from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Iterator,
    List,
    Optional,
)


def build_string_literal_node(
    args: SyntaxGraphArgs,
    value: str,
    c_ids: Optional[Iterator] = None,
    declaration_vars: Optional[List[str]] = None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value=value,
        value_type="string",
        label_type="Literal",
    )

    if c_ids:
        for c_id in c_ids:
            args.syntax_graph.add_edge(
                args.n_id,
                args.generic(args.fork_n_id(c_id)),
                label_ast="AST",
            )

    if declaration_vars:
        new_id = len(args.ast_graph) + 1
        while args.syntax_graph.nodes.get(str(new_id)):
            new_id = new_id + 1

        for var_name in declaration_vars:
            _id = str(new_id)
            args.syntax_graph.add_node(
                _id,
                symbol=var_name,
                label_type="SymbolLookup",
            )
            args.syntax_graph.add_edge(
                args.n_id,
                _id,
                label_ast="AST",
            )
            new_id = new_id + 1

    return args.n_id
