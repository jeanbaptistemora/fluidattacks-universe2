import os
import tree_sitter

tree_sitter.Language.build_library(
    os.environ["out"],
    [
        os.environ["envTreeSitterCSharp"],
        os.environ["envTreeSitterGo"],
        os.environ["envTreeSitterJava"],
        os.environ["envTreeSitterJavaScript"],
        os.environ["envTreeSitterKotlin"],
        os.environ["envTreeSitterTsx"] + "/tsx",
    ],
)
