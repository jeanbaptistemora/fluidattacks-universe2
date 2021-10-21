import json
import os
import tree_sitter
from typing import (
    Dict,
    Tuple,
)

GRAMMARS: Dict[str, str] = dict(
    c_sharp=os.environ["envTreeSitterCSharp"],
    go=os.environ["envTreeSitterGo"],
    java=os.environ["envTreeSitterJava"],
    javascript=os.environ["envTreeSitterJavaScript"],
    kotlin=os.environ["envTreeSitterKotlin"],
    php=os.environ["envTreeSitterPhp"],
    tsx=os.path.join(os.environ["envTreeSitterTsx"], "tsx"),
)


def get_fields(src: str) -> Dict[str, Tuple[str, ...]]:
    path: str = os.path.join(src, "src", "node-types.json")
    with open(path, encoding="utf-8") as handle:
        fields: Dict[str, Tuple[str, ...]] = {
            node["type"]: fields
            for node in json.load(handle)
            for fields in [tuple(node.get("fields", {}))]
            if fields
        }
    return fields


def main() -> None:
    out: str = os.environ["out"]
    path: str

    os.makedirs(out)

    for grammar, src in GRAMMARS.items():
        path = os.path.join(out, f"{grammar}.so")
        tree_sitter.Language.build_library(path, [src])

        path = os.path.join(out, f"{grammar}-fields.json")
        with open(path, encoding="utf-8", mode="w") as file:
            json.dump(get_fields(src), file)


if __name__ == "__main__":
    main()
