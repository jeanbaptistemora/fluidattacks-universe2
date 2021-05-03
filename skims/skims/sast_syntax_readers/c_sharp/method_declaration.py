# Local libraries
from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import graph as g


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    for ps_id in g.get_ast_childs(args.graph, args.n_id, "parameter_list"):
        for p_id in g.get_ast_childs(args.graph, ps_id, "parameter"):
            yield from _method_declaration_parameters(args.fork_n_id(p_id))


def _method_declaration_parameters(
    args: SyntaxReaderArgs,
) -> SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "predefined_type",
        "identifier",
    )
    if (
        len(match) == 2
        and (var_type_id := match["predefined_type"])
        and (var_id := match["identifier"])
    ):
        var_type_str: str = args.graph.nodes[var_type_id]["label_text"]

        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(args.n_id),
            var=args.graph.nodes[var_id]["label_text"],
            var_type=var_type_str,
        )
    else:
        raise MissingCaseHandling(args)
