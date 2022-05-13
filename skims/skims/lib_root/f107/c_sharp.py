from lib_root.utilities.c_sharp import (
    yield_shard_object_creation,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
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


def ldap_injection(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_LDAP_INJECTION
    finding = method.value.finding
    csharp = GraphShardMetadataLanguage.CSHARP

    def n_ids() -> GraphShardNodes:

        for shard in graph_db.shards_by_language(csharp):
            if shard.syntax_graph is None:
                continue

            ldap_obj = {"DirectorySearcher"}

            for obj_id in yield_shard_object_creation(shard, ldap_obj):
                graph = shard.syntax_graph
                for path in get_backward_paths(graph, obj_id):
                    evaluation = evaluate(csharp, finding, graph, path, obj_id)
                    if evaluation and evaluation.danger:
                        yield shard, obj_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f107.ldap_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
