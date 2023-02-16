from collections.abc import (
    Iterator,
    Set,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
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
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
    split_on_last_dot as split_last,
)


def validate_import(graph: Graph, check: str) -> Iterator[str]:
    for node in g.matching_nodes(graph, label_type="Import"):
        form, _ = split_last(graph.nodes[node].get("expression"))
        yield form + "." + check


def is_secure(options: Iterator[str], pattern: Set[str]) -> bool:
    if any(library in pattern for library in options):
        return True
    return False


def is_method_danger(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.JAVA_CREATE_TEMP_FILE
    lib = {"java.nio.file.Files.createTempFile"}
    exp = graph.nodes[n_id].get("expression")

    if obj := graph.nodes[n_id].get("object_id"):
        imp_check = graph.nodes[obj].get("symbol") + "." + exp
    else:
        imp_check = exp

    lib_safe = is_secure(validate_import(graph, imp_check), lib)
    if not lib_safe:
        return True

    if lib_safe and (
        (al_id := graph.nodes[n_id].get("arguments_id"))
        and (test_nid := g.match_ast(graph, al_id).get("__1__"))
    ):
        for path in get_backward_paths(graph, test_nid):
            evaluation = evaluate(method, graph, path, test_nid)
            if evaluation and evaluation.danger:
                return True

    return False


def java_file_create_temp_file(
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_methods = complete_attrs_on_set({"java.io.File.createTempFile"})
    method = MethodsEnum.JAVA_CREATE_TEMP_FILE

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, danger_methods):
                if is_method_danger(graph, n_id):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f160.java_file_create_temp_file.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
