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
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Union,
)

NAttrs = Dict[str, str]
NAttrsPredicateFunction = Callable[[NAttrs], bool]
NId = str
NIdPredicateFunction = Callable[[str], bool]

ShardDb = Any

SyntaxStep = Any
SyntaxSteps = List[SyntaxStep]
SyntaxStepsLazy = Iterator[SyntaxStep]


class CurrentInstance(NamedTuple):
    fields: Dict[str, Any] = {}


class Graph(nx.DiGraph):
    pass


GraphSyntax = Dict[NId, SyntaxSteps]


class GraphShardMetadataClassField(NamedTuple):
    n_id: NId
    var: str
    var_type: str
    static: bool = False


class GraphShardMetadataParameter(NamedTuple):
    n_id: NId
    name: str
    type_name: str
    attributes: Optional[List[str]] = None


class GraphShardMetadataClassMethod(NamedTuple):
    n_id: NId
    class_name: Optional[str] = None
    name: Optional[str] = None
    parameters: Optional[Dict[str, GraphShardMetadataParameter]] = None
    return_type: Optional[str] = None
    static: bool = False
    attributes: Optional[List[str]] = None


class GraphShardMetadataClass(NamedTuple):
    fields: Dict[str, GraphShardMetadataClassField]
    methods: Dict[str, GraphShardMetadataClassMethod]
    n_id: NId
    attributes: Optional[List[str]] = None
    inherit: Optional[Union[Set[str], str]] = None


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


class GraphVulnerabilityParameters(NamedTuple):
    desc_key: str
    desc_params: Dict[str, str]


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
