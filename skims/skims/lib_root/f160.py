from lib_root import (
    yield_c_sharp_invocation_expression,
    yield_java_method_invocation,
)
from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils.string import (
    complete_attrs_on_set,
)


def java_file_create_temp_file(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        danger_methods = complete_attrs_on_set({"java.io.File.createTempFile"})
        for shard, method_id, method_name in yield_java_method_invocation(
            graph_db
        ):
            if method_name in danger_methods:
                yield shard, method_id

    translation_key = (
        "src.lib_path.f160.java_file_create_temp_file.description"
    )
    return get_vulnerabilities_from_n_ids(
        cwe=("378",),
        desc_key=translation_key,
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def c_sharp_file_create_temp_file(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        danger_methods = complete_attrs_on_set(
            {"System.IO.Path.GetTempFileName"}
        )
        for (
            shard,
            method_id,
            method_name,
        ) in yield_c_sharp_invocation_expression(graph_db):
            if method_name in danger_methods:
                yield shard, method_id

    translation_key = (
        "src.lib_path.f160.c_sharp_file_create_temp_file.description"
    )
    return get_vulnerabilities_from_n_ids(
        cwe=("378",),
        desc_key=translation_key,
        desc_params=dict(lang="C#"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F160
QUERIES: graph_model.Queries = (
    (FINDING, java_file_create_temp_file),
    (FINDING, c_sharp_file_create_temp_file),
)
