from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    yield graph_model.SyntaxStepParenthesizedExpression(
        meta=graph_model.SyntaxStepMeta.default(
            n_id=args.n_id,
        ),
    )
