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
from parse_hcl2.structure import (
    iterate_resources,
)
from parse_hcl2.tokens import (
    Attribute,
    Block,
)


def test_iterate_resources() -> None:
    with open('test/data/parse_hcl2/iam.tf') as file:
        model = load(file.read())

    assert len(tuple(iterate_resources(model, 'resource', 'aws_iam_role'))) == 1
