from model.graph_model import (
    SyntaxStepDeclaration,
    SyntaxStepLiteral,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    List,
    Optional,
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
        assignment = []
        var_type: Optional[str] = None
        if value_id := node_attrs.get("label_field_value"):
            value = args.generic(args.fork_n_id(value_id))
            if value and isinstance(value[0], SyntaxStepLiteral):
                var_type = value[0].value_type
            assignment.append(value)

        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(
                args.n_id,
                assignment,
            ),
            var=args.graph.nodes[var_id]["label_text"],
            var_type=var_type,
            is_destructuring=is_destructuring,
        )
