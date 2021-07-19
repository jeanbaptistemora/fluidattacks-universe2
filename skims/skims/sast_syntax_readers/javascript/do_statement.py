from model import (
    graph_model,
)
from model.graph_model import (
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "parenthesized_expression",
    )

    yield graph_model.SyntaxStepParenthesizedExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            dependencies_from_arguments(
                args.fork_n_id(match["parenthesized_expression"]),
            ),
        ),
    )
