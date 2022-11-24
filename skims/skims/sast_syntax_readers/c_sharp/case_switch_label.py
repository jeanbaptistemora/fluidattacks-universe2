from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id)

    if len(match) == 3:
        yield graph_model.SyntaxStepSwitchLabelCase(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(str(match["__1__"]))),
                ],
            ),
        )
    else:
        raise MissingCaseHandling(args)
