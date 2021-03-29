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


def reader(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, 'new', '__0__', 'argument_list')

    if (
        match['new']
        and (object_type_id := match['__0__'])
        and (args_id := match['argument_list'])
    ):
        yield graph_model.SyntaxStepObjectInstantiation(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id, dependencies_from_arguments(
                    args.fork_n_id(args_id),
                ),
            ),
            object_type=(
                args.graph.nodes[object_type_id]['label_text']
                .split('<', maxsplit=1)[0]
            ),
        )
    else:
        raise MissingCaseHandling(args)
