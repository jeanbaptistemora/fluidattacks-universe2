from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from utils import (
    graph as g,
)


def reader(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "while",
        "(",
        ")",
        "block",
        "__0__",
    )
    if len(match) == 5 and (expression := match["__0__"]):
        yield graph_model.SyntaxStepParenthesizedExpression(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                dependencies_from_arguments(
                    args.fork_n_id(expression),
                ),
            ),
        )
    else:
        raise MissingCaseHandling(args)
