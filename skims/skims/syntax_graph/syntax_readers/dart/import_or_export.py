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
from utils import (
    graph as g,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def get_expression(graph: Graph, n_id: NId, args_n_id: NId) -> str:
    if (
        library_nodes := g.get_nodes_by_path(
            graph, n_id, [], "configurable_uri", "uri", "string_literal"
        )
    ) and (name_n_id := next(iter(library_nodes), None)):
        expression = graph.nodes[name_n_id].get("label_text")
    else:
        expression = node_to_str(graph, args_n_id)
    return expression


def get_alias(graph: Graph, n_id: NId) -> str | None:
    if (alias_node := g.match_ast_d(graph, n_id, "identifier")) and (
        alias := graph.nodes[alias_node].get("label_text")
    ):
        return alias
    return None


def reader(args: SyntaxGraphArgs) -> NId:
    graph: Graph = args.ast_graph
    node_attrs: dict[str, str] = {}

    for n_id in g.match_ast_group_d(
        graph, args.n_id, "import_specification", depth=-1
    ):
        expression = get_expression(graph, n_id, args.n_id)
        node_attrs.update({"expression": expression})
        if alias := get_alias(graph, n_id):
            node_attrs.update({"label_alias": alias})

    return build_import_statement_node(args, node_attrs)
