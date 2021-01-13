# Standard library
from enum import (
    Enum,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

# Third party libraries
import networkx as nx

# Local libraries
from model import (
    core_model,
)


NAttrs = Dict[str, str]
NAttrsPredicateFunction = Callable[[NAttrs], bool]
NId = str
NIdPredicateFunction = Callable[[str], bool]

SyntaxStep = Any
SyntaxSteps = List[SyntaxStep]


class Graph(nx.DiGraph):
    pass


GraphSyntax = Dict[NId, SyntaxSteps]


class GraphShardMetadataJavaClassMethod(NamedTuple):
    n_id: NId


class GraphShardMetadataJavaClass(NamedTuple):
    methods: Dict[str, GraphShardMetadataJavaClassMethod]
    n_id: NId


class GraphShardMetadataJava(NamedTuple):
    classes: Dict[str, GraphShardMetadataJavaClass]
    package: str


class GraphShardMetadataLanguage(Enum):
    JAVA: str = 'java'
    NOT_SUPPORTED: str = 'not_supported'


class GraphShardMetadata(NamedTuple):
    java: Optional[GraphShardMetadataJava]
    language: GraphShardMetadataLanguage


class GraphShardCacheable(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    syntax: GraphSyntax


class GraphShard(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    path: str
    syntax: GraphSyntax


class GraphDB(NamedTuple):
    shards: List[GraphShard]
    shards_by_path: Dict[str, int]


Query = Callable[[Graph], core_model.Vulnerabilities]
Queries = Tuple[Query, ...]
