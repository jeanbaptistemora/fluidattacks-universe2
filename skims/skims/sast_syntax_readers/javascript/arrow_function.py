from model import (
    graph_model,
)
from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
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
        "=>",
        "__0__",
        "identifier",
        "formal_parameters",
    )
    if identifier_id := match["identifier"]:
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(args.n_id),
            var=args.graph.nodes[identifier_id]["label_text"],
        )
    elif parameters_id := match["formal_parameters"]:
        yield from args.generic(args.fork_n_id(parameters_id))

    yield graph_model.SyntaxStepLambdaExpression(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            dependencies_from_arguments(args.fork_n_id(match["__0__"])),
        ),
    )
