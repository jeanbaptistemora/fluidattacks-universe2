from model import (
    graph_model,
)
from model.graph_model import (
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    yield graph_model.SyntaxStepSwitchLabelCase(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(
                    args.fork_n_id(
                        args.graph.nodes[args.n_id]["label_field_value"],
                    )
                ),
            ],
        ),
    )
