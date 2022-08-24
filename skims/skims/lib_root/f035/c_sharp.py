from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
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
from typing import (
    Set,
)
from utils import (
    graph as g,
)


def is_danger_value(graph: Graph, n_id: NId, memb_name: str) -> bool:
    method = core_model.MethodsEnum.CS_WEAK_CREDENTIAL
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


def check_no_password_argument(triggers: Set[str]) -> bool:
    eval_str = "".join(reversed(list(triggers)))
    for arg_part in eval_str.split(";"):
        if "=" in arg_part:
            var, value = arg_part.split("=", maxsplit=1)
            if var == "Password" and not value:
                return True
    return False


# https://docs.microsoft.com/es-es/aspnet/core/security/authentication/identity-configuration
def weak_credential_policy(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    object_type = {"Configure<IdentityOptions>"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="MemberAccess"),
            ):
                if not graph.nodes[nid].get("member") in object_type:
                    continue

                al_id = graph.nodes[g.pred(graph, nid)[0]].get("arguments_id")
                opt_id = g.match_ast(graph, al_id).get("__0__")
                if (
                    opt_id
                    and graph.nodes[opt_id].get("label_type")
                    == "LambdaExpression"
                    and (block_id := g.adj_ast(graph, opt_id)[1])
                ):
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
                            yield shard, arg_list[0]

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f035.csharp_weak_credential_policy.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_WEAK_CREDENTIAL,
    )


def no_password(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_NO_PASSWORD
    c_sharp = GraphLanguage.CSHARP

    bad_types = {"Microsoft", "EntityFrameworkCore", "DbContextOptionsBuilder"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            flagged_vars = get_object_identifiers(graph, bad_types)

            for n_id in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="MemberAccess"),
            ):
                expr = graph.nodes[n_id].get("expression")
                member = graph.nodes[n_id].get("member")
                if (
                    expr in flagged_vars
                    and member == "UseSqlServer"
                    and (
                        al_id := graph.nodes[g.pred(graph, n_id)[0]].get(
                            "arguments_id"
                        )
                    )
                    and (test_nid := g.match_ast(graph, al_id).get("__0__"))
                ):
                    for path in get_backward_paths(graph, test_nid):
                        evaluation = evaluate(method, graph, path, test_nid)
                        if evaluation and check_no_password_argument(
                            evaluation.triggers
                        ):
                            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f035.csharp_no_password.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_NO_PASSWORD,
    )
