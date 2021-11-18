from model import (
    core_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
    SyntaxStep,
    SyntaxStepLambdaExpression,
    SyntaxStepMemberAccessExpression,
    SyntaxStepMethodInvocationChain,
    SyntaxStepObjectInstantiation,
    SyntaxSteps,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from sast_symbolic_evaluation.utils_generic import (
    get_dependencies_from_nid,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from typing import (
    Optional,
)
from utils.string import (
    split_on_last_dot,
)


def insecure_cors(
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> GraphShardNodes:
        cors_objects = []
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            for steps in shard.syntax.values():
                for index, step in enumerate(steps):
                    dependencies = get_dependencies(index, steps)
                    if (
                        dependencies
                        and isinstance(
                            dependencies[0], SyntaxStepObjectInstantiation
                        )
                        and dependencies[0].object_type == "CorsPolicyBuilder"
                    ):
                        cors_objects.append(step.var)
                    if (
                        isinstance(step, SyntaxStepMethodInvocationChain)
                        and step.method == "UseCors"
                        and dependencies
                        and isinstance(
                            dependencies[0], SyntaxStepLambdaExpression
                        )
                    ):
                        cors_objects.append(
                            get_dependencies_from_nid(
                                steps, dependencies[0].meta.n_id
                            )[0].var
                        )
                    if allow_all(step, dependencies):
                        yield shard, step.meta.n_id
                    if vuln_nid := allow_any_origin(step, cors_objects):
                        yield shard, vuln_nid

    return get_vulnerabilities_from_n_ids(
        cwe=("16",),
        desc_key="F134.title",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def allow_any_origin(step: SyntaxStep, cors_objects: list) -> Optional[str]:
    if (
        isinstance(step, SyntaxStepMethodInvocationChain)
        and step.method == "AllowAnyOrigin"
        and list(
            elem for elem in step.expression.split(".") if elem in cors_objects
        )
    ):
        return step.meta.n_id
    return None


def allow_all(step: SyntaxStep, dependencies: SyntaxSteps) -> bool:
    if not dependencies:
        return False
    if (
        isinstance(step, SyntaxStepMethodInvocationChain)
        and step.method == "UseCors"
        and isinstance(dependencies[0], SyntaxStepMemberAccessExpression)
        and dependencies[0].member == "AllowAll"
        and split_on_last_dot(dependencies[0].expression)[1] == "CorsOptions"
    ):
        return True
    return False


FINDING: core_model.FindingEnum = core_model.FindingEnum.F134
