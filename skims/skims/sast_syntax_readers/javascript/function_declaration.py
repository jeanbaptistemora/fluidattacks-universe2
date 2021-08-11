from model.graph_model import (
    SyntaxStepLambdaExpression,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    yield SyntaxStepLambdaExpression(
        SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(
                    args.fork_n_id(
                        args.graph.nodes[args.n_id]["label_field_parameters"]
                    )
                ),
            ],
        )
    )
