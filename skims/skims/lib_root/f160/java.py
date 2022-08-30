from lib_root.utilities.common import (
    search_method_invocation_naive,
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


def java_file_create_temp_file(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    danger_methods = complete_attrs_on_set({"java.io.File.createTempFile"})
    method = core_model.MethodsEnum.JAVA_CREATE_TEMP_FILE

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for method_id in search_method_invocation_naive(
                graph, danger_methods
            ):
                yield shard, method_id

    translation_key = (
        "src.lib_path.f160.java_file_create_temp_file.description"
    )
    return get_vulnerabilities_from_n_ids(
        desc_key=translation_key,
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
