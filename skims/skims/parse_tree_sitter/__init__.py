# Standard library
import os
from typing import (
    Any,
    Dict,
)

# Third party libraries
from tree_sitter import (
    Language,
    Node,
    Parser,
    Tree,
)

# Local libraries
from state import (
    STATE_FOLDER,
)
from utils.ctx import (
    TREE_SITTER_JAVA,
)

# Constants
LANGUAGES_SO = os.path.join(STATE_FOLDER, 'languages.so')

# Side effects
Language.build_library(LANGUAGES_SO, [
    TREE_SITTER_JAVA,
])

# Constants
PARSER_JAVA: Parser = Parser()
PARSER_JAVA.set_language(Language(LANGUAGES_SO, 'java'))


def _build_tree(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, Tree):
        return _build_tree(obj.root_node)

    if isinstance(obj, Node):
        if obj.has_error:
            raise ValueError()

        return {
            'children': list(map(_build_tree, obj.children)),
            'c': obj.start_point[1],
            'l': obj.start_point[0],
            'type': obj.type,
        }

    raise NotImplementedError()


def parse_java(content: bytes) -> Dict[str, Any]:
    return _build_tree(PARSER_JAVA.parse(content))
