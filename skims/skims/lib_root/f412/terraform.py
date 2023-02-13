from lib_root.utilities.terraform import (
    get_key_value,
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
    Tuple,
)
from utils.graph import (
    adj_ast,
)


def get_attribute(
    graph: Graph, object_id: NId, expected_attr: str
) -> Tuple[Optional[str], str]:
    for attr_id in adj_ast(graph, object_id, label_type="Pair"):
        key, value = get_key_value(graph, attr_id)
        if key == expected_attr:
            return key, value
    return None, ""


def _azure_key_vault_not_recoverable(graph: Graph, nid: NId) -> Optional[NId]:
    soft_key, soft_val = get_attribute(graph, nid, "soft_delete_enabled")
    pur_key, pur_val = get_attribute(graph, nid, "purge_protection_enabled")
    if (
        not soft_key
        or soft_val.lower() == "false"
        or not pur_key
        or pur_val.lower() == "false"
    ):
        return nid
    return None


def tfm_azure_key_vault_not_recoverable(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_KEY_VAULT_NOT_RECOVER

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_key_vault"):
                if report := _azure_key_vault_not_recoverable(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f412.azure_key_vault_not_recoverable",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
