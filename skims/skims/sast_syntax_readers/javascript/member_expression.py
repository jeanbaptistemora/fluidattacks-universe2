from model.graph_model import (
    SyntaxStepMemberAccessExpression,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils.graph.transformation import (
    node_to_str,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    expression_id = node_attrs["label_field_object"]
    member_id = node_attrs["label_field_property"]

    yield SyntaxStepMemberAccessExpression(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [args.generic(args.fork_n_id(expression_id))],
        ),
        member=node_to_str(args.graph, member_id),
        expression=node_to_str(args.graph, expression_id),
    )
