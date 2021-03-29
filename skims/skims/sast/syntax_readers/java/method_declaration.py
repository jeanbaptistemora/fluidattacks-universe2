# Local libraries
from model import (
    graph_model,
)
from sast.syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    for ps_id in g.get_ast_childs(args.graph, args.n_id, 'formal_parameters'):
        for p_id in g.get_ast_childs(args.graph, ps_id, 'formal_parameter'):
            yield from method_declaration_formal_parameter(
                args.fork_n_id(p_id)
            )


def method_declaration_formal_parameter(
    args: SyntaxReaderArgs,
) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, '__0__', '__1__')

    if (
        len(match) == 2
        and (var_type_id := match['__0__'])
        and (var_id := match['__1__'])
    ):
        yield graph_model.SyntaxStepDeclaration(
            meta=graph_model.SyntaxStepMeta.default(args.n_id),
            var=args.graph.nodes[var_id]['label_text'],
            var_type=args.graph.nodes[var_type_id]['label_text'],
        )
    else:
        raise MissingCaseHandling(args)
