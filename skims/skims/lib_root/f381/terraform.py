from collections.abc import (
    Iterator,
)
from lib_root.utilities.terraform import (
    get_attribute,
    iterate_resource,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def _check_required_version(graph: Graph, nid: NId) -> NId | None:
    attr, _, _ = get_attribute(graph, nid, "required_version")
    if not attr:
        return nid
    return None


def tfm_check_required_version(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CHECK_REQUIRED_VERSION

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "terraform"):
                if report := _check_required_version(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f381.tfm_check_required_version",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
