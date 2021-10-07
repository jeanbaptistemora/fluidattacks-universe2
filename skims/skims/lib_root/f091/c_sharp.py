from lib_root.utilities.common import (
    get_method_param_by_obj,
)
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


def insecure_attribute(
    shard: graph_model.GraphShard, object_name: str, n_id: str
) -> str:
    logging_methods = {
        "Info",
        "Log",
        "WriteLine",
        "WriteEntry",
        "TraceEvent",
        "Debug",
    }

    danger_param = get_method_param_by_obj(shard, n_id, "HttpRequest")

    for syntax_steps in shard.syntax.values():
        for index, syntax_step in enumerate(syntax_steps):
            if (
                isinstance(syntax_step, graph_model.SyntaxStepAssignment)
                and syntax_step.var == danger_param
            ):
                danger_param = ""
            if (
                isinstance(
                    syntax_step, graph_model.SyntaxStepMethodInvocationChain
                )
                and syntax_step.method in logging_methods
                and object_name
                in list(
                    dependencie.symbol
                    for dependencie in get_dependencies(index, syntax_steps)
                )
                and danger_param
                in list(
                    dependencie.symbol
                    for dependencie in get_dependencies(index, syntax_steps)
                )
            ):
                return syntax_step.meta.n_id
    return ""


def insecure_logging(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:

    object_methods = {
        "GetLogger",
        "GetCurrentClassLogger",
    }

    object_names = {
        "FileLogger",
        "DBLogger",
        "EventLogger",
        "EventLog",
        "StreamWriter",
        "TraceSource",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for syntax_steps in shard.syntax.values():
                for index, syntax_step in enumerate(syntax_steps):
                    member = ""
                    if (
                        isinstance(
                            syntax_step, graph_model.SyntaxStepDeclaration
                        )
                        and get_dependencies(index, syntax_steps)
                        and isinstance(
                            get_dependencies(index, syntax_steps)[0],
                            graph_model.SyntaxStepMethodInvocationChain,
                        )
                        and get_dependencies(index, syntax_steps)[0].method
                        in object_methods
                    ):
                        member = insecure_attribute(
                            shard, syntax_step.var, syntax_step.meta.n_id
                        )
                    elif (
                        isinstance(
                            syntax_step, graph_model.SyntaxStepDeclaration
                        )
                        and get_dependencies(index, syntax_steps)
                        and isinstance(
                            get_dependencies(index, syntax_steps)[0],
                            graph_model.SyntaxStepObjectInstantiation,
                        )
                        and get_dependencies(index, syntax_steps)[
                            0
                        ].object_type
                        in object_names
                    ):
                        member = insecure_attribute(
                            shard, syntax_step.var, syntax_step.meta.n_id
                        )
                    if len(member) > 0:
                        yield shard, member

    return get_vulnerabilities_from_n_ids(
        cwe=("502",),
        desc_key="F091.title",
        desc_params={},
        finding=core_model.FindingEnum.F091,
        graph_shard_nodes=n_ids(),
    )
