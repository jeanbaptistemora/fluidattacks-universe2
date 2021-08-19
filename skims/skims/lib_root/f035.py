from itertools import (
    chain,
)
from model import (
    core_model,
    graph_model,
)
from sast.query import (
    shard_n_id_query,
)
from sast_transformations.danger_nodes.utils import (
    append_label,
    mark_assignments_sink,
)
from typing import (
    Iterator,
)


# https://docs.microsoft.com/es-es/aspnet/core/security/authentication/identity-configuration
def csharp_weak_credential_policy(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def find_vulns() -> Iterator[core_model.Vulnerabilities]:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for syntax_steps in shard.syntax.values():
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
                append_label(shard.graph, param_id, input_type, FINDING)

                mark_assignments_sink(
                    FINDING,
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

                yield shard_n_id_query(graph_db, FINDING, shard, param_id)

    return tuple(chain.from_iterable(find_vulns()))


FINDING: core_model.FindingEnum = core_model.FindingEnum.F035
QUERIES: graph_model.Queries = ((FINDING, csharp_weak_credential_policy),)
