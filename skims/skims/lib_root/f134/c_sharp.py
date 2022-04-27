from lib_root.utilities.c_sharp import (
    get_first_member,
    get_object_identifiers,
)
from lib_sast.types import (
    ShardDb,
)
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
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    Optional,
)
from utils import (
    graph as g,
)
from utils.graph.text_nodes import (
    node_to_str,
)
from utils.string import (
    split_on_last_dot,
)


def insecure_cors(
    shard_db: ShardDb,  # pylint: disable=unused-argument
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
                        nid_dependencies = get_dependencies_from_nid(
                            steps, dependencies[0].meta.n_id
                        )
                        if nid_dependencies:
                            cors_objects.append(nid_dependencies[0].var)
                    if allow_all(step, dependencies):
                        yield shard, step.meta.n_id
                    if vuln_nid := allow_any_origin(step, cors_objects):
                        yield shard, vuln_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_INSECURE_CORS,
    )


def allow_any_origin(step: SyntaxStep, cors_objects: list) -> Optional[str]:
    if (
        isinstance(step, SyntaxStepMethodInvocationChain)
        and step.method == "AllowAnyOrigin"
        and list(
            elem
            for elem in str(step.expression).split(".")
            if elem in cors_objects
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


def insecure_cors_origin(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_INSECURE_CORS_ORIGIN
    finding = method.value.finding
    c_sharp = GraphShardMetadataLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue

            cors_objects = get_object_identifiers(
                shard, graph_db, {"CorsPolicy"}
            )
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="member_access_expression"
                ),
            ):
                if (
                    "Origins.Add" in node_to_str(shard.graph, member)
                    and (fr_member := get_first_member(shard, member))
                    and shard.graph.nodes[fr_member]["label_type"]
                    == "identifier"
                    and shard.graph.nodes[fr_member]["label_text"]
                    in cors_objects
                ):
                    pred_nid = g.pred_ast(shard.graph, member)[0]
                    graph = shard.syntax_graph
                    for path in get_backward_paths(graph, pred_nid):
                        if evaluate(c_sharp, finding, graph, path, pred_nid):
                            yield shard, pred_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
