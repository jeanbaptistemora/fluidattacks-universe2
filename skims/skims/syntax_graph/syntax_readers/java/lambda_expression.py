from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.lambda_expression import (
    build_lambda_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    body_id = n_attrs["label_field_body"]
    parameters_id = n_attrs["label_field_parameters"]
    identifier = "Unnamed"

    return build_lambda_expression_node(
        args, identifier, body_id, parameters_id
    )
