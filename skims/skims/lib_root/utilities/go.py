# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    GraphDB,
    GraphShard,
    GraphShardMetadataLanguage,
    GraphShardNode,
    NId,
)
from typing import (
    Iterable,
    Iterator,
    Set,
)
from utils.graph import (
    filter_nodes,
    match_ast,
    pred_has_labels,
)


def yield_object_creation(
    graph_db: GraphDB, members: Set[str]
) -> Iterable[GraphShardNode]:
    for shard in graph_db.shards_by_language(
        GraphShardMetadataLanguage.GO,
    ):
        for member in yield_shard_object_creation(shard, members):
            yield shard, member


def yield_shard_object_creation(
    shard: GraphShard, members: Set[str]
) -> Iterator[NId]:
    for member in filter_nodes(
        shard.graph,
        nodes=shard.graph.nodes,
        predicate=pred_has_labels(label_type="selector_expression"),
    ):
        match = match_ast(shard.graph, member, "identifier")
        if (identifier := match["identifier"]) and shard.graph.nodes[
            identifier
        ]["label_text"] in members:
            yield member


def yield_member_access(
    graph_db: GraphDB, members: Set[str]
) -> Iterable[GraphShardNode]:
    for shard in graph_db.shards_by_language(
        GraphShardMetadataLanguage.GO,
    ):
        for member in yield_shard_member_access(shard, members):
            yield shard, member


def yield_shard_member_access(
    shard: GraphShard, members: Set[str]
) -> Iterator[NId]:
    for member in filter_nodes(
        shard.graph,
        nodes=shard.graph.nodes,
        predicate=pred_has_labels(label_type="selector_expression"),
    ):
        match = match_ast(shard.graph, member, "field_identifier")
        if (identifier := match["field_identifier"]) and shard.graph.nodes[
            identifier
        ]["label_text"] in members:
            yield member
