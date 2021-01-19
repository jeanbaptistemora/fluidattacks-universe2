# Future
from __future__ import (
    annotations,
)

# Standard library
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
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
SyntaxStepsLazy = Iterator[SyntaxStep]


@dataclass
class SyntaxStepMeta:
    danger: bool
    dependencies: Any
    sink: Optional[str]
    value: Optional[Any]

    @staticmethod
    def default(
        dependencies: Optional[List[SyntaxSteps]] = None,
    ) -> SyntaxStepMeta:
        return SyntaxStepMeta(
            danger=False,
            dependencies=dependencies or [],
            sink=None,
            value=None,
        )

    def linear(self) -> bool:
        return isinstance(self.dependencies, int)


class SyntaxStepBinaryExpression(NamedTuple):
    operator: str
    meta: SyntaxStepMeta

    type: str = 'SyntaxStepBinaryExpression'


class SyntaxStepDeclaration(NamedTuple):
    meta: SyntaxStepMeta
    var: str
    var_type: str

    type: str = 'SyntaxStepDeclaration'


class SyntaxStepMethodInvocation(NamedTuple):
    meta: SyntaxStepMeta
    method: str

    type: str = 'SyntaxStepMethodInvocation'


class SyntaxStepNoOp(NamedTuple):
    meta: SyntaxStepMeta

    type: str = 'SyntaxStepNoOp'


class SyntaxStepObjectInstantiation(NamedTuple):
    meta: SyntaxStepMeta
    object_type: str

    type: str = 'SyntaxStepObjectInstantiation'


class SyntaxStepStringLiteral(NamedTuple):
    meta: SyntaxStepMeta
    value: str

    type: str = 'SyntaxStepStringLiteral'


class SyntaxStepSymbolLookup(NamedTuple):
    meta: SyntaxStepMeta
    symbol: str

    type: str = 'SyntaxStepSymbolLookup'


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


class GraphShardMetadataNodes(NamedTuple):
    in_cfg: Tuple[NId, ...]


class GraphShardMetadataLanguage(Enum):
    JAVA: str = 'java'
    NOT_SUPPORTED: str = 'not_supported'


class GraphShardMetadata(NamedTuple):
    java: Optional[GraphShardMetadataJava]
    language: GraphShardMetadataLanguage
    nodes: Optional[GraphShardMetadataNodes]


class GraphShardCacheable(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    syntax: GraphSyntax


class GraphShard(NamedTuple):
    graph: Graph
    metadata: GraphShardMetadata
    path: str
    syntax: GraphSyntax


class GraphUntrustedNode(Enum):
    F034_INSECURE_RANDOM: str = 'F034_INSECURE_RANDOM'
    F063_PATH_TRAVERSAL: str = 'F063_PATH_TRAVERSAL'


class GraphDangerousActionNode(Enum):
    F034_INSECURE_RANDOM: str = 'F034_INSECURE_RANDOM'
    F063_PATH_TRAVERSAL: str = 'F063_PATH_TRAVERSAL'


class GraphDB(NamedTuple):
    shards: List[GraphShard]
    shards_by_path: Dict[str, int]


GraphShardNode = Tuple[GraphShard, NId]
GraphShardNodes = Iterable[GraphShardNode]

Query = Callable[[Graph], core_model.Vulnerabilities]
Queries = Tuple[Query, ...]
