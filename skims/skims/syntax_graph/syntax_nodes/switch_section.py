from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    List,
)


def build_switch_section_node(
    args: SyntaxGraphArgs,
    case_expr: str,
    execution_ids: List[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        case_expression=case_expr,
        label_type="SwitchSection",
    )

    for statement_id in execution_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(statement_id)),
            label_ast="AST",
        )

    return args.n_id
