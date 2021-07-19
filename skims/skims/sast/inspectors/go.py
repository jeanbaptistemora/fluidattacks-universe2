from model.graph_model import (
    Graph,
    GraphShardMetadataGo,
    GraphShardMetadataLanguage,
    NId,
    SinkFunctions,
)
from typing import (
    Dict,
    List,
)
from utils import (
    graph as g,
)


def _get_sink_functions_metadata(
    graph: Graph,
) -> Dict[str, List[SinkFunctions]]:
    def _predicate(n_id: NId) -> bool:
        return g.pred_has_labels(label_type="function_declaration")(n_id)

    danger_functions_metadata: Dict[str, List[SinkFunctions]] = {}
    function_dcl_ids = g.filter_nodes(graph, graph.nodes, _predicate)
    for function_dcl_id in function_dcl_ids:
        function_name_id: str = g.get_ast_childs(
            graph, function_dcl_id, "identifier"
        )[0]
        function_name: str = graph.nodes[function_name_id]["label_text"]
        for c_id in g.adj_ast(graph, function_dcl_id, depth=-1):
            if finding_ids := graph.nodes[c_id].get("label_sink_type"):
                for finding_id in finding_ids:
                    if finding_id in danger_functions_metadata:
                        danger_functions_metadata[finding_id].append(
                            SinkFunctions(
                                name=function_name,
                                n_id=function_dcl_id,
                                s_id=c_id,
                            )
                        )
                    else:
                        danger_functions_metadata[finding_id] = [
                            SinkFunctions(
                                name=function_name,
                                n_id=function_dcl_id,
                                s_id=c_id,
                            )
                        ]
    return danger_functions_metadata


def _get_package_metadata(graph: Graph) -> str:
    package_name: str = ""
    match = g.match_ast(graph, g.ROOT_NODE, "package_clause")
    if pkg_clause_id := match["package_clause"]:
        pkg_id = g.get_ast_childs(graph, pkg_clause_id, "package_identifier")[
            0
        ]
        package_name = graph.nodes[pkg_id]["label_text"]
    return package_name


def get_metadata(
    graph: Graph, language: GraphShardMetadataLanguage
) -> GraphShardMetadataGo:
    if language != GraphShardMetadataLanguage.GO:
        return GraphShardMetadataGo(sink_functions={}, package="")

    return GraphShardMetadataGo(
        sink_functions=_get_sink_functions_metadata(graph),
        package=_get_package_metadata(graph),
    )
