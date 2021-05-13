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
    match = g.match_ast_group(
        args.graph,
        args.n_id,
        "predefined_type",
        "identifier",
    )
    # pylint:disable=used-before-assignment
    if (_identifiers := match["identifier"]) and len(_identifiers) == 2:
        # pylint:disable=unpacking-non-sequence
        param_type, param_identifier = _identifiers
    elif (_var_type_id := match["predefined_type"]) and (
        _var_id := match["identifier"]
    ):
        param_type = _var_type_id.pop()
        param_identifier = _var_id.pop()
    else:
        raise MissingCaseHandling(args)

    var_type_str: str = args.graph.nodes[param_type]["label_text"]
    var_identifier_str: str = args.graph.nodes[param_identifier]["label_text"]

    yield SyntaxStepDeclaration(
        meta=SyntaxStepMeta.default(args.n_id),
        var=var_identifier_str,
        var_type=var_type_str,
    )
