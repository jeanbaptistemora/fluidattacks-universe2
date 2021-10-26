from syntax_graph.syntax_readers.c_sharp import (
    class_declaration as c_sharp_class_declaration,
    compilation_unit as c_sharp_compilation_unit,
    method_declaration as c_sharp_method_declaration,
    namespace_declaration as c_sharp_namespace_declaration,
    parameter as c_sharp_parameter,
    parameter_list as c_sharp_parameter_list,
)
from syntax_graph.syntax_readers.common import (
    block as common_block,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

CSHARP_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "block",
        },
        syntax_reader=common_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_declaration",
        },
        syntax_reader=c_sharp_class_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "compilation_unit",
        },
        syntax_reader=c_sharp_compilation_unit.reader,
    ),
    Dispatcher(
        applicable_types={
            "declaration_list",
        },
        syntax_reader=common_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "method_declaration",
        },
        syntax_reader=c_sharp_method_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "namespace_declaration",
        },
        syntax_reader=c_sharp_namespace_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameter",
        },
        syntax_reader=c_sharp_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameter_list",
        },
        syntax_reader=c_sharp_parameter_list.reader,
    ),
)
