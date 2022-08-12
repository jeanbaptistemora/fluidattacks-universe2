from lib_root.utilities.c_sharp import (
    yield_syntax_graph_object_creation,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
from model.core_model import (
    MethodsEnum,
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


def check_hashes_salt(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP
    method = MethodsEnum.CS_CHECK_HASHES_SALT

    directory_object = {"Rfc2898DeriveBytes"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in yield_syntax_graph_object_creation(
                graph, directory_object
            ):
                for path in get_backward_paths(graph, member):
                    evaluation = evaluate(method, graph, path, member)
                    if evaluation and evaluation.danger:
                        yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.338.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
