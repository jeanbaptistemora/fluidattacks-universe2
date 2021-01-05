# Third party libraries
from tree_sitter import (
    Language,
    Parser,
    Tree,
)

# Local libraries
from utils.ctx import (
    TREE_SITTER_JAVA,
)

# Side effects
Language.build_library('skims-languages.so', [
    TREE_SITTER_JAVA,
])

# Constants
PARSER_JAVA: Parser = Parser()
PARSER_JAVA.set_language(Language('skims-languages.so', 'java'))


def parse_java(content: bytes) -> Tree:
    return PARSER_JAVA.parse(content)
