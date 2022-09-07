# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    GraphShard,
    GraphShardMetadataLanguage,
)
from sast_symbolic_evaluation.lookup.common import (
    lookup_class as _lookup_class_common,
    lookup_field as _lookup_field_common,
    lookup_method as _lookup_method_common,
    lookup_shard_by_class as _lookup_shard_by_class_common,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    LookedUpClass,
    LookedUpClassField,
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


def lookup_field(
    args: EvaluatorArgs,
    field_name: str,
    field_class: Optional[str] = None,
) -> Optional[LookedUpClassField]:
    if args.shard.metadata.language == GraphShardMetadataLanguage.JAVA:
        return _lookup_field_common(
            args,
            field_name,
            GraphShardMetadataLanguage.JAVA,
            field_class,
        )

    if args.shard.metadata.language == GraphShardMetadataLanguage.CSHARP:
        return _lookup_field_common(
            args,
            field_name,
            GraphShardMetadataLanguage.CSHARP,
            field_class,
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


def lookup_shard_by_class(
    args: EvaluatorArgs,
    class_name: str,
) -> Optional[GraphShard]:
    if args.shard.metadata.language == GraphShardMetadataLanguage.JAVA:
        return _lookup_shard_by_class_common(
            args,
            class_name,
            GraphShardMetadataLanguage.JAVA,
        )

    if args.shard.metadata.language == GraphShardMetadataLanguage.CSHARP:
        return _lookup_shard_by_class_common(
            args,
            class_name,
            GraphShardMetadataLanguage.CSHARP,
        )

    return None
