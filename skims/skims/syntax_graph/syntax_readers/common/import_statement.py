from model.graph_model import (
    Graph,
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


def import_label_text(args: SyntaxGraphArgs) -> str:
    node = args.ast_graph.nodes[args.n_id]
    source_id = node.get("label_field_source")
    if source_id:
        import_text = node_to_str(args.ast_graph, source_id)
    else:
        import_text = node_to_str(args.ast_graph, args.n_id)
    return import_text


def get_named_imports_attrs(graph: Graph, n_id: NId) -> Dict[str, str]:
    named_attrs: Dict[str, str] = {}
    for specifier_n_id in g.match_ast_group_d(graph, n_id, "import_specifier"):
        if (
            name_n_id := graph.nodes[specifier_n_id].get("label_field_name")
        ) and (identifier := graph.nodes[name_n_id].get("label_text")):
            named_attrs.update({"identifier": identifier})

        if (
            alias_n_id := graph.nodes[specifier_n_id].get("label_field_alias")
        ) and (alias := graph.nodes[alias_n_id].get("label_text")):
            named_attrs.update({"label_alias": alias})
    return named_attrs


def js_ts_reader(args: SyntaxGraphArgs) -> NId:
    graph: Graph = args.ast_graph
    node_attrs: Dict[str, str] = {
        "expression": import_label_text(args),
    }
    if import_clause_n_id := g.match_ast_d(graph, args.n_id, "import_clause"):
        if named_imports_n_id := g.match_ast_d(
            graph, import_clause_n_id, "named_imports"
        ):
            node_attrs.update(
                get_named_imports_attrs(graph, named_imports_n_id)
            )
        elif (
            identifier_n_id := g.match_ast_d(
                graph, import_clause_n_id, "identifier"
            )
        ) and (identifier := graph.nodes[identifier_n_id].get("label_text")):

            node_attrs.update({"identifier": identifier})

    return build_import_statement_node(args, node_attrs)
