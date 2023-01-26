# Future
from __future__ import (
    annotations,
)

from enum import (
    Enum,
)
from model import (
    core_model,
)
import networkx as nx
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

NAttrs = Dict[str, str]
NAttrsPredicateFunction = Callable[[NAttrs], bool]
NId = str
NIdPredicateFunction = Callable[[str], bool]
GraphSyntax = Dict[str, str]


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
    TYPESCRIPT: str = "tsx"
    YAML: str = "yaml"


class GraphShardMetadata(NamedTuple):
    language: GraphShardMetadataLanguage


class GraphShardCacheable(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    syntax: GraphSyntax
    syntax_graph: Optional[Graph]


class GraphShard(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    path: str
    syntax: GraphSyntax
    syntax_graph: Optional[Graph]


class GraphDB(NamedTuple):
    context: Dict[str, str]
    shards: List[GraphShard]
    shards_by_language_class: Dict[str, Dict[str, str]]
    shards_by_path: Dict[str, int]

    def shards_by_path_f(self, path: str) -> GraphShard:
        return self.shards[self.shards_by_path[path]]

    def shards_by_language(
        self,
        language: GraphShardMetadataLanguage,
    ) -> List[GraphShard]:
        return [
            shard
            for shard in self.shards
            if shard.metadata.language == language
        ]


MetadataGraphShardNode = Tuple[GraphShard, NId, Dict]
MetadataGraphShardNodes = Iterable[MetadataGraphShardNode]
GraphShardNode = Tuple[GraphShard, NId]
GraphShardNodes = Iterable[GraphShardNode]

Query = Callable[[GraphDB], core_model.Vulnerabilities]
Queries = Tuple[Tuple[core_model.FindingEnum, Query], ...]
