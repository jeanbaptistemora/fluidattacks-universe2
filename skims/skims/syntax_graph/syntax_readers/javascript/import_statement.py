from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.import_statement import (
    build_import_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Dict,
)
from utils import (
    graph as g,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def get_import_text(args: SyntaxGraphArgs) -> str:
    node = args.ast_graph.nodes[args.n_id]
    source_id = node.get("label_field_source")
    if source_id:
        import_text = node_to_str(args.ast_graph, source_id)
    else:
        import_text = node_to_str(args.ast_graph, args.n_id)
    return import_text


def reader(args: SyntaxGraphArgs) -> NId:
    import_text = get_import_text(args)
    node_attrs: Dict[str, str] = {
        "expression": import_text,
    }
    if import_clause_n_id := g.match_ast_d(
        args.ast_graph, args.n_id, "import_clause"
    ):
        if named_imports_n_id := g.match_ast_d(
            args.ast_graph, import_clause_n_id, "named_imports"
        ):
            for specifier_n_id in g.match_ast_group_d(
                args.ast_graph, named_imports_n_id, "import_specifier"
            ):
                name_n_id = args.ast_graph.nodes[specifier_n_id].get(
                    "label_field_name"
                )
                alias_n_id = args.ast_graph.nodes[specifier_n_id].get(
                    "label_field_alias"
                )
                if name_n_id:
                    identifier = args.ast_graph.nodes[name_n_id].get(
                        "label_text"
                    )
                    node_attrs.update({"identifier": identifier})
                if alias_n_id:
                    alias = args.ast_graph.nodes[alias_n_id].get("label_text")
                    node_attrs.update({"label_alias": alias})
        elif identifier_n_id := g.match_ast_d(
            args.ast_graph, import_clause_n_id, "identifier"
        ):
            identifier = args.ast_graph.nodes[identifier_n_id]["label_text"]
            node_attrs.update({"identifier": identifier})

    return build_import_statement_node(args, node_attrs)
