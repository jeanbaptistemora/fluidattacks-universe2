from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_function_signature_node(
    args: SyntaxGraphArgs, function_name: str, parameters_id: NId
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        function_name=function_name,
        label_type="FunctionSignature",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(parameters_id)),
        label_ast="AST",
    )

    return args.n_id
