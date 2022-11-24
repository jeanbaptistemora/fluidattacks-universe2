from lib_root.utilities.c_sharp import (
    yield_syntax_graph_object_creation,
)
from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    Iterable,
)


def is_object_danger(graph: Graph, nid: NId) -> bool:
    method = MethodsEnum.CS_LDAP_INJECTION
    for path in get_backward_paths(graph, nid):
        evaluation = evaluate(method, graph, path, nid)
        if evaluation and evaluation.danger:
            return True
    return False


def ldap_injection(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_LDAP_INJECTION
    csharp = GraphShardMetadataLanguage.CSHARP
    ldap_obj = {"DirectorySearcher"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(csharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for obj_id in yield_syntax_graph_object_creation(graph, ldap_obj):
                if is_object_danger(graph, obj_id):
                    yield shard, obj_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f107.ldap_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
