# Third party libraries
import pytest

# Local libraries
from parse_tree_sitter import (
    parse_java,
)


@pytest.mark.skims_test_group('unittesting')
def test_parse_java() -> None:
    tree = parse_java(b"""
    package x.x.x;
    import y.y;
    """)

    assert tree.root_node.sexp() == (
        '(program (package_declaration (scoped_identifier scope: (scoped_identifier '
        'scope: (identifier) name: (identifier)) name: (identifier))) '
        '(import_declaration (scoped_identifier scope: (identifier) name: '
        '(identifier))))'
    )
