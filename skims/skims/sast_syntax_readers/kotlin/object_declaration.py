from model.graph_model import (
    NId,
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.kotlin.common import (
    get_var_id_type,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
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
        var_name, var_type = get_var_id_type(args, param_id)
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(param_id),
            var=str(var_name),
            var_type=var_type,
            modifiers=set(),
        )
