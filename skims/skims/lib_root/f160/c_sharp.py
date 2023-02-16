from collections.abc import (
    Iterator,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNode,
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
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_CREATE_TEMP_FILE
    c_sharp = GraphShardMetadataLanguage.CSHARP
    danger_methods = complete_attrs_on_set({"System.IO.Path.GetTempFileName"})

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="MethodInvocation"):
                method_name = graph.nodes[nid].get("expression")
                if method_name in danger_methods:
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f160.c_sharp_file_create_temp_file.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
