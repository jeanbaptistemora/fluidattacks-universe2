# Local libraries
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
    match = g.match_ast(
        args.graph,
        args.n_id,
        'type_identifier',
        'instanceof',
        'scoped_type_identifier',
        '__0__',
    )
    type_of_id = match['type_identifier'] or match['scoped_type_identifier']

    if (len(match) == 4 and (statement := match['__0__'])):
        yield graph_model.SyntaxStepInstanceofExpression(
            meta=graph_model.SyntaxStepMeta.default(
                n_id=args.n_id,
                dependencies=[
                    args.generic(args.fork_n_id(statement)),
                ],
            ),
            instanceof_type=args.graph.nodes[type_of_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(args)
