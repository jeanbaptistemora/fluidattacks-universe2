from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    op_id = args.graph.nodes[args.n_id]["label_field_operator"]

    yield graph_model.SyntaxStepBinaryExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
        ),
        operator=args.graph.nodes[op_id]["label_text"],
    )
