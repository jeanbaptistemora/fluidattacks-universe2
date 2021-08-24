from model.graph_model import (
    NId,
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
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


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    label_type = args.graph.nodes[args.n_id]["label_type"]
    params_ids: Tuple[NId, ...] = tuple()
    if label_type == "function_declaration":
        params_ids = g.get_ast_childs(args.graph, args.n_id, "parameter")
    elif label_type == "class_declaration":
        params_ids = g.get_ast_childs(
            args.graph, args.n_id, "class_parameter", depth=2
        )

    for param_id in params_ids:
        match = g.match_ast(
            args.graph,
            param_id,
            "nullable_type",
            "simple_identifier",
            "user_type",
        )
        var_id: Optional[str] = match["simple_identifier"]
        var_type_parent: Optional[str] = match["user_type"]
        if (
            var_type_parent is None
            and (null_type := match["nullable_type"])
            and (c_ids := g.get_ast_childs(args.graph, null_type, "user_type"))
        ):
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
            yield SyntaxStepDeclaration(
                meta=SyntaxStepMeta.default(param_id),
                var=args.graph.nodes[var_id]["label_text"],
                var_type=var_type,
                modifiers=set(),
            )
        else:
            raise MissingCaseHandling(args)
