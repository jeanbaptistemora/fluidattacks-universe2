from collections.abc import (
    Iterator,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def get_eval_danger(
    graph: Graph, n_ids: list[NId], method: MethodsEnum
) -> bool:
    for _id in n_ids:
        if graph.nodes[_id]["argument_name"] != "resolve_entities":
            continue
        val_id = graph.nodes[_id]["value_id"]
        for path in get_backward_paths(graph, val_id):
            evaluation = evaluate(method, graph, path, val_id)
            if evaluation and evaluation.danger:
                return True
    return False


def is_xml_parser_vuln(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    al_id = g.match_ast_d(graph, n_id, "ArgumentList")
    if al_id and (
        not (args := g.match_ast_group_d(graph, al_id, "NamedArgument"))
        or get_eval_danger(graph, args, method)
    ):
        return True
    return False


def python_xml_parser(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_XML_PARSER

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.PYTHON,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                if graph.nodes[n_id][
                    "expression"
                ] == "etree.XMLParser" and is_xml_parser_vuln(
                    graph, n_id, method
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f083.generic_xml_parser",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
