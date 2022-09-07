# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Set,
    Tuple,
)

Frame = Dict[str, str]  # {type: node_type, next_id: n_id}
Stack = List[Frame]


CFG_ARGS = Any


class CfgArgs(NamedTuple):
    generic: Callable[[CFG_ARGS, Stack], None]
    graph: Graph
    n_id: str
    language: GraphShardMetadataLanguage

    def fork_n_id(self, n_id: str) -> CFG_ARGS:
        return CfgArgs(
            generic=self.generic,
            graph=self.graph,
            n_id=n_id,
            language=self.language,
        )


CfgBuilder = Callable[[CfgArgs, Stack], None]


class Walker(NamedTuple):
    applicable_node_label_types: Set[str]
    walk_fun: CfgBuilder


Walkers = Tuple[Walker, ...]
