from lib_root.utilities.c_sharp import (
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
                            dep.symbol
                            for dep in get_dependencies(index, syntax_steps)
                            if isinstance(
                                dep, graph_model.SyntaxStepSymbolLookup
                            )
                        )
                        if not secure_command(shard, dependencies):
                            yield shard, syntax_step.meta.n_id

    return get_vulnerabilities_from_n_ids(
        cwe=("89",),
        desc_key="F001.description",
        desc_params=dict(lang="C#"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def secure_command(shard: graph_model.GraphShard, dependencies: list) -> bool:

    secure_chars = ("@", "{", "}", "[(]", "[)]")

    secure_str = False
    for depend in dependencies:
        for elem in secure_chars:
            if get_variable_attribute(
                shard, depend, "type"
            ) == "binary_expression" and re.search(
                elem, get_variable_attribute(shard, depend, "text")
            ):
                secure_str = True
    return secure_str


FINDING: core_model.FindingEnum = core_model.FindingEnum.F001
