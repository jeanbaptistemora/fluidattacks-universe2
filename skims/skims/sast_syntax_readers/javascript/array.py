from model.graph_model import (
    SyntaxStepMeta,
    SyntaxStepObjectInstantiation,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast_group(args.graph, args.n_id, ",", "[", "]")
    elements = [
        args.generic(args.fork_n_id(value))[-1]
        for value in match.values()
        if isinstance(value, str)
    ]
    yield from elements
    yield SyntaxStepObjectInstantiation(
        meta=SyntaxStepMeta(
            danger=False, dependencies=[], n_id=args.n_id, value=elements
        ),
        object_type="Array",
    )
