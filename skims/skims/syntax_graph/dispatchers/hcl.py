from syntax_graph.syntax_readers.hcl import (
    attribute as hcl_attribute,
    block as hcl_block,
    config_file as hcl_config_file,
    expression as hcl_expression,
    identifier as hcl_identifier,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

HCL_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "attribute",
            "object_elem",
        },
        syntax_reader=hcl_attribute.reader,
    ),
    Dispatcher(
        applicable_types={
            "block",
        },
        syntax_reader=hcl_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "config_file",
        },
        syntax_reader=hcl_config_file.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression",
        },
        syntax_reader=hcl_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=hcl_identifier.reader,
    ),
)
