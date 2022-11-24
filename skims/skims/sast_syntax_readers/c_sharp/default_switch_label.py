from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    yield graph_model.SyntaxStepSwitchLabelDefault(
        meta=graph_model.SyntaxStepMeta.default(args.n_id),
    )
