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
import re
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
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)

# Constants
WS = r"\s*"
SEP = f"{WS},{WS}"


def has_like_injection(statement: str) -> bool:
    roots = (
        # like %x
        r"like\s+%{}",
        # like x%
        r"like\s+{}%",
        # like %x%
        r"like\s+%{}%",
        # like concat('%',   x)
        rf"like\s+concat\('%'{SEP}{{}}\)",
        # like concat(x,  '%')
        rf"like\s+concat\({{}}{SEP}'%'\)",
        # like concat('%',   x,'%')
        rf"like\s+concat\('%'{SEP}{{}}{SEP}'%'\)",
    )
    variables = (
        # :#{[0]}
        r":\#\{\[\d+\]\}",
        # :lastname
        r":[a-z0-9_\$]+",
        # ?0
        r"\?\d+",
    )
    statement = statement.lower()

    for var in variables:
        for root in roots:
            if re.search(root.format(var), statement):
                return True
    return False


def is_argument_vuln(
    graph: Graph,
    n_id: NId,
) -> bool:
    method = MethodsEnum.JAVA_JPA_LIKE
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and has_like_injection(
            "".join(list(evaluation.triggers))
        ):
            return True
    return False


def analyze_jpa_node(graph: Graph, annotation_id: str) -> bool:
    _, *c_ids = g.adj_ast(graph, annotation_id, depth=2)
    results_vuln = []
    for n_id in c_ids:
        results_vuln.append(is_argument_vuln(graph, n_id))

    if any(results_vuln):
        m_id = g.pred_ast(graph, annotation_id, depth=2)[1]
        pm_id = g.adj_ast(graph, m_id, label_type="ParameterList")[0]
        annotations = g.adj_ast(graph, pm_id, depth=3, label_type="Annotation")
        if not any(
            graph.nodes[annotation]["name"] == "Bind"
            for annotation in annotations
        ):
            return True
    return False


def jpa_like(
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_decorators = complete_attrs_on_set(
        {
            "org.springframework.data.jpa.repository.Query",
            "org.springframework.jdbc.object.SqlQuery",
        }
    )

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVA):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for annotation_id in g.matching_nodes(
                graph,
                label_type="Annotation",
            ):
                identifier_text = graph.nodes[annotation_id]["name"]
                if identifier_text in danger_decorators and analyze_jpa_node(
                    graph, annotation_id
                ):
                    yield shard, annotation_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f001_jpa.java_like.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_JPA_LIKE,
    )
