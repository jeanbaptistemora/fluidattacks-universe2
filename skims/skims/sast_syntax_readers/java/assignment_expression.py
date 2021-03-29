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
    assignment_operators = {
        '=',
        '+=',
        '-=',
        '*=',
        '/=',
        '%=',
        '&=',
        '^=',
        '|=',
        '<<=',
        '>>=',
        '>>>=',
    }
    match = g.match_ast(
        args.graph,
        args.n_id,
        '__0__',
        '__1__',
        '__2__',
    )

    # pylint: disable=used-before-assignment
    if (
        (var_id := match['__0__'])
        and (op_id := match['__1__'])
        and (args.graph.nodes[op_id]['label_text'] in assignment_operators)
        and (src_id := match['__2__'])
    ):
        yield graph_model.SyntaxStepAssignment(
            meta=graph_model.SyntaxStepMeta.default(args.n_id, [
                args.generic(args.fork_n_id(src_id)),
            ]),
            var=args.graph.nodes[var_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(args)
