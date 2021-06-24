from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def _get_var_type(args: SyntaxReaderArgs, var_type: str = "") -> str:
    label_type = args.graph.nodes[args.n_id]["label_type"]
    if label_type == "type_identifier":
        var_type += args.graph.nodes[args.n_id]["label_text"]
    elif label_type == "qualified_type":
        match = g.match_ast(
            args.graph, args.n_id, "package_identifier", "type_identifier"
        )
        package_id = match["package_identifier"]
        var_type = _get_var_type(
            args.fork_n_id(match["type_identifier"]),
            f"{var_type}{args.graph.nodes[package_id]['label_text']}.",
        )
    elif label_type == "pointer_type":
        match = g.match_ast(args.graph, args.n_id, "*", "__0__")
        var_type = _get_var_type(args.fork_n_id(match["__0__"]), "*")
    elif label_type == "slice_type":
        match = g.match_ast(args.graph, args.n_id, "[", "]", "__0__")
        var_type = _get_var_type(
            args.fork_n_id(match["__0__"]), f"{var_type}[]"
        )
    elif label_type == "map_type":
        match = g.match_ast(
            args.graph, args.n_id, "map", "[", "]", "__0__", "__1__"
        )
        var_type += (
            f"map[{_get_var_type(args.fork_n_id(match['__0__']))}]"
            f"{_get_var_type(args.fork_n_id(match['__1__']))}"
        )
    else:
        raise MissingCaseHandling(args)
    return var_type


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    params = g.get_ast_childs(args.graph, args.n_id, "parameter_list")[-1]
    for p_id in g.get_ast_childs(args.graph, params, "parameter_declaration"):
        yield from function_declaration_parameter(args.fork_n_id(p_id))


def function_declaration_parameter(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(args.graph, args.n_id, "identifier", "__0__")
    var_name_id = match["identifier"]
    var_type = _get_var_type(args.fork_n_id(match["__0__"]))
    yield SyntaxStepDeclaration(
        meta=SyntaxStepMeta.default(args.n_id),
        var=args.graph.nodes[var_name_id]["label_text"],
        var_type=var_type,
        modifiers=set(),
    )
