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


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        'new',
        '__0__',
        'dimensions_expr',
    )

    if (
        len(match) == 3
        and match['new']
        and (object_type_id := match['__0__'])
        and (dimension := match['dimensions_expr'])
    ):
        match = g.match_ast(
            args.graph,
            dimension,
            '__1__',
        )
        yield graph_model.SyntaxStepArrayInstantiation(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id, dependencies_from_arguments(
                    args.fork_n_id(match['__1__']),
                ),
            ),
            array_type=args.graph.nodes[object_type_id]['label_text'],
        )
    elif (
        len(match) == 5
        and match['new']
        and (object_type_id := match['__0__'])
        and (match['__1__'])
        and (initializer := match['__2__'])
    ):
        yield graph_model.SyntaxStepArrayInstantiation(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, [
                args.generic(args.fork_n_id(initializer)),
            ]),
            array_type=args.graph.nodes[object_type_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(args)
