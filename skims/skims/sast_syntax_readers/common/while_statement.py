from model.graph_model import (
    SyntaxStepLoop,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(
    args: SyntaxReaderArgs,
) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]

    yield SyntaxStepLoop(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(
                    args.fork_n_id(node_attrs["label_field_condition"])
                )
            ],
        ),
    )
