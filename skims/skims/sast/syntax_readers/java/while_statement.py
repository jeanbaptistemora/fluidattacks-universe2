# Local libraries
from model import (
    graph_model,
)
from sast.syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from sast.syntax_readers.utils import (
    dependencies_from_arguments,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs,) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph, args.n_id,
        'while',
        'parenthesized_expression',
        'block',
    )
    if (
        len(match) == 3
        and (expression := match['parenthesized_expression'])
    ):
        yield graph_model.SyntaxStepParenthesizedExpression(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id, dependencies_from_arguments(
                    args.fork_n_id(expression),
                ),
            ),
        )
    else:
        raise MissingCaseHandling(args)
