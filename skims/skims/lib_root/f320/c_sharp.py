from model import (
    core_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
    SyntaxStepMemberAccessExpression,
    SyntaxStepObjectInstantiation,
    SyntaxSteps,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)


def _insecure_arg(dependencies: SyntaxSteps) -> bool:
    for step in dependencies:
        if (
            isinstance(step, SyntaxStepMemberAccessExpression)
            and step.expression == "AuthenticationTypes"
            and step.member == "None"
        ):
            return True
    return False


def ldap_connections_authenticated(
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            for steps in shard.syntax.values():
                for index, step in enumerate(steps):
                    if (
                        isinstance(step, SyntaxStepObjectInstantiation)
                        and step.object_type == "DirectoryEntry"
                        and _insecure_arg(get_dependencies(index, steps))
                    ):
                        yield shard, step.meta.n_id

    return get_vulnerabilities_from_n_ids(
        cwe=("90",),
        desc_key="lib_root.f320.authenticated_ldap_connections",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F320
