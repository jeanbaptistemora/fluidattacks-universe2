from syntax_graph.syntax_readers.common import (
    library_name as common_library_name,
    parameter_list as common_parameter_list,
    program as common_program,
)
from syntax_graph.syntax_readers.dart import (
    function_signature as dart_function_signature,
    import_or_export as dart_import_or_export,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

DART_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "function_signature",
        },
        syntax_reader=dart_function_signature.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_or_export",
        },
        syntax_reader=dart_import_or_export.reader,
    ),
    Dispatcher(
        applicable_types={
            "library_name",
        },
        syntax_reader=common_library_name.reader,
    ),
    Dispatcher(
        applicable_types={
            "formal_parameter_list",
        },
        syntax_reader=common_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=common_program.reader,
    ),
)
