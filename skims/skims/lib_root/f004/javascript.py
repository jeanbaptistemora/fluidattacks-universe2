from collections.abc import (
    Iterator,
)
from lib_root.f004.common import (
    remote_command_exec_nodes,
)
from model import (
    core_model,
    graph_model,
)
from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def remote_command_execution(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    javascript = GraphLanguage.JAVASCRIPT
    method = MethodsEnum.JS_REMOTE_COMMAND_EXECUTION

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(javascript):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in remote_command_exec_nodes(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
