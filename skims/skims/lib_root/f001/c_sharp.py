from lib_root.utilities.c_sharp import (
    get_object_argument_list,
    get_variable_attribute,
)
from model import (
    core_model,
    graph_model,
)
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)


def sql_injection(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:

        danger_methods = {"ExecuteSqlCommand"}
        danger_objects = {"SqlCommand"}

        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for syntax_steps in shard.syntax.values():
                for index, syntax_step in enumerate(syntax_steps):
                    if (
                        isinstance(
                            syntax_step,
                            graph_model.SyntaxStepMethodInvocationChain,
                        )
                        and syntax_step.method in danger_methods
                    ) or (
                        isinstance(
                            syntax_step,
                            graph_model.SyntaxStepObjectInstantiation,
                        )
                        and syntax_step.object_type in danger_objects
                    ):
                        dependencies = list(
                            dep
                            for dep in get_dependencies(index, syntax_steps)
                            if isinstance(
                                dep,
                                (
                                    graph_model.SyntaxStepSymbolLookup,
                                    graph_model.SyntaxStepBinaryExpression,
                                ),
                            )
                        )
                        if not secure_command(
                            shard, dependencies, syntax_step.meta.n_id
                        ):
                            yield shard, syntax_step.meta.n_id

    return get_vulnerabilities_from_n_ids(
        cwe=("89",),
        desc_key="F001.description",
        desc_params=dict(lang="C#"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def secure_command(
    shard: graph_model.GraphShard, dependencies: list, elem_id: str
) -> bool:

    if not dependencies:
        return True

    secure_chars = ("@", "{", "}", "[(]", "[)]")

    for depend in dependencies:
        if isinstance(depend, graph_model.SyntaxStepSymbolLookup):
            is_var = True
            depend = depend.symbol
            sql_str = get_variable_attribute(shard, depend, "text")
        elif isinstance(depend, graph_model.SyntaxStepBinaryExpression):
            is_var = False
            sql_str = get_object_argument_list(shard, elem_id)
        for elem in secure_chars:
            if (
                not sql_str or re.search(elem, sql_str) or " " not in sql_str
            ) or (
                is_var
                and get_variable_attribute(shard, depend, "type")
                != "binary_expression"
            ):
                return True

    return False


FINDING: core_model.FindingEnum = core_model.FindingEnum.F001
