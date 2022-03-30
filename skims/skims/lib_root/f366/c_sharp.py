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


def conflicting_annotations(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        critical = False
        for shard in graph_db.shards:
            for _class in (
                shard.metadata.c_sharp.classes.values()
                if shard.metadata.c_sharp
                else []
            ):
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
        desc_key="lib_root.f366.conflicting_transparency_annotations",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_CONFLICTING_ANNOTATIONS,
    )
