# Third library
import pytest

# Local import
from model.graph_model import GraphShardMetadataLanguage
from test_helpers import create_test_context
from sast.parse import parse_one

create_test_context()


@pytest.mark.skims_test_group("unittesting")
def test_pdg() -> None:
    graph_shard = parse_one(
        language=GraphShardMetadataLanguage.CSHARP,
        path="skims/test/data/transformations/csharp.cs",
    )

    graph = graph_shard.graph

    assert graph["23"].get("50")  # line: 6 -> 9
    assert graph["23"].get("61")  # line: 6 -> 11
    assert graph["61"].get("66")  # line: 11 -> 12
    assert graph["61"].get("77")  # line: 11 -> 13
    assert graph["83"].get("90")  # line: 14 -> 16
    assert graph["90"].get("146")  # line: 16 -> 27
    assert graph["96"].get("134")  # line: 17 -> 26
    assert graph["106"].get("112")  # line: 21 -> 22
    assert graph["106"].get("134")  # line: 21 -> 26
    assert graph["112"].get("146")  # line: 22 -> 27
