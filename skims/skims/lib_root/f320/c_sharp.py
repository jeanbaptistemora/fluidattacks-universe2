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


def insecure_arg(depends: graph_model.SyntaxSteps) -> bool:
    for syntax_step in depends:
        if (
            isinstance(
                syntax_step, graph_model.SyntaxStepMemberAccessExpression
            )
            and syntax_step.expression == "AuthenticationTypes.None"
        ):
            return True
    return False


def ldap_connections_authenticated(
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
                            syntax_step,
                            graph_model.SyntaxStepObjectInstantiation,
                        )
                        and syntax_step.object_type == "DirectoryEntry"
                        and len(get_dependencies(index, syntax_steps)) > 0
                        and insecure_arg(get_dependencies(index, syntax_steps))
                    ):
                        yield shard, syntax_step.meta.n_id

    return get_vulnerabilities_from_n_ids(
        cwe=("90",),
        desc_key="F320.title",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F320
