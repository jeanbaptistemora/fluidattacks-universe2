from model import (
    core_model,
    graph_model,
)
from sast.parse import (
    parse_content,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def java_commented_code(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            for comment_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="comment"),
            ):
                code: str = shard.graph.nodes[comment_id]["label_text"]

                # remove // or /*
                if code.endswith("*/"):
                    code = code[2:-2]
                else:
                    code = code[2:]

                tree = parse_content(str.encode(code), shard.metadata.language)
                if not tree.root_node.has_error:
                    yield shard, comment_id

    return get_vulnerabilities_from_n_ids(
        cwe=("615",),
        desc_key="src.lib_path.f074.commented_code",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def csharp_commented_code(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for comment_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="comment"),
            ):
                code: str = shard.graph.nodes[comment_id]["label_text"]

                if code.endswith("*/"):
                    code = code[2:-2]
                else:
                    code = code[2:]

                tree = parse_content(str.encode(code), shard.metadata.language)
                if not tree.root_node.has_error:
                    yield shard, comment_id

    return get_vulnerabilities_from_n_ids(
        cwe=("615",),
        desc_key="src.lib_path.f074.commented_code",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F074
QUERIES: graph_model.Queries = (
    (FINDING, java_commented_code),
    (FINDING, csharp_commented_code),
)
