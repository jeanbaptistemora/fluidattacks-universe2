from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def conflicting_annotations(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        critical = False
        for shard in graph_db.shards:
            for _class in shard.metadata.c_sharp.classes.values():
                if (
                    _class.attributes
                    and "SecurityCritical" in _class.attributes
                ):
                    critical = True
                for _method in _class.methods.values():
                    if (
                        _method.attributes
                        and critical
                        and "SecuritySafeCritical" in _method.attributes
                    ):
                        yield shard, _method.n_id

    return get_vulnerabilities_from_n_ids(
        cwe=("749",),
        desc_key="F366.title",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F366
