from model.graph_model import (
    SyntaxStepCatchClause,
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
        args.graph, args.n_id, "catch", "statement_block", "identifier"
    )
    # exceptions may not have an identifier
    if match["identifier"]:
        yield SyntaxStepCatchClause(
            meta=SyntaxStepMeta.default(
                n_id=args.n_id,
                dependencies=dependencies_from_arguments(
                    args.fork_n_id(match["statement_block"]),
                ),
            ),
            var=args.graph.nodes[match["identifier"]]["label_text"],
        )
