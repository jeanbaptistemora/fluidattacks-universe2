from typing import Optional
from model.graph_model import GraphShard, GraphShardMetadataLanguage
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    LookedUpJavaClass,
    LookedUpJavaClassField,
    LookedUpJavaMethod,
)
from sast_symbolic_evaluation.lookup.java import (
    lookup_class as _lookup_class_java,
    lookup_field as _lookup_field_java,
    lookup_method as _lookup_method_java,
    lookup_shard_by_class as _lookup_shard_by_class_java,
)


def lookup_class(
    args: EvaluatorArgs,
    class_name: str,
) -> Optional[LookedUpJavaClass]:
    if args.shard.metadata.language == GraphShardMetadataLanguage.JAVA:
        return _lookup_class_java(args, class_name)

    return None


def lookup_field(
    args: EvaluatorArgs,
    field_name: str,
    field_class: Optional[str] = None,
) -> Optional[LookedUpJavaClassField]:
    if args.shard.metadata.language == GraphShardMetadataLanguage.JAVA:
        return _lookup_field_java(args, field_name, field_class)

    return None


def lookup_method(
    args: EvaluatorArgs,
    method_name: str,
    method_class: Optional[str] = None,
) -> Optional[LookedUpJavaMethod]:
    if args.shard.metadata.language == GraphShardMetadataLanguage.JAVA:
        return _lookup_method_java(args, method_name, method_class)

    return None


def lookup_shard_by_class(
    args: EvaluatorArgs,
    class_name: str,
) -> Optional[GraphShard]:
    if args.shard.metadata.language == GraphShardMetadataLanguage.JAVA:
        return _lookup_shard_by_class_java(args, class_name)

    return None
