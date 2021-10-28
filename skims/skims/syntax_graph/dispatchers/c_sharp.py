from syntax_graph.syntax_readers.c_sharp import (
    argument as c_sharp_argument,
    argument_list as c_sharp_argument_list,
    bracketed_argument_list as c_sharp_bracketed_argument_list,
    class_declaration as c_sharp_class_declaration,
    compilation_unit as c_sharp_compilation_unit,
    local_declaration_statement as c_sharp_local_declaration_statement,
    method_declaration as c_sharp_method_declaration,
    namespace_declaration as c_sharp_namespace_declaration,
    parameter as c_sharp_parameter,
    parameter_list as c_sharp_parameter_list,
    variable_declaration as c_sharp_variable_declaration,
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
            "argument",
        },
        syntax_reader=c_sharp_argument.reader,
    ),
    Dispatcher(
        applicable_types={
            "argument_list",
        },
        syntax_reader=c_sharp_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "bracketed_argument_list",
        },
        syntax_reader=c_sharp_bracketed_argument_list.reader,
    ),
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
            "local_declaration_statement",
        },
        syntax_reader=c_sharp_local_declaration_statement.reader,
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
    Dispatcher(
        applicable_types={
            "variable_declaration",
        },
        syntax_reader=c_sharp_variable_declaration.reader,
    ),
)
