from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    expression_id = args.graph.nodes[args.n_id]["label_field_expression"]
    member_id = args.graph.nodes[args.n_id]["label_field_name"]

    yield graph_model.SyntaxStepMemberAccessExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [args.generic(args.fork_n_id(expression_id))],
        ),
        member=node_to_str(args.graph, member_id),
        expression=node_to_str(args.graph, expression_id),
    )
