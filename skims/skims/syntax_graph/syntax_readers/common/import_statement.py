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
    List,
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


def get_namespace_import(
    graph: Graph, n_id: NId, library_name: str
) -> Dict[str, str]:
    node_attrs: Dict[str, str] = {}
    if (identifier_n_id := g.match_ast_d(graph, n_id, "identifier")) and (
        identifier := graph.nodes[identifier_n_id].get("label_text")
    ):
        node_attrs.update(
            {
                "expression": library_name,
                "identifier": identifier,
                "import_type": "namespace_import",
            }
        )
    return node_attrs


def get_named_imports_attrs(
    graph: Graph, n_id: NId, library_name: str
) -> List[Dict[str, str]]:
    named_imports: List[Dict[str, str]] = []
    for specifier_n_id in g.match_ast_group_d(graph, n_id, "import_specifier"):
        n_attrs: Dict[str, str] = {
            "expression": library_name,
            "import_type": "named_import",
        }
        if (
            name_n_id := graph.nodes[specifier_n_id].get("label_field_name")
        ) and (identifier := graph.nodes[name_n_id].get("label_text")):
            n_attrs.update({"identifier": identifier})

        if (
            alias_n_id := graph.nodes[specifier_n_id].get("label_field_alias")
        ) and (alias := graph.nodes[alias_n_id].get("label_text")):
            n_attrs.update({"label_alias": alias})
        named_imports.append(n_attrs)
    return named_imports


def get_default_export(
    graph: Graph, n_id: NId, library_name: str
) -> Dict[str, str]:
    node_attrs: Dict[str, str] = {}
    if identifier := graph.nodes[n_id].get("label_text"):
        node_attrs.update(
            {
                "expression": library_name,
                "identifier": identifier,
                "import_type": "default_import",
            }
        )
    return node_attrs


def js_ts_reader(args: SyntaxGraphArgs) -> NId:
    graph: Graph = args.ast_graph
    library_name = import_label_text(args)
    node_attrs: Dict[str, str] = {"expression": library_name}

    if import_clause_n_id := g.match_ast_d(graph, args.n_id, "import_clause"):
        if identifier_n_id := g.match_ast_d(
            graph, import_clause_n_id, "identifier"
        ):
            node_attrs = get_default_export(
                graph, identifier_n_id, library_name
            )

        if namespace_import_n_id := g.match_ast_d(
            graph, import_clause_n_id, "namespace_import"
        ):
            node_attrs = get_namespace_import(
                graph, namespace_import_n_id, library_name
            )

        if named_imports_n_id := g.match_ast_d(
            graph, import_clause_n_id, "named_imports"
        ):
            node_attrs = get_named_imports_attrs(
                graph, named_imports_n_id, library_name
            )[-1]

    return build_import_statement_node(args, node_attrs)
