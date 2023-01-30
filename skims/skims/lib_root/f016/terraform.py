from lib_root.utilities.json import (
    get_value,
)
from lib_root.utilities.terraform import (
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
from typing import (
    Iterable,
    Optional,
)
from utils.graph import (
    adj_ast,
)


def _azure_serves_content_over_insecure_protocols(
    graph: Graph, nid: NId
) -> Optional[NId]:
    expected_attr = "min_tls_version"
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key_id = graph.nodes[c_id]["key_id"]
        key = graph.nodes[key_id]["value"]
        value_id = graph.nodes[c_id]["value_id"]
        value = get_value(graph, value_id)
        if key == expected_attr:
            if value in ("TLS1_0", "TLS1_1"):
                return c_id
            return None
    return nid


def tfm_azure_serves_content_over_insecure_protocols(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_INSEC_PROTO

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_storage_account"):
                if report := _azure_serves_content_over_insecure_protocols(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("src.lib_path.f016.serves_content_over_insecure_protocols"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
