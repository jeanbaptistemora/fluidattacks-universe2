from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)


def insecure_props(shard: graph_model.GraphShard, name_var: str) -> bool:
    security_props = {
        "HttpOnly",
        "Secure",
    }

    count_checks = 0
    for syntax_steps in shard.syntax.values():
        for index, syntax_step in enumerate(syntax_steps):
            if (
                isinstance(syntax_step, graph_model.SyntaxStepAssignment)
                and syntax_step.var.split(".")[0] == name_var
                and syntax_step.var.split(".")[1] in security_props
                and len(get_dependencies(index, syntax_steps)) > 0
                and isinstance(
                    get_dependencies(index, syntax_steps)[0],
                    graph_model.SyntaxStepLiteral,
                )
            ):
                if get_dependencies(index, syntax_steps)[0].value == "true":
                    count_checks += 1
                elif get_dependencies(index, syntax_steps)[0].value == "false":
                    return True
    if count_checks > 1:
        return False
    return True


def insecurely_generated_cookies(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for syntax_steps in shard.syntax.values():
                for index, syntax_step in enumerate(syntax_steps):
                    if (
                        isinstance(
                            syntax_step, graph_model.SyntaxStepDeclaration
                        )
                        and len(get_dependencies(index, syntax_steps)) > 0
                        and isinstance(
                            get_dependencies(index, syntax_steps)[0],
                            graph_model.SyntaxStepObjectInstantiation,
                        )
                        and get_dependencies(index, syntax_steps)[
                            0
                        ].object_type
                        == "HttpCookie"
                        and insecure_props(shard, syntax_step.var)
                    ):
                        yield shard, syntax_step.meta.n_id

    return get_vulnerabilities_from_n_ids(
        cwe=("614",),
        desc_key="F042.description",
        desc_params=dict(lang="C#"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F042
