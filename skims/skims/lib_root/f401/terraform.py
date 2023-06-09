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


def _azure_kv_secret_no_expiration_date(graph: Graph, nid: NId) -> NId | None:
    attr, _, _ = get_attribute(graph, nid, "expiration_date")
    if not attr:
        return nid
    return None


def tfm_azure_kv_secret_no_expiration_date(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_KV_SECRET_NO_EXPIRATION

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_key_vault_secret"):
                if report := _azure_kv_secret_no_expiration_date(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f401.has_not_expiration_date_set",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
