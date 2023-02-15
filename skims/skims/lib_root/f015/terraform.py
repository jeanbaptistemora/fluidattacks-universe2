from collections.abc import (
    Iterator,
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
from utils.graph import (
    adj_ast,
)


def _azure_linux_vm_insecure_authentication(
    graph: Graph, nid: NId
) -> NId | None:
    expected_block = "admin_ssh_key"
    if len(adj_ast(graph, nid, name=expected_block)) == 0:
        return nid
    return None


def _azure_virtual_machine_insecure_authentication(
    graph: Graph, nid: NId
) -> NId | None:
    expected_block = "os_profile_linux_config"
    expected_block_attr = "ssh_keys"
    for c_id in adj_ast(graph, nid, name=expected_block):
        if len(adj_ast(graph, c_id, 2, value=expected_block_attr)) == 0:
            return c_id
    return None


def tfm_azure_virtual_machine_insecure_authentication(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_VM_INSEC_AUTH

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "azurerm_virtual_machine"):
                if report := _azure_virtual_machine_insecure_authentication(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=(
            "lib_root.f015.tfm_azure_virtual_machine_insecure_authentication"
        ),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_linux_vm_insecure_authentication(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_LNX_VM_INSEC_AUTH

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(
                graph, "azurerm_linux_virtual_machine"
            ):
                if report := _azure_linux_vm_insecure_authentication(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("lib_root.f015.tfm_azure_linux_vm_insecure_authentication"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
