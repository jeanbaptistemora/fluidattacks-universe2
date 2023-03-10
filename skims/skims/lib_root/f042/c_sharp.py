from collections.abc import (
    Iterator,
)
from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
    yield_syntax_graph_object_creation,
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
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def is_insecure_cookie_object(
    method: MethodsEnum, graph: Graph, object_nid: str
) -> NId | None:
    security_props = {"HttpOnly", "Secure"}
    pred = g.pred(graph, object_nid)[0]
    var_name = {graph.nodes[pred].get("variable")}

    sec_access = []
    for nid in yield_syntax_graph_member_access(graph, var_name):
        if graph.nodes[nid].get("member") not in security_props:
            continue
        parent_id = g.pred(graph, nid)[0]
        test_nid = graph.nodes[parent_id].get("value_id")
        sec_access.append(nid)
        if get_node_evaluation_results(method, graph, test_nid, set()):
            return pred

    if len(sec_access) < 2:
        return pred
    return None


def insecurely_generated_cookies(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_INSEC_COOKIES
    object_name = {"HttpCookie"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for object_nid in yield_syntax_graph_object_creation(
                graph, object_name
            ):
                if pred := is_insecure_cookie_object(
                    method, graph, object_nid
                ):
                    yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.042.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
