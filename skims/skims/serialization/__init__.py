from lark import (
    Tree as LarkTree,
)
from lark.tree import (
    Meta as LarkMeta,
)
from metaloaders.model import (
    Node,
    Type,
)
from model import (
    core_model,
    cvss3_model,
    graph_model,
)
from parse_common.types import (
    ListToken,
)
from parse_hcl2.tokens import (
    Attribute as HCL2Attribute,
    Block as HCL2Block,
    Json as HCL2Json,
)
import safe_pickle
from safe_pickle import (
    dump,
    load,
)
from typing import (
    Any,
)
from utils.graph import (
    export_graph_as_json,
    import_graph_from_json,
)


def _dump_graph(instance: graph_model.Graph) -> safe_pickle.Serialized:
    graph_as_json = export_graph_as_json(instance, include_styles=True)
    return safe_pickle.serialize(instance, graph_as_json)


def _load_graph(graph_as_json: Any) -> graph_model.Graph:
    return import_graph_from_json(graph_as_json)


def _dump_lark_meta(meta: LarkMeta) -> safe_pickle.Serialized:
    return safe_pickle.serialize(
        meta,
        *map(
            safe_pickle.dump_raw,
            {
                attr: getattr(meta, attr, None)
                for attr in (
                    "column",
                    "empty",
                    "end_column",
                    "end_line",
                    "line",
                )
            },
        ),
    )


def _load_lark_meta(**kwargs: Any) -> LarkMeta:
    meta = LarkMeta()
    for attr, value in kwargs.items():
        if value is not None:
            setattr(meta, attr, value)
    return meta


def _dump_lark_tree(tree: LarkTree) -> safe_pickle.Serialized:
    return safe_pickle.serialize(
        tree,
        *map(
            safe_pickle.dump_raw,
            (
                tree.children,
                tree.data,
                tree.meta,
            ),
        ),
    )


def _load_lark_tree(children: Any, data: Any, meta: Any) -> LarkTree:
    return LarkTree(data, children, meta)


def _side_effects() -> None:
    for factory in (
        core_model.FindingEnum,
        core_model.Grammar,
        core_model.Platform,
        core_model.VulnerabilityKindEnum,
        core_model.VulnerabilitySourceEnum,
        core_model.VulnerabilityVerificationStateEnum,
        core_model.VulnerabilityStateEnum,
        cvss3_model.AttackComplexity,
        cvss3_model.AttackVector,
        cvss3_model.AvailabilityImpact,
        cvss3_model.ConfidentialityImpact,
        cvss3_model.Exploitability,
        cvss3_model.IntegrityImpact,
        cvss3_model.PrivilegesRequired,
        cvss3_model.RemediationLevel,
        cvss3_model.ReportConfidence,
        cvss3_model.SeverityScope,
        cvss3_model.SeverityScope,
        cvss3_model.UserInteraction,
        graph_model.GraphShardMetadataLanguage,
        Type,
    ):
        safe_pickle.register_enum(factory)

    for factory in (
        core_model.FindingMetadata,
        core_model.IntegratesVulnerabilityMetadata,
        core_model.NVDVulnerability,
        core_model.SkimsVulnerabilityMetadata,
        core_model.Vulnerability,
        core_model.VulnerabilityVerification,
        cvss3_model.Score,
        HCL2Attribute,
        HCL2Block,
        HCL2Json,
        graph_model.GraphDB,
        graph_model.GraphShardCacheable,
        graph_model.GraphShard,
        graph_model.GraphShardMetadata,
        graph_model.GraphShardMetadataCSharp,
        graph_model.GraphShardMetadataJava,
        graph_model.GraphShardMetadataClass,
        graph_model.GraphShardMetadataClassField,
        graph_model.GraphShardMetadataClassMethod,
        graph_model.GraphVulnerabilityParameters,
        graph_model.SyntaxStepArrayAccess,
        graph_model.SyntaxStepArrayInstantiation,
        graph_model.SyntaxStepArrayInitialization,
        graph_model.SyntaxStepAssignment,
        graph_model.SyntaxStepBinaryExpression,
        graph_model.SyntaxStepCastExpression,
        graph_model.SyntaxStepInstanceofExpression,
        graph_model.SyntaxStepCatchClause,
        graph_model.SyntaxStepDeclaration,
        graph_model.SyntaxStepIf,
        graph_model.SyntaxStepLoop,
        graph_model.SyntaxStepLiteral,
        graph_model.SyntaxStepMethodInvocation,
        graph_model.SyntaxStepMethodInvocationChain,
        graph_model.SyntaxStepNoOp,
        graph_model.SyntaxStepObjectInstantiation,
        graph_model.SyntaxStepReturn,
        graph_model.SyntaxStepSwitch,
        graph_model.SyntaxStepSwitchLabelCase,
        graph_model.SyntaxStepSwitchLabelDefault,
        graph_model.SyntaxStepParenthesizedExpression,
        graph_model.SyntaxStepSymbolLookup,
        graph_model.SyntaxStepTernary,
        graph_model.SyntaxStepUnaryExpression,
        Node,
    ):
        safe_pickle.register_namedtuple(factory)

    for factory in (graph_model.SyntaxStepMeta,):
        safe_pickle.register_dataclass(factory)

    for factory, dumper, loader in (
        (graph_model.Graph, _dump_graph, _load_graph),
        (LarkMeta, _dump_lark_meta, _load_lark_meta),
        (LarkTree, _dump_lark_tree, _load_lark_tree),
        (ListToken, safe_pickle.tuple_dump, safe_pickle.list_load),
    ):
        safe_pickle.register(factory, dumper, loader)


# Side effects
_side_effects()

# Exported members
__all__ = ["dump", "load"]
