# Third party libraries
from lark import (
    Tree,
)
from lark.lexer import (
    Token,
)

# Local libraries
from parse_hcl2.loader import (
    load,
)


def test_load_empty() -> None:
    expected = Tree('start', [
        Tree('body', [

        ])
    ])

    with open('test/data/parse_hcl2/empty.tf') as file:
        template = load(file.read())

    assert template == expected


def test_load_full() -> None:
    expected = Tree('start', [
        Tree('body', [
            Tree('block', [
                Tree('identifier', [
                    Token('__ANON_3', 'module')
                ]),
                Token('STRING_LIT', '"iam_user"'),
                Tree('body', [
                    Tree('attribute', [
                        Tree('identifier', [
                            Token('__ANON_3', 'source')
                        ]),
                        Tree('expr_term', [
                            Token('STRING_LIT', '"modules\\/iam-user"')
                        ]),
                    ]),
                    Tree('attribute', [
                        Tree('identifier', [
                            Token('__ANON_3', 'name')
                        ]),
                        Tree('expr_term', [
                            Token('STRING_LIT', '"${var.iamuser}"')
                        ]),
                    ]),
                    Tree('attribute', [
                        Tree('identifier', [
                            Token('__ANON_3', 'force_destroy')
                        ]),
                        Tree('expr_term', [
                            Tree('true_lit', [])
                        ]),
                    ]),
                    Tree('attribute', [
                        Tree('identifier', [
                            Token('__ANON_3', 'tags')
                        ]),
                        Tree('expr_term', [
                            Tree('object', [
                                Tree('object_elem', [
                                    Tree('identifier', [
                                        Token('__ANON_3', 'proyecto')
                                    ]),
                                    Tree('expr_term', [
                                        Token('STRING_LIT', '"${var.proyecto}"')
                                    ])
                                ]),
                                Tree('object_elem', [
                                    Tree('identifier', [
                                        Token('__ANON_3', 'analista')
                                    ]),
                                    Tree('expr_term', [
                                        Token('STRING_LIT', '"${var.analista}"')
                                    ])
                                ]),
                            ])
                        ]),
                    ])
                ]),
            ])
        ])
    ])

    with open('test/data/parse_hcl2/full.tf') as file:
        template = load(file.read())

    assert template == expected
