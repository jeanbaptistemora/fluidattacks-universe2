from syntax_graph.syntax_readers.yaml import (
    block_mapping as yaml_block_mapping,
    block_mapping_pair as yaml_block_mapping_pair,
    block_sequence as yaml_block_sequence,
    flow_node as yaml_flow_node,
    stream as yaml_stream,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

YAML_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "block_mapping",
            "flow_mapping",
        },
        syntax_reader=yaml_block_mapping.reader,
    ),
    Dispatcher(
        applicable_types={
            "block_mapping_pair",
            "flow_pair",
        },
        syntax_reader=yaml_block_mapping_pair.reader,
    ),
    Dispatcher(
        applicable_types={
            "block_sequence",
        },
        syntax_reader=yaml_block_sequence.reader,
    ),
    Dispatcher(
        applicable_types={
            "flow_node",
        },
        syntax_reader=yaml_flow_node.reader,
    ),
    Dispatcher(
        applicable_types={
            "stream",
        },
        syntax_reader=yaml_stream.reader,
    ),
)
