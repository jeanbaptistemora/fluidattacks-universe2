from model import (
    graph_model,
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
from utils.string import (
    split_on_last_dot,
)


def _lookup_class_in_shard(
    shard: graph_model.GraphShard,
    class_name: str,
    language: graph_model.GraphShardMetadataLanguage,
) -> Optional[graph_model.GraphShardMetadataClass]:
    # First lookup the class in the current shard
    language_data = getattr(shard.metadata, language.value)
    if data := language_data.classes.get(class_name):
        return data
    if data := language_data.classes.get(f".{class_name}"):
        return data
    for class_path, class_data in language_data.classes.items():
        qualified = language_data.package + class_path

        if class_name == qualified or qualified.endswith(f".{class_name}"):
            return class_data

    return None


def lookup_shard_by_class(
    args: EvaluatorArgs,
    class_name: str,
    language: graph_model.GraphShardMetadataLanguage,
) -> Optional[graph_model.GraphShard]:
    language_data = getattr(args.shard.metadata, language.value)

    if path := args.graph_db.shards_by_language_class[language.value].get(
        class_name
    ):
        return args.graph_db.shards_by_path_f(path)

    if path := args.graph_db.shards_by_language_class[language.value].get(
        f".{class_name}"
    ):
        return args.graph_db.shards_by_path_f(path)

    # It can be access to a static field
    _class = ".".join(class_name.split(".")[:-1])
    if path := args.graph_db.shards_by_language_class[language.value].get(
        _class
    ):
        return args.graph_db.shards_by_path_f(path)

    # la clase actual puyede estar en el shard actual
    if class_name in language_data.classes:
        return args.shard
    # Is possible that the class does not have a package
    if class_name.startswith("."):
        class_name = class_name.replace(".", "", 1)
    for key, path in args.graph_db.shards_by_language_class[
        language.value
    ].items():
        if key.endswith(f".{class_name}"):
            return args.graph_db.shards_by_path_f(path)

    return None


def lookup_class(
    args: EvaluatorArgs,
    class_name: str,
    language: graph_model.GraphShardMetadataLanguage,
) -> Optional[LookedUpClass]:
    # First lookup in the current shard
    if data := _lookup_class_in_shard(args.shard, class_name, language):
        return LookedUpClass(
            metadata=data,
            shard_path=args.shard.path,
        )

    # Now lookoup in other shards different than the current shard
    if (shard := lookup_shard_by_class(args, class_name, language)) and (
        data := _lookup_class_in_shard(shard, class_name, language)
    ):
        return LookedUpClass(
            metadata=data,
            shard_path=shard.path,
        )

    return None


def _lookup_field_in_shard(
    shard: graph_model.GraphShard,
    field_name: str,
    language: graph_model.GraphShardMetadataLanguage,
) -> Optional[graph_model.GraphShardMetadataClassField]:
    language_data = getattr(shard.metadata, language.value)

    for class_path, class_data in language_data.classes.items():
        for field_path, field_data in class_data.fields.items():
            qualified = language_data.package + class_path + field_path

            if qualified == field_name or (
                field_name and qualified.endswith(field_name)
            ):
                return field_data

    return None


def lookup_field(
    args: EvaluatorArgs,
    field_name: str,
    language: graph_model.GraphShardMetadataLanguage,
    field_class: Optional[str] = None,
) -> Optional[LookedUpClassField]:
    # method_name can be an empty string
    if not field_name:
        return None

    # First lookup in the current shard
    if data := _lookup_field_in_shard(args.shard, field_name, language):
        return LookedUpClassField(data, args.shard.path)

    # Now lookoup in other shards different than the current shard
    if (
        field_class
        and (shard := lookup_shard_by_class(args, field_class, language))
        and (data := _lookup_field_in_shard(shard, field_name, language))
    ):
        return LookedUpClassField(data, shard.path)

    # Can be an static field
    if (shard := lookup_shard_by_class(args, field_name, language)) and (
        data := _lookup_field_in_shard(shard, field_name, language)
    ):
        return LookedUpClassField(data, shard.path)

    return None


def _lookup_method_in_shard(
    shard: graph_model.GraphShard,
    method_name: str,
    language: graph_model.GraphShardMetadataLanguage,
) -> Optional[graph_model.GraphShardMetadataClassMethod]:
    # First lookup the class in the current shard
    language_data = getattr(shard.metadata, language.value)
    for class_path, class_data in language_data.classes.items():
        for method_path, method_data in class_data.methods.items():
            canon = language_data.package + class_path + method_path

            if canon == method_name or canon.endswith(f".{method_name}"):
                return method_data

    return None


def lookup_method(
    args: EvaluatorArgs,
    method_name: str,
    language: graph_model.GraphShardMetadataLanguage,
    method_class: Optional[str] = None,
) -> Optional[LookedUpMethod]:
    # method_name can be an empty string
    if not method_name:
        return None

    # Lookup in other shards different than the current shard
    if (
        method_class
        and (shard := lookup_shard_by_class(args, method_class, language))
        and (data := _lookup_method_in_shard(shard, method_name, language))
    ):
        return LookedUpMethod(
            metadata=data,
            shard_path=shard.path,
        )
    if "this" in method_name:
        method_name = method_name.split("this.")[-1]
    # Lookup in the current shard
    if not method_class and (
        data := _lookup_method_in_shard(args.shard, method_name, language)
    ):
        return LookedUpMethod(
            metadata=data,
            shard_path=args.shard.path,
        )

    # Lookup for static methods
    _method_class, _method_name = split_on_last_dot(method_name)
    if (
        _method_name
        and _method_class
        and (shard := lookup_shard_by_class(args, _method_class, language))
        and (data := _lookup_method_in_shard(shard, method_name, language))
    ):
        return LookedUpMethod(
            metadata=data,
            shard_path=shard.path,
        )

    return None
