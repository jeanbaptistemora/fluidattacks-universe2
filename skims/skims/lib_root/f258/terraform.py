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


def _elb2_has_not_deletion_protection(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "enable_deletion_protection"
    )
    if not attr:
        return nid
    if attr_val.lower() in {"false", "0"}:
        return attr_id
    return None


def tfm_elb2_has_not_deletion_protection(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ELB2_NOT_DELETION_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_lb"):
                if report := _elb2_has_not_deletion_protection(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f258.elb2_has_not_deletion_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
