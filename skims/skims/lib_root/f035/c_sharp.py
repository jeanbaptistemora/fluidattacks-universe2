from itertools import (
    chain,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
from model.graph_model import (
    GraphShardMetadataLanguage as GraphLanguage,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
    shard_n_id_query,
)
from sast_transformations.danger_nodes.utils import (
    append_label,
    mark_assignments_sink,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
    get_object_identifiers,
)
from typing import (
    Iterator,
)
from utils import (
    graph as g,
)


# https://docs.microsoft.com/es-es/aspnet/core/security/authentication/identity-configuration
def weak_credential_policy(
    shard_db: ShardDb,
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_WEAK_CREDENTIAL
    finding = method.value.finding

    def find_vulns() -> Iterator[core_model.Vulnerabilities]:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for syntax_steps in shard.syntax.values():
                if len(syntax_steps) == 0:  # handle missing syntax case
                    continue

                *dependecies, invocation_step = syntax_steps
                if (
                    invocation_step.type != "SyntaxStepMethodInvocationChain"
                    or invocation_step.method != "Configure<IdentityOptions>"
                ):
                    continue

                *_, first_param = dependecies
                if first_param.type != "SyntaxStepLambdaExpression":
                    continue

                param_syntax, *_ = shard.syntax[first_param.meta.n_id]
                param_id = param_syntax.meta.n_id

                input_type = "label_input_type"
                param_syntax.meta.danger = True
                append_label(shard.graph, param_id, input_type, finding)

                mark_assignments_sink(
                    finding,
                    shard.graph,
                    shard.syntax,
                    {
                        "RequireDigit",
                        "RequiredLength",
                        "RequireNonAlphanumeric",
                        "RequireUppercase",
                        "RequireLowercase",
                        "RequiredUniqueChars",
                    },
                )

                yield shard_n_id_query(
                    shard_db,
                    graph_db,
                    shard,
                    param_id,
                    method=method,
                )

    return tuple(chain.from_iterable(find_vulns()))


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
                        if evaluation and evaluation.danger:
                            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f035.csharp_no_password.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_NO_PASSWORD,
    )
