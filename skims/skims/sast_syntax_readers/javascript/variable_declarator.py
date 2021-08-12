from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    List,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> SyntaxStepsLazy:
    node_attrs = args.graph.nodes[args.n_id]
    var_name_attrs = args.graph.nodes[node_attrs["label_field_name"]]
    variable_ids: List[str] = []
    is_destructuring = False

    if var_name_attrs["label_type"] == "identifier":
        variable_ids.append(node_attrs["label_field_name"])
    elif var_name_attrs["label_type"] == "object_pattern":
        is_destructuring = True
        variable_ids = g.match_ast_group(
            args.graph,
            node_attrs["label_field_name"],
            "shorthand_property_identifier_pattern",
        )["shorthand_property_identifier_pattern"]

    for var_id in variable_ids:
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(
                        args.fork_n_id(node_attrs["label_field_value"])
                    ),
                ]
                if "label_field_value" in node_attrs
                else [],
            ),
            var=args.graph.nodes[var_id]["label_text"],
            is_destructuring=is_destructuring,
        )
