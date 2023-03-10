from collections.abc import (
    Iterable,
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
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_object_identifiers,
)
from utils import (
    graph as g,
)


def is_insecure_decoder(
    method: MethodsEnum,
    graph: Graph,
    n_id: str,
    obj_identifiers: Iterable[str],
) -> bool:
    exp = graph.nodes[n_id]["expression"]
    memb = graph.nodes[n_id]["member"]
    if (
        exp in obj_identifiers
        and memb == "Decode"
        and (al_id := graph.nodes[g.pred(graph, n_id)[0]].get("arguments_id"))
        and (test_nid := g.match_ast(graph, al_id).get("__2__"))
        and get_node_evaluation_results(method, graph, test_nid, set())
    ):
        return True
    return False


def check_pred(graph: Graph, depth: int = 1, elem_jwt: str = "0") -> bool:
    pred = g.pred(graph, elem_jwt, depth)[0]
    if (
        graph.nodes[pred].get("label_type") == "MemberAccess"
        and graph.nodes[pred].get("member") == "MustVerifySignature"
    ):
        return True
    if graph.nodes[pred].get("label_type") != "VariableDeclaration":
        signed = check_pred(graph, depth + 1, pred)
    else:
        return False
    return signed


def verify_decoder(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_VERIFY_DECODER

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            obj_jwt = get_object_identifiers(graph, {"JwtDecoder"})
            for member in g.matching_nodes(graph, label_type="MemberAccess"):
                if is_insecure_decoder(method, graph, member, obj_jwt):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.017.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def jwt_signed(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_JWT_SIGNED
    object_name = {"JwtBuilder"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in [
                *yield_syntax_graph_member_access(graph, object_name),
                *yield_syntax_graph_object_creation(graph, object_name),
            ]:
                if not check_pred(graph, elem_jwt=member):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.017.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
