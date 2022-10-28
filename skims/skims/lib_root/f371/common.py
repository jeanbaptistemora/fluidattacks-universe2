# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
from model.graph_model import (
    GraphShard,
    GraphShardNode,
)
from typing import (
    Iterable,
)


def has_innerhtml(shard: GraphShard) -> Iterable[GraphShardNode]:
    if shard.syntax_graph is not None:
        graph = shard.syntax_graph
        for nid in yield_syntax_graph_member_access(graph, {"innerHTML"}):
            yield shard, nid
