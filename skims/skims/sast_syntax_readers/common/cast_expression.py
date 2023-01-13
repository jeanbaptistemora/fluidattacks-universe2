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
    match = g.match_ast(args.graph, args.n_id, "(", "__0__", ")", "__1__")

    if cast_type_id := match["__0__"]:
        yield graph_model.SyntaxStepCastExpression(
            meta=graph_model.SyntaxStepMeta.default(
                n_id=args.n_id,
            ),
            cast_type=args.graph.nodes[cast_type_id]["label_text"],
        )
    else:
        raise MissingCaseHandling(args)
