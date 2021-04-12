# Standard library
from typing import (
    Optional,
)

# Local libraries
from model import (
    graph_model,
)
from sast_symbolic_evaluation.types import (
    EvaluatorArgs,
    LookedUpJavaClass,
    LookedUpJavaClassField,
    LookedUpJavaMethod,
)


def _lookup_java_class_in_shard(
    shard: graph_model.GraphShard,
    class_name: str,
) -> Optional[graph_model.GraphShardMetadataJavaClass]:
    # First lookup the class in the current shard
    for class_path, class_data in shard.metadata.java.classes.items():
        qualified = shard.metadata.java.package + class_path

        if class_name == qualified or qualified.endswith(f'.{class_name}'):
            return class_data

    return None


def lookup_java_class(
    args: EvaluatorArgs,
    class_name: str,
) -> Optional[LookedUpJavaClass]:
    # First lookup in the current shard
    if data := _lookup_java_class_in_shard(args.shard, class_name):
        return LookedUpJavaClass(
            metadata=data,
            shard_path=args.shard.path,
        )

    # Now lookoup in other shards different than the current shard
    for class_key, shard_path in args.graph_db.shards_by_java_class.items():
        if class_name == class_key:
            shard_index = args.graph_db.shards_by_path[shard_path]
            shard = args.graph_db.shards[shard_index]
            if data := _lookup_java_class_in_shard(shard, class_name):
                return LookedUpJavaClass(
                    metadata=data,
                    shard_path=shard.path,
                )

    return None


def _lookup_java_field_in_shard(
    shard: graph_model.GraphShard,
    field_name: str,
) -> Optional[graph_model.GraphShardMetadataJavaClassField]:
    for class_path, class_data in shard.metadata.java.classes.items():
        for field_path, field_data in class_data.fields.items():
            qualified = shard.metadata.java.package + class_path + field_path

            if qualified == field_name or (
                field_name and qualified.endswith(field_name)
            ):
                return field_data

    return None


def lookup_java_field(
    args: EvaluatorArgs,
    field_name: str,
    field_class: Optional[str] = None,
) -> Optional[LookedUpJavaClassField]:
    # First lookup in the current shard
    if data := _lookup_java_field_in_shard(args.shard, field_name):
        return LookedUpJavaClassField(data, args.shard.path)

    # Now lookoup in other shards different than the current shard
    if field_class and (
        shard_path := args.graph_db.shards_by_class.get(field_class)
    ):
        shard = args.graph_db.shards_by_path_f(shard_path)
        if data := _lookup_java_field_in_shard(shard, field_name):
            return LookedUpJavaClassField(data, shard.path)
    else:
        for shard in args.graph_db.shards:
            if shard.path != args.shard.path:
                if data := _lookup_java_field_in_shard(shard, field_name):
                    return LookedUpJavaClassField(data, shard.path)

    return None


def _lookup_java_method_in_shard(
    shard: graph_model.GraphShard,
    method_name: str,
) -> Optional[graph_model.GraphShardMetadataJavaClassMethod]:
    # First lookup the class in the current shard
    for class_path, class_data in shard.metadata.java.classes.items():
        for method_path, method_data in class_data.methods.items():
            canon = shard.metadata.java.package + class_path + method_path

            if canon == method_name or canon.endswith(f'.{method_name}'):
                return method_data

    return None


def lookup_java_method(
    args: EvaluatorArgs,
    method_name: str,
    method_class: Optional[str] = None,
) -> Optional[LookedUpJavaMethod]:
    # Lookup in other shards different than the current shard
    if method_class and (
        shard_path := args.graph_db.shards_by_java_class.get(method_class)
    ):
        shard = args.graph_db.shards_by_path_f(shard_path)
        if data := _lookup_java_method_in_shard(shard, method_name):
            return LookedUpJavaMethod(
                metadata=data,
                shard_path=shard.path,
            )

    # Lookup in the current shard
    if not method_class and (data := _lookup_java_method_in_shard(
            args.shard, method_name)):
        return LookedUpJavaMethod(
            metadata=data,
            shard_path=args.shard.path,
        )

    for shard in args.graph_db.shards:
        if shard.path != args.shard.path:
            if data := _lookup_java_method_in_shard(shard, method_name):
                return LookedUpJavaMethod(
                    metadata=data,
                    shard_path=shard.path,
                )

    return None
