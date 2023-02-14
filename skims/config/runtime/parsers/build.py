import json
import os
import tree_sitter

GRAMMARS: dict[str, str] = dict(
    c_sharp=os.environ["envTreeSitterCSharp"],
    dart=os.environ["envTreeSitterDart"],
    go=os.environ["envTreeSitterGo"],
    hcl=os.environ["envTreeSitterHcl"],
    java=os.environ["envTreeSitterJava"],
    javascript=os.environ["envTreeSitterJavaScript"],
    json=os.environ["envTreeSitterJson"],
    kotlin=os.environ["envTreeSitterKotlin"],
    php=os.environ["envTreeSitterPhp"],
    python=os.environ["envTreeSitterPython"],
    ruby=os.environ["envTreeSitterRuby"],
    scala=os.environ["envTreeSitterScala"],
    tsx=os.path.join(os.environ["envTreeSitterTsx"], "tsx"),
    yaml=os.environ["envTreeSitterYaml"],
)


def get_fields(src: str) -> dict[str, tuple[str, ...]]:
    path: str = os.path.join(src, "src", "node-types.json")
    with open(path, encoding="utf-8") as handle:
        fields: dict[str, tuple[str, ...]] = {
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
