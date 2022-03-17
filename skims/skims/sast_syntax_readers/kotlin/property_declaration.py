from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.kotlin.common import (
    get_var_id_type,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from typing import (
    Set,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "modifiers",
        "val",
        "var",
        "variable_declaration",
        "=",
    )
    if var_id_parent := match["variable_declaration"]:
        var_name, var_type = get_var_id_type(args, var_id_parent)
        modifiers: Set = set()
        deps = (
            [args.generic(args.fork_n_id(match["__0__"]))]
            if match["="]
            else []
        )
        if modifiers_id := match["modifiers"]:
            modifiers = set(
                args.graph.nodes[g.adj_ast(args.graph, modifier_type)[0]][
                    "label_text"
                ]
                if args.graph.nodes[modifier_type]["label_type"]
                not in {"property_modifier"}
                else args.graph.nodes[modifier_type]["label_text"]
                for modifier_type in g.adj_ast(args.graph, modifiers_id)
            )
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(n_id=var_id_parent, dependencies=deps),
            var=str(var_name),
            var_type=var_type,
            modifiers=modifiers,
        )
    else:
        raise MissingCaseHandling(args)
