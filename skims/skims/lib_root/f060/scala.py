from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Set,
)
from utils import (
    graph as g,
)


def insecure_exceptions(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    insecure: Set[str] = {
        "Exception",
        "NullPointerException",
        "Throwable",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.SCALA,
        ):
            for case_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="case_clause"),
            ):
                pattern_id = shard.graph.nodes[case_id]["label_field_pattern"]
                pattern_n_attrs = shard.graph.nodes[pattern_id]

                if pattern_n_attrs["label_type"] == "typed_pattern":
                    type_id = pattern_n_attrs["label_field_type"]
                    if shard.graph.nodes[type_id]["label_text"] in insecure:
                        yield shard, pattern_id

    return get_vulnerabilities_from_n_ids(
        cwe=("396",),
        desc_key="src.lib_path.f060.insecure_exceptions.description",
        desc_params=dict(lang="Scala"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F060
