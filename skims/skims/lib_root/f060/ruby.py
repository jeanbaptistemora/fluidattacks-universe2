from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def insecure_exceptions(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.RUBY,
        ):
            for rescue_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="rescue"),
            ):
                rescue_c_ids = g.adj_ast(shard.graph, rescue_id)
                if not any(
                    shard.graph.nodes[rescue_c_id]["label_type"] == "rescue"
                    for rescue_c_id in rescue_c_ids
                ):
                    # The grammar for `rescue` has another `rescue` as a child.
                    # We are only interested in the parent `rescue`
                    # because this one has the information about the exceptions
                    # so let's ignore the child `rescue`s
                    continue

                if exceptions_id := shard.graph.nodes[rescue_id].get(
                    "label_field_exceptions"
                ):
                    for exception_id in g.adj_ast(shard.graph, exceptions_id):
                        if shard.graph.nodes[exception_id]["label_text"] in {
                            "Exception",
                            "StandardError",
                        }:
                            yield shard, rescue_id
                else:
                    yield shard, rescue_id

    return get_vulnerabilities_from_n_ids(
        cwe=("396",),
        desc_key="src.lib_path.f060.insecure_exceptions.description",
        desc_params=dict(lang="Ruby"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F060
