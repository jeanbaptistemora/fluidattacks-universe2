from lib_root.utilities.javascript import (
    yield_method_invocation,
)
from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
    Vulnerability,
)
from model.graph_model import (
    GraphDB,
)
from sast.query import (
    shard_n_id_query,
)
from sast_transformations.danger_nodes.utils import (
    append_label_input,
    mark_methods_sink,
)
from typing import (
    Iterator,
)
from utils.string import (
    split_on_last_dot,
)


def weak_random(
    shard_db: ShardDb,
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_WEAK_RANDOM
    finding = method.value.finding

    def find_vulns() -> Iterator[Vulnerability]:
        random_number = False
        for (
            shard,
            _,
            invocation_step,
            __,
        ) in yield_method_invocation(graph_db):
            _, method_name = split_on_last_dot(invocation_step.method)
            if method_name == "random":
                random_number = True
                append_label_input(
                    shard.graph, invocation_step.meta.n_id, finding
                )
            elif random_number and method_name == "cookie":
                append_label_input(shard.graph, "1", finding)
                mark_methods_sink(
                    finding,
                    shard.graph,
                    shard.syntax,
                    {"cookie"},
                )
                yield from shard_n_id_query(
                    shard_db,
                    graph_db,
                    shard,
                    n_id="1",
                    method=method,
                )

    return tuple(find_vulns())
