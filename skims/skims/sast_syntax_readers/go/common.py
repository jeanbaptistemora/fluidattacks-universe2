from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def get_var_type(args: SyntaxReaderArgs, var_type: str = "") -> str:
    # Recurse until we get the basic label `type_identifier`
    label_type = args.graph.nodes[args.n_id]["label_type"]
    if label_type == "type_identifier":
        # Basic types, e.g. int, string
        var_type += args.graph.nodes[args.n_id]["label_text"]
    elif label_type == "qualified_type":
        # Types from a package, e.g. http.Request
        match = g.match_ast(
            args.graph, args.n_id, "package_identifier", "type_identifier"
        )
        package_id = match["package_identifier"]
        if nid := match["type_identifier"]:
            var_type = get_var_type(
                args.fork_n_id(nid),
                f"{var_type}{args.graph.nodes[package_id]['label_text']}.",
            )
    elif label_type == "pointer_type":
        # Pointer type, e.g. *int, *http.ResponseWriter
        match = g.match_ast(args.graph, args.n_id, "*", "__0__")
        if nid := match["__0__"]:
            var_type = get_var_type(args.fork_n_id(nid), "*")
    elif label_type == "slice_type":
        # Array type, e.g. []int, []string
        match = g.match_ast(args.graph, args.n_id, "[", "]", "__0__")
        if nid := match["__0__"]:
            var_type = get_var_type(args.fork_n_id(nid), f"{var_type}[]")
    elif label_type == "map_type":
        # Map types, e.g. map[string]int, map[int]http.Request
        match = g.match_ast(
            args.graph, args.n_id, "map", "[", "]", "__0__", "__1__"
        )
        if (nid_0 := match["__0__"]) and (nid_1 := match["__1__"]):
            var_type += (
                f"map[{get_var_type(args.fork_n_id(nid_0))}]"
                f"{get_var_type(args.fork_n_id(nid_1))}"
            )
    else:
        raise MissingCaseHandling(args)
    return var_type
