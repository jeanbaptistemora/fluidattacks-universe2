from collections.abc import (
    Iterator,
)
from lib_root.f021.common import (
    insecure_dynamic_xpath,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def ts_dynamic_xpath(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_DYNAMIC_X_PATH

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in insecure_dynamic_xpath(graph, method):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f021.xpath_injection_evaluate",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
