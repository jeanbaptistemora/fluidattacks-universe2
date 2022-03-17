from .common import (
    get_var_type,
)
from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    # Methods have an extra parameter_list object, but we only need the one
    # that describes the arguments received by the function
    label_type = args.graph.nodes[args.n_id]["label_type"]
    params = g.get_ast_childs(args.graph, args.n_id, "parameter_list")
    if label_type == "method_declaration":
        params = params[1:]
    for p_id in g.get_ast_childs(
        args.graph, params[0], "parameter_declaration"
    ):
        yield from function_declaration_parameter(args.fork_n_id(p_id))


def function_declaration_parameter(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, "identifier", "__0__")
    var_name_id = match["identifier"]
    var_type = get_var_type(args.fork_n_id(str(match["__0__"])))
    yield SyntaxStepDeclaration(
        meta=SyntaxStepMeta.default(args.n_id),
        var=args.graph.nodes[var_name_id]["label_text"],
        var_type=var_type,
        modifiers=set(),
    )
