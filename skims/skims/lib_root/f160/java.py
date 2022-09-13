# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
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
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)


def java_file_create_temp_file(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    danger_methods = complete_attrs_on_set({"java.io.File.createTempFile"})
    method = core_model.MethodsEnum.JAVA_CREATE_TEMP_FILE

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, danger_methods):
                if (al_id := graph.nodes[n_id].get("arguments_id")) and (
                    test_nid := g.match_ast(graph, al_id).get("__1__")
                ):
                    for path in get_backward_paths(graph, test_nid):
                        evaluation = evaluate(method, graph, path, test_nid)
                        if evaluation and evaluation.danger:
                            yield shard, n_id

    translation_key = (
        "src.lib_path.f160.java_file_create_temp_file.description"
    )
    return get_vulnerabilities_from_n_ids(
        desc_key=translation_key,
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
