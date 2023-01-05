from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Dict,
)


def build_import_statement_node(
    args: SyntaxGraphArgs, *imported_elements: Dict[str, str]
) -> NId:
    if len(imported_elements) == 1:
        imported_elements[0].pop("corrected_n_id", None)
        args.syntax_graph.add_node(
            args.n_id,
            **imported_elements[0],
            label_type="Import",
        )
    else:
        args.syntax_graph.add_node(
            args.n_id,
            import_type="multiple_import",
            label_type="Import",
        )
        for imported_element in imported_elements:
            corrected_n_id = imported_element.pop("corrected_n_id", None)
            imported_element.update({"label_type": "Import"})
            args.syntax_graph.add_node(corrected_n_id, **imported_element)
            if corrected_n_id:
                args.syntax_graph.add_edge(
                    args.n_id,
                    corrected_n_id,
                    label_ast="AST",
                )

    return args.n_id
