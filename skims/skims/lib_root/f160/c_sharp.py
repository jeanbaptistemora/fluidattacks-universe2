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
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)


def c_sharp_file_create_temp_file(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_CREATE_TEMP_FILE
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP

    def n_ids() -> graph_model.GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            graph = shard.syntax_graph
            danger_methods = complete_attrs_on_set(
                {"System.IO.Path.GetTempFileName"}
            )
            for nid in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MethodInvocation"),
            ):
                method_name = graph.nodes[nid].get("expression")
                if method_name in danger_methods:
                    yield shard, nid

    translation_key = (
        "src.lib_path.f160.c_sharp_file_create_temp_file.description"
    )
    return get_vulnerabilities_from_n_ids(
        desc_key=translation_key,
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
