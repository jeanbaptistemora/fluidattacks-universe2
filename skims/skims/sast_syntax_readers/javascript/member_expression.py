from model.graph_model import (
    SyntaxStepMemberAccessExpression,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils.graph.transformation import (
    build_member_access_expression_key,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    expression_str = build_member_access_expression_key(args.graph, args.n_id)
    member_str = args.graph.nodes[node_attrs["label_field_property"]].get(
        "label_text"
    )
    yield SyntaxStepMemberAccessExpression(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [args.generic(args.fork_n_id(node_attrs["label_field_object"]))],
        ),
        member=member_str,
        expression=expression_str,
    )
