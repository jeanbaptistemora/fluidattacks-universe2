# Future
from __future__ import (
    annotations,
)

from collections.abc import (
    Callable,
    Iterable,
)
from enum import (
    Enum,
)
from model import (
    core_model,
)
import networkx as nx
from typing import (
    NamedTuple,
)

NAttrs = dict[str, str]
NAttrsPredicateFunction = Callable[[NAttrs], bool]
NId = str
NIdPredicateFunction = Callable[[str], bool]
GraphSyntax = dict[str, str]


class Graph(nx.DiGraph):
    pass


class GraphShardMetadataLanguage(Enum):
    CSHARP: str = "c_sharp"
    DART: str = "dart"
    GO: str = "go"
    HCL: str = "hcl"
    JAVA: str = "java"
    JAVASCRIPT: str = "javascript"
    JSON: str = "json"
    KOTLIN: str = "kotlin"
    NOT_SUPPORTED: str = "not_supported"
    PHP: str = "php"
    PYTHON: str = "python"
    RUBY: str = "ruby"
    SCALA: str = "scala"
    SWIFT: str = "swift"
    TYPESCRIPT: str = "tsx"
    YAML: str = "yaml"


class GraphShardMetadata(NamedTuple):
    language: GraphShardMetadataLanguage


class GraphShardCacheable(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    syntax: GraphSyntax
    syntax_graph: Graph | None


class GraphShard(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    path: str
    syntax: GraphSyntax
    syntax_graph: Graph | None


class GraphDB(NamedTuple):
    context: dict[str, str]
    shards: list[GraphShard]
    shards_by_language_class: dict[str, dict[str, str]]
    shards_by_path: dict[str, int]

    def shards_by_path_f(self, path: str) -> GraphShard:
        return self.shards[self.shards_by_path[path]]

    def shards_by_language(
        self,
        language: GraphShardMetadataLanguage,
    ) -> list[GraphShard]:
        return [
            shard
            for shard in self.shards
            if shard.metadata.language == language
        ]


MetadataGraphShardNode = tuple[GraphShard, NId, dict]
MetadataGraphShardNodes = Iterable[MetadataGraphShardNode]
GraphShardNode = tuple[GraphShard, NId]
GraphShardNodes = Iterable[GraphShardNode]

Query = Callable[[GraphDB], core_model.Vulnerabilities]
Queries = tuple[tuple[core_model.FindingEnum, Query], ...]
