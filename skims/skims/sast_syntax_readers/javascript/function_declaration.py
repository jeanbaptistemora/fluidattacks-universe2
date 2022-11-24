from model.graph_model import (
    SyntaxStep,
    SyntaxStepLambdaExpression,
    SyntaxStepMeta,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
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
