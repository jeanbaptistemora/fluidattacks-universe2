from itertools import (
    chain,
)
from lib_root.utilities.javascript import (
    yield_method_invocation,
)
from model.core_model import (
    FindingEnum,
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


def weak_random(graph_db: GraphDB) -> Vulnerabilities:
    def find_vulns() -> Iterator[Vulnerability]:
        random_number = False
        for (
            shard,
            _,
            invocation_step,
            __,
        ) in yield_method_invocation(graph_db):
            _, method = split_on_last_dot(invocation_step.method)
            if method == "random":
                random_number = True
                append_label_input(
                    shard.graph, invocation_step.meta.n_id, FINDING
                )
            elif random_number and method == "cookie":
                append_label_input(shard.graph, "1", FINDING)
                mark_methods_sink(
                    FINDING,
                    shard.graph,
                    shard.syntax,
                    {"cookie"},
                )
                yield shard_n_id_query(graph_db, FINDING, shard, "1")

    return tuple(chain.from_iterable(find_vulns()))


FINDING: FindingEnum = FindingEnum.F034
