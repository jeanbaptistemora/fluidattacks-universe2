from lib_root.utilities.c_sharp import (
    get_first_member_syntax_graph,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNodes,
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
from typing import (
    Iterator,
    List,
)
from utils import (
    graph as g,
)


def get_insecure_vars(graph: Graph) -> List[str]:
    object_names = {
        "CorsPolicyBuilder",
    }
    insecure_vars = []
    for nid in g.filter_nodes(
        graph,
        graph.nodes,
        g.pred_has_labels(label_type="ObjectCreation"),
    ):
        if (
            graph.nodes[nid].get("label_type") == "ObjectCreation"
            and graph.nodes[nid].get("name") in object_names
        ):
            var_nid = g.pred_ast(graph, nid)[0]
            if graph.nodes[var_nid].get("label_type") == "VariableDeclaration":
                insecure_vars.append(graph.nodes[var_nid].get("variable"))
    return insecure_vars


def get_cors_vars(graph: Graph) -> Iterator[NId]:
    for obj_id in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(label_type="ObjectCreation"),
    ):
        if "CorsPolicy" in graph.nodes[obj_id].get("name").split("."):
            invocation = g.pred_ast(graph, obj_id)[0]
            yield graph.nodes[invocation].get("variable")


def insecure_cors(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP
    danger_methods = {"AllowAnyOrigin"}
    object_methods = {
        "UseCors",
    }

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            insecure_vars = get_insecure_vars(graph)
            for nid in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="MemberAccess"),
            ):
                if (
                    graph.nodes[nid].get("member") in danger_methods
                    and graph.nodes[nid].get("expression").split(".")[0]
                    in insecure_vars
                ):
                    yield shard, nid
                elif graph.nodes[nid].get("member") in object_methods:
                    al_id = graph.nodes[g.pred(graph, nid)[0]].get(
                        "arguments_id"
                    )
                    arg_nid = g.match_ast(graph, al_id).get("__0__")
                    label_t = graph.nodes[arg_nid].get("label_type")
                    if (
                        arg_nid
                        and label_t == "MemberAccess"
                        and graph.nodes[arg_nid].get("member") == "AllowAll"
                    ):
                        yield shard, nid
                    elif (
                        arg_nid
                        and label_t == "LambdaExpression"
                        and (method_id := g.adj_ast(graph, arg_nid)[1])
                        and "AllowAnyOrigin"
                        in graph.nodes[method_id].get("expression").split(".")
                    ):
                        yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_INSECURE_CORS,
    )


def insecure_cors_origin(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_INSECURE_CORS_ORIGIN

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            cors_objects = list(get_cors_vars(graph))
            for member in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MemberAccess"),
            ):
                expr = graph.nodes[member].get("expression")
                memb = graph.nodes[member].get("member")
                if (
                    "Origins.Add" in f"{expr}.{memb}"
                    and (
                        fr_member := get_first_member_syntax_graph(
                            graph, member
                        )
                    )
                    and graph.nodes[fr_member].get("label_type")
                    == "SymbolLookup"
                    and graph.nodes[fr_member].get("symbol") in cors_objects
                ):
                    pred_nid = g.pred_ast(graph, member)[0]
                    for path in get_backward_paths(graph, pred_nid):
                        if (
                            evaluation := evaluate(
                                method, graph, path, pred_nid
                            )
                        ) and evaluation.danger:
                            yield shard, pred_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
