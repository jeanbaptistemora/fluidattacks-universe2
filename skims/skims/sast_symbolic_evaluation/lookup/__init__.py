from model.graph_model import (
    GraphShardMetadataLanguage,
)
from sast_symbolic_evaluation.lookup.common import (
    lookup_class as _lookup_class_common,
    lookup_method as _lookup_method_common,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    LookedUpClass,
    LookedUpMethod,
)
from typing import (
    Optional,
)


def lookup_class(
    args: EvaluatorArgs,
    class_name: str,
) -> Optional[LookedUpClass]:
    if args.shard.metadata.language == GraphShardMetadataLanguage.JAVA:
        return _lookup_class_common(
            args,
            class_name,
            GraphShardMetadataLanguage.JAVA,
        )

    if args.shard.metadata.language == GraphShardMetadataLanguage.CSHARP:
        return _lookup_class_common(
            args,
            class_name,
            GraphShardMetadataLanguage.CSHARP,
        )

    return None


def lookup_method(
    args: EvaluatorArgs,
    method_name: str,
    method_class: Optional[str] = None,
) -> Optional[LookedUpMethod]:
    if args.shard.metadata.language == GraphShardMetadataLanguage.JAVA:
        return _lookup_method_common(
            args,
            method_name,
            GraphShardMetadataLanguage.JAVA,
            method_class,
        )

    if args.shard.metadata.language == GraphShardMetadataLanguage.CSHARP:
        return _lookup_method_common(
            args,
            method_name,
            GraphShardMetadataLanguage.CSHARP,
            method_class,
        )

    return None
