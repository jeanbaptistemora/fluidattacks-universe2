from model.graph_model import (
    SyntaxStepMemberAccessExpression,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    yield SyntaxStepMemberAccessExpression(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [args.generic(args.fork_n_id(node_attrs["label_field_object"]))],
        ),
        member=args.graph.nodes[node_attrs["label_field_property"]].get(
            "label_text"
        ),
    )
