from collections.abc import (
    Iterator,
    Set,
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
    get_object_identifiers,
)
from utils import (
    graph as g,
)


def is_danger_value(graph: Graph, n_id: NId, memb_name: str) -> bool:
    method = MethodsEnum.CS_WEAK_CREDENTIAL
    insec_rules = {
        "RequireDigit": ["false"],
        "RequireNonAlphanumeric": ["false"],
        "RequireUppercase": ["false"],
        "RequireLowercase": ["false"],
        "RequiredLength": ["0", "1", "2", "3", "4", "5", "6", "7"],
        "RequiredUniqueChars": ["0", "1", "2", "3", "4", "5"],
    }
    if not insec_rules.get(memb_name):
        return False

    for path in get_backward_paths(graph, n_id):
        if (
            (evaluation := evaluate(method, graph, path, n_id))
            and (results := list(evaluation.triggers))
            and len(results) > 0
            and results[0] in insec_rules[memb_name]
        ):
            return True
    return False


def get_weak_policies_ids(graph: Graph, n_id: NId) -> set[NId]:
    weak_nodes: set[NId] = set()
    parent_id = g.pred(graph, n_id)[0]
    al_id = graph.nodes[parent_id].get("arguments_id")
    opt_id = g.match_ast(graph, al_id).get("__0__")
    if opt_id and graph.nodes[opt_id]["label_type"] == "LambdaExpression":
        block_id = graph.nodes[opt_id]["block_id"]
        config_options = g.adj_ast(graph, block_id)
        for assignment in config_options:
            arg_list = g.adj_ast(graph, assignment)
            if (
                len(arg_list) >= 2
                and (memb_n := graph.nodes[arg_list[0]])
                and "Password" in memb_n.get("expression")
                and (member := memb_n.get("member"))
                and is_danger_value(graph, arg_list[1], member)
            ):
                weak_nodes.add(arg_list[0])
    return weak_nodes


def get_vuln_nodes(graph: Graph) -> set[NId]:
    config_options = "Configure<IdentityOptions>"
    vuln_nodes: set[NId] = set()
    for nid in g.matching_nodes(graph, label_type="MemberAccess"):
        if graph.nodes[nid].get("member") != config_options:
            continue
        vuln_nodes.update(get_weak_policies_ids(graph, nid))
    return vuln_nodes


def check_no_password_argument(triggers: Set[str]) -> bool:
    eval_str = "".join(list(triggers))
    for arg_part in eval_str.split(";"):
        if "=" in arg_part:
            var, value = arg_part.split("=", maxsplit=1)
            if var == "Password" and not value:
                return True
    return False


def get_eval_danger(method: MethodsEnum, graph: Graph, n_id: NId) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and check_no_password_argument(evaluation.triggers):
            return True
    return False


# https://docs.microsoft.com/es-es/aspnet/core/security/authentication/identity-configuration
def weak_credential_policy(graph_db: GraphDB) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for res_nid in get_vuln_nodes(graph):
                yield shard, res_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f035.csharp_weak_credential_policy.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_WEAK_CREDENTIAL,
    )


def no_password(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_NO_PASSWORD
    bad_types = {"Microsoft", "EntityFrameworkCore", "DbContextOptionsBuilder"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            flagged_vars = get_object_identifiers(graph, bad_types)

            for n_id in g.matching_nodes(graph, label_type="MemberAccess"):
                expr = graph.nodes[n_id].get("expression")
                parent_id = g.pred(graph, n_id)[0]
                if (
                    expr in flagged_vars
                    and graph.nodes[n_id].get("member") == "UseSqlServer"
                    and (al_id := graph.nodes[parent_id].get("arguments_id"))
                    and (test_nid := g.match_ast(graph, al_id).get("__0__"))
                    and get_eval_danger(method, graph, test_nid)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f035.csharp_no_password.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
