from model.graph_model import (
    NId,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from typing import (
    Optional,
    Tuple,
)
from utils import (
    graph as g,
)


def get_var_id_type(
    args: SyntaxReaderArgs, n_id: NId
) -> Tuple[Optional[str], str]:
    match = g.match_ast(
        args.graph,
        n_id,
        "nullable_type",
        "simple_identifier",
        "user_type",
    )
    var_id: Optional[str] = match["simple_identifier"]
    if var_id is None:
        raise MissingCaseHandling(args)

    var_type_parent: Optional[str] = match["user_type"]
    var_type: str = ""
    if var_type_parent is None and (null_type := match["nullable_type"]):
        if c_ids := g.get_ast_childs(args.graph, null_type, "user_type"):
            var_type_parent = c_ids[0]
    if (
        var_id
        and var_type_parent
        and (
            var_type_id := g.get_ast_childs(
                args.graph, var_type_parent, "type_identifier"
            )
        )
    ):
        var_type = args.graph.nodes[var_type_id[0]]["label_text"]
        if match["nullable_type"]:
            var_type += "?"
    return args.graph.nodes[var_id]["label_text"], var_type
