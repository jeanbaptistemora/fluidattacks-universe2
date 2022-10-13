# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_sast.types import (
    ShardDb,
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
from typing import (
    Iterable,
    List,
    Set,
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


def check_no_password_argument(triggers: Set[str]) -> bool:
    eval_str = "".join(list(triggers))
    for arg_part in eval_str.split(";"):
        if "=" in arg_part:
            var, value = arg_part.split("=", maxsplit=1)
            if var == "Password" and not value:
                return True
    return False


def get_weak_policies_ids(graph: Graph, n_id: NId) -> List[NId]:
    weak_nodes = []
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
                weak_nodes.append(arg_list[0])
    return weak_nodes


def get_eval_danger(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_NO_PASSWORD
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and check_no_password_argument(evaluation.triggers):
            return True
    return False


# https://docs.microsoft.com/es-es/aspnet/core/security/authentication/identity-configuration
def weak_credential_policy(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    config_options = "Configure<IdentityOptions>"

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="MemberAccess"),
            ):
                if graph.nodes[nid].get("member") != config_options:
                    continue

                weak_policies_ids = get_weak_policies_ids(graph, nid)
                for res_nid in weak_policies_ids:
                    yield shard, res_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f035.csharp_weak_credential_policy.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_WEAK_CREDENTIAL,
    )


def no_password(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_NO_PASSWORD
    c_sharp = GraphLanguage.CSHARP
    bad_types = {"Microsoft", "EntityFrameworkCore", "DbContextOptionsBuilder"}

    def n_ids() -> Iterable[GraphShardNode]:
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
                parent_id = g.pred(graph, n_id)[0]

                if (
                    expr in flagged_vars
                    and member == "UseSqlServer"
                    and (al_id := graph.nodes[parent_id].get("arguments_id"))
                    and (test_nid := g.match_ast(graph, al_id).get("__0__"))
                    and get_eval_danger(graph, test_nid)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f035.csharp_no_password.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
