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
    c_ids = g.adj_ast(args.graph, args.n_id)

    identifier_ids = c_ids[0:-1]
    root_id = c_ids[0]
    path_ids = c_ids[1:-1]
    args_id = c_ids[-1]

    dot_chain = {
        'field_access',
        'identifier',
        '.',
    }

    if g.contains_label_type_in(args.graph, identifier_ids, dot_chain):
        yield graph_model.SyntaxStepMethodInvocation(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id, dependencies_from_arguments(
                    args.fork_n_id(args_id),
                ),
            ),
            method=g.concatenate_label_text(args.graph, identifier_ids),
        )
    elif g.contains_label_type_in(args.graph, path_ids, dot_chain):
        yield graph_model.SyntaxStepMethodInvocationChain(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id, [
                    args.generic(args.fork_n_id(root_id)),
                    *dependencies_from_arguments(
                        args.fork_n_id(args_id),
                    ),
                ],
            ),
            method=g.concatenate_label_text(args.graph, path_ids),
        )
    else:
        raise MissingCaseHandling(args)
