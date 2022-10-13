# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from itertools import (
    chain,
)
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
from typing import (
    Iterable,
    List,
)
from utils import (
    graph as g,
)


def get_insecure_vars(graph: Graph) -> List[str]:
    object_names = {"CorsPolicyBuilder"}
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


def is_insecure_use_cors(graph: Graph, nid: NId) -> bool:
    al_id = graph.nodes[g.pred(graph, nid)[0]].get("arguments_id")
    arg_nid = g.match_ast(graph, al_id).get("__0__")
    if not arg_nid:
        return False

    node_type = graph.nodes[arg_nid]["label_type"]
    if (
        node_type == "MemberAccess"
        and graph.nodes[arg_nid].get("member") == "AllowAll"
    ) or (
        node_type == "LambdaExpression"
        and (method_id := g.adj_ast(graph, arg_nid)[1])
        and "AllowAnyOrigin"
        in graph.nodes[method_id].get("expression").split(".")
    ):
        return True

    return False


def get_eval_danger(
    graph: Graph,
    n_id: NId,
    check: str = "danger",
) -> bool:
    method = core_model.MethodsEnum.CS_INSECURE_CORS_ORIGIN
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if not evaluation:
            continue
        if check == "danger" and evaluation.danger:
            return True
        if check == "triggers" and evaluation.triggers == {"CorsObject"}:
            return True
    return False


def is_vulnerable_enable_attribute(graph: Graph, n_id: NId, name: str) -> bool:
    if name.lower() != "enablecors":
        return False

    al_id = g.match_ast(graph, n_id, "ArgumentList").get("ArgumentList")
    if not al_id:
        return False
    al_list = g.adj_ast(graph, al_id)

    for arg in al_list:
        node = graph.nodes[arg]
        if (
            node["label_type"] == "NamedArgument"
            and (var := graph.nodes[node["variable_id"]].get("symbol"))
            and var.lower() == "origins"
        ):
            test_node = node["value_id"]
            if get_eval_danger(graph, test_node):
                return True

    return False


def is_vulnerable_policy(graph: Graph, n_id: NId) -> bool:
    if (
        (al_id := graph.nodes[n_id].get("arguments_id"))
        and (al_list := g.adj_ast(graph, al_id))
        and len(al_list) >= 2
        and graph.nodes[al_list[1]]["label_type"] == "LambdaExpression"
    ):
        if block_id := graph.nodes[al_list[1]].get("block_id"):
            m_id = g.match_ast(graph, block_id).get("__0__")
        elif (lambda_childs := g.adj_ast(graph, al_list[1])) and len(
            lambda_childs
        ) == 2:
            m_id = lambda_childs[1]
        else:
            return False
        expr = graph.nodes[m_id].get("expression")
        if "AllowAnyOrigin" in expr:
            return True
    return False


def is_vulnerable_origin(graph: Graph, nid: NId, expr: str) -> bool:
    if "addpolicy" in expr.lower() and is_vulnerable_policy(graph, nid):
        return True

    if (
        "origins.add" in expr.lower()
        and (fr_m := get_first_member_syntax_graph(graph, nid))
        and get_eval_danger(graph, fr_m, "triggers")
        and (arg_id := graph.nodes[nid].get("arguments_id"))
    ):
        childs = g.adj_ast(graph, arg_id)
        if len(childs) > 0 and get_eval_danger(graph, childs[0]):
            return True

    return False


def insecure_cors(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
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
                    graph.nodes[nid].get("member") == "AllowAnyOrigin"
                    and graph.nodes[nid].get("expression").split(".")[0]
                    in insecure_vars
                ) or (
                    graph.nodes[nid].get("member") == "UseCors"
                    and is_insecure_use_cors(graph, nid)
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_INSECURE_CORS,
    )


def insecure_cors_origin(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_INSECURE_CORS_ORIGIN

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                g.filter_nodes(
                    graph,
                    graph.nodes,
                    g.pred_has_labels(label_type="MethodInvocation"),
                ),
                g.filter_nodes(
                    graph,
                    graph.nodes,
                    g.pred_has_labels(label_type="Attribute"),
                ),
            ):
                expr = graph.nodes[nid].get("expression")
                name = graph.nodes[nid].get("name")

                if (
                    name and is_vulnerable_enable_attribute(graph, nid, name)
                ) or (expr and is_vulnerable_origin(graph, nid, expr)):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
