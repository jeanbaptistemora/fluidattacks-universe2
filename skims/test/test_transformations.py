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

    assert graph["24"].get("45")  # line: 6  -> 8
    assert graph["24"].get("55")  # line: 6  -> 10
    assert graph["24"].get("71")  # line: 6  -> 15
    assert graph["24"].get("83")  # line: 6  -> 18
    assert graph["33"].get("95")  # line: 7  -> 19
    assert graph["52"].get("95")  # line: 10 -> 19
    assert graph["62"].get("83")  # line: 14 -> 18
    assert graph["68"].get("95")  # line: 15 -> 19


test_pdg()
