from ._utils import (
    map_over_children,
)
from .dag import (
    DAG,
)
from fa_purity import (
    FrozenList,
    Maybe,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
import grimp
from typing import (
    Any,
    FrozenSet,
)


def _check_dag(graph: Any, module: str) -> None:
    _children: FrozenSet[str] = frozenset(graph.find_children(module))
    children = (
        from_flist(tuple(_children))
        .map(lambda s: s.removeprefix(module + "."))
        .transform(lambda x: frozenset(x))
    )
    dag_modules: FrozenSet[str] = (
        Maybe.from_optional(DAG.get(module))
        .map(lambda l: frozenset(l))
        .value_or(frozenset([]))
    )
    missing = children - dag_modules
    if missing:
        raise Exception(
            f"Missing children modules of {module} at DAG i.e. {missing}"
        )
    dag_struct: FrozenList[str] = (
        Maybe.from_optional(DAG.get(module))
        .map(lambda t: tuple(module + "." + x for x in t))
        .value_or(tuple())
    )
    for n, a in enumerate(dag_struct):
        for i in dag_struct[n + 1 :]:
            if graph.chain_exists(i, a, True):
                raise Exception(f"Broken DAG with illegal import {i} -> {a}")

    return None


def test_dag() -> None:
    root = "target_s3"
    graph = grimp.build_graph(root)
    _check_dag(graph, root)
