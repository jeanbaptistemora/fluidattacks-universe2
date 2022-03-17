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


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "lambda_expression",
        "inferred_parameters",
        "__0__",
        "__1__",
    )
    if len(match) == 4:
        yield graph_model.SyntaxStepLambdaExpression(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                dependencies_from_arguments(args.fork_n_id(
                    str(match["__1__"])
                )),
            ),
        )
    else:
        raise MissingCaseHandling(args)
