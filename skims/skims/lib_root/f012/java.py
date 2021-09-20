from model import (
    core_model,
    graph_model,
)
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
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


def _has_like_injection(statement: str) -> bool:
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


def jpa_like(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        danger_decorators = complete_attrs_on_set(
            {
                "org.springframework.data.jpa.repository.Query",
                "org.springframework.jdbc.object.SqlQuery",
            }
        )
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            graph = shard.graph

            for annotation_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="annotation"),
            ):

                match = g.match_ast(
                    graph,
                    annotation_id,
                    "annotation_argument_list",
                    "identifier",
                    "scoped_identifier",
                )
                if identifier_id := match.get("identifier") or (
                    identifier_id := match.get("scoped_identifier")
                ):
                    identifier_text = graph.nodes[identifier_id]["label_text"]
                if identifier_text not in danger_decorators:
                    continue

                for string_literal_id in g.filter_nodes(
                    graph,
                    nodes=g.adj_ast(graph, annotation_id, depth=-1),
                    predicate=g.pred_has_labels(label_type="string_literal"),
                ):
                    content = graph.nodes[string_literal_id]["label_text"]
                    if _has_like_injection(content):
                        yield shard, string_literal_id

    return get_vulnerabilities_from_n_ids(
        cwe=("89",),
        desc_key="src.lib_path.f001_jpa.java_like.description",
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F012
