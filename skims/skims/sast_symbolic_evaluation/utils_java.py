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
)


def lookup_java_class(
    args: EvaluatorArgs,
    class_name: str,
) -> Optional[graph_model.GraphShardMetadataJavaClass]:
    # First lookup the class in the current shard
    for class_path, class_data in args.shard.metadata.java.classes.items():
        qualified = args.shard.metadata.java.package + class_path

        if qualified.endswith(f'.{class_name}'):
            return class_data

    return None


def _lookup_java_field_in_shard(
    shard: graph_model.GraphShard,
    field_name: str,
) -> Optional[graph_model.GraphShardMetadataJavaClassField]:
    for class_path, class_data in shard.metadata.java.classes.items():
        for field_path, field_data in class_data.fields.items():
            qualified = shard.metadata.java.package + class_path + field_path

            if qualified == field_name:
                return field_data

    return None


def lookup_java_field(
    args: EvaluatorArgs,
    field_name: str,
) -> Optional[graph_model.GraphShardMetadataJavaClassField]:
    # First lookup in the current shard
    if data := _lookup_java_field_in_shard(args.shard, field_name):
        return data

    # Now lookoup in other shards different than the current shard
    for shard in args.graph_db.shards:
        if shard.path != args.shard.path:
            if data := _lookup_java_field_in_shard(shard, field_name):
                return data

    return None


def _lookup_java_method_in_shard(
    shard: graph_model.GraphShard,
    method_name: str,
) -> Optional[graph_model.GraphShardMetadataJavaClassMethod]:
    # First lookup the class in the current shard
    for class_path, class_data in shard.metadata.java.classes.items():
        for method_path, method_data in class_data.methods.items():
            qualified = shard.metadata.java.package + class_path + method_path

            if qualified.endswith(f'.{method_name}'):
                return method_data

    return None


def lookup_java_method(
    args: EvaluatorArgs,
    method_name: str,
) -> Optional[graph_model.GraphShardMetadataJavaClassMethod]:
    # First lookup in the current shard
    if data := _lookup_java_method_in_shard(args.shard, method_name):
        return data

    # Now lookoup in other shards different than the current shard
    for shard in args.graph_db.shards:
        if shard.path != args.shard.path:
            if data := _lookup_java_method_in_shard(shard, method_name):
                return data

    return None
