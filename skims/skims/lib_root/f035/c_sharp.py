from itertools import (
    chain,
)
from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
    shard_n_id_query,
)
from sast_transformations.danger_nodes.utils import (
    append_label,
    mark_assignments_sink,
)
from typing import (
    Iterator,
    Optional,
)


# https://docs.microsoft.com/es-es/aspnet/core/security/authentication/identity-configuration
def weak_credential_policy(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
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


def _get_var_decl(
    var_step: graph_model.SyntaxStepSymbolLookup,
    syntax_steps: graph_model.SyntaxSteps,
) -> Optional[graph_model.SyntaxStep]:
    for step in reversed(syntax_steps):
        if isinstance(step, graph_model.SyntaxStepDeclaration):
            if step.var == var_step.symbol:
                return step
    return None


def _get_var_val(
    var_step: graph_model.SyntaxStepSymbolLookup,
    syntax_steps: graph_model.SyntaxSteps,
) -> Optional[graph_model.SyntaxStep]:
    return_next = False
    for syntax_step in reversed(syntax_steps):
        if isinstance(syntax_step, graph_model.SyntaxStepAssignment):
            if syntax_step.var == var_step.symbol:
                return_next = True
        elif return_next:
            return syntax_step
    return None


def _check_no_password_argument(arg: graph_model.SyntaxStepLiteral) -> bool:
    if arg.value_type == "string":
        for arg_part in arg.value.split(";"):
            if "=" in arg_part:
                var, value = arg_part.split("=", maxsplit=1)
                if var == "Password" and not value:
                    return True
    return False


def no_password(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        bad_types = [
            "Microsoft",
            "EntityFrameworkCore",
            "DbContextOptionsBuilder",
        ]

        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            all_syntax_steps = []
            for syntax_steps in shard.syntax.values():
                if len(syntax_steps) == 0:  # handle missing syntax case
                    continue

                all_syntax_steps.extend(syntax_steps)

                *dependencies, step = syntax_steps

                if (
                    step.type != "SyntaxStepMethodInvocationChain"
                    or step.method != "UseSqlServer"
                ):
                    continue

                var_step, *arguments = dependencies
                var_decl = _get_var_decl(var_step, all_syntax_steps)

                if not var_decl or var_decl.var_type not in bad_types:
                    continue

                for arg in arguments:
                    if isinstance(
                        arg, graph_model.SyntaxStepSymbolLookup
                    ) and not (arg := _get_var_val(arg, all_syntax_steps)):
                        continue

                    if _check_no_password_argument(arg):
                        yield shard, arg.meta.n_id

    return get_vulnerabilities_from_n_ids(
        cwe=("521",),
        desc_key="src.lib_root.f035.csharp_no_password.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F035
