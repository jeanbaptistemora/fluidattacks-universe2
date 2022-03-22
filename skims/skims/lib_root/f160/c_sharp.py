from lib_root.utilities.c_sharp import (
    yield_invocation_expression,
)
from lib_sast.types import (
    ShardDb,
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


def c_sharp_file_create_temp_file(
    shard_db: ShardDb,  # pylint: disable=unused-argument
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
        ) in yield_invocation_expression(graph_db):
            if method_name in danger_methods:
                yield shard, method_id

    translation_key = (
        "src.lib_path.f160.c_sharp_file_create_temp_file.description"
    )
    return get_vulnerabilities_from_n_ids(
        desc_key=translation_key,
        desc_params=dict(lang="C#"),
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_CREATE_TEMP_FILE,
    )
