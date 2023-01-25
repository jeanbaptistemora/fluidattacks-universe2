from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
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
from typing import (
    Iterable,
    Optional,
)
from utils import (
    graph as g,
)


def get_regex_node(graph: Graph, expr: str) -> Optional[NId]:
    if regex_name := expr.split(".")[0]:
        for vid in g.matching_nodes(graph, label_type="VariableDeclaration"):
            if graph.nodes[vid].get("variable") == regex_name:
                return vid
    return None


def sets_timespan(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_VULN_REGEX
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and "hastimespan" in evaluation.triggers:
            return True
    return False


def is_pattern_danger(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_VULN_REGEX
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and "safepattern" not in evaluation.triggers
        ):
            return True
    return False


def is_node_danger(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_VULN_REGEX
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers == {
            "userparams",
            "userconnection",
        }:
            return True
    return False


def is_regex_vuln(graph: Graph, n_id: NId) -> bool:
    obj_c = g.match_ast(graph, n_id, "ObjectCreation").get("ObjectCreation")
    if (
        obj_c
        and graph.nodes[obj_c].get("name") == "Regex"
        and (al_id := g.get_ast_childs(graph, obj_c, "ArgumentList")[0])
    ):
        args_nids = g.adj_ast(graph, al_id)
        regpat_nid = args_nids[0]
        is_danger_pattern = is_pattern_danger(graph, regpat_nid)
        has_timespan = False
        if len(args_nids) == 3:
            timespan_nid = args_nids[2]
            has_timespan = sets_timespan(graph, timespan_nid)

        return is_danger_pattern and not has_timespan

    return False


def analyze_method_vuln(graph: Graph, method_id: NId) -> bool:
    method_n = graph.nodes[method_id]
    expr = method_n.get("expression")
    args_id = g.get_ast_childs(graph, method_id, "ArgumentList")
    args_nids = g.adj_ast(graph, args_id[0])

    if len(args_nids) == 0 or not is_node_danger(graph, args_nids[0]):
        return False

    if len(args_nids) == 1:
        is_danger_method = True
    elif len(args_nids) >= 2:
        regpat_nid = args_nids[1]
        is_danger_method = is_pattern_danger(graph, regpat_nid)

    if len(args_nids) == 4:
        timespan_nid = args_nids[3]
        is_danger_method = not sets_timespan(graph, timespan_nid)

    if (
        is_danger_method
        and (regex_node := get_regex_node(graph, expr))
        and is_regex_vuln(graph, regex_node)
    ):
        return True

    return False


def eval_regex_injection(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_REGEX_INJETCION
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def vuln_regular_expression(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_VULN_REGEX
    c_sharp = GraphLanguage.CSHARP
    regex_methods = {"IsMatch", "Match", "Matches"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="MemberAccess"):
                method_id = g.pred_ast(graph, nid)[0]
                if graph.nodes[nid].get(
                    "member"
                ) in regex_methods and analyze_method_vuln(graph, method_id):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_vulnerable",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def regex_injection(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_REGEX_INJETCION
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in yield_syntax_graph_member_access(graph, {"Regex"}):
                pred = g.pred_ast(graph, member)[0]
                if graph.nodes[member][
                    "member"
                ] == "Match" and eval_regex_injection(graph, pred):
                    yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
