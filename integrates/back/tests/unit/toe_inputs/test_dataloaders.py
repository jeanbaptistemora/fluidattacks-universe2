from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
    ToeInputEdge,
    ToeInputsConnection,
)
from dynamodb.types import (
    PageInfo,
)
import pytest

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_by_group() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load(
        GroupToeInputsRequest(group_name=group_name)
    )
    assert group_toe_inputs == ToeInputsConnection(
        edges=(
            ToeInputEdge(
                node=ToeInput(
                    attacked_at=datetime.fromisoformat(
                        "2020-01-02T05:00:00+00:00"
                    ),
                    attacked_by="test@test.com",
                    be_present=True,
                    be_present_until=None,
                    component="test.com/api/Test",
                    entry_point="idTest",
                    first_attack_at=datetime.fromisoformat(
                        "2020-01-02T05:00:00+00:00"
                    ),
                    group_name="unittesting",
                    seen_at=datetime.fromisoformat(
                        "2000-01-01T05:00:00+00:00"
                    ),
                    seen_first_time_by="",
                    unreliable_root_id="",
                ),
                cursor="eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJJTlBVVFMjQ09NUE9ORU5UI3Rlc3QuY29tL2FwaS9UZXN0I0VOVFJZUE9JTlQjaWRUZXN0In0=",
            ),
            ToeInputEdge(
                node=ToeInput(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-02T05:00:00+00:00"
                    ),
                    attacked_by="test@test.com",
                    be_present=False,
                    be_present_until=datetime.fromisoformat(
                        "2021-03-20T15:41:04+00:00"
                    ),
                    component="test.com/test/test.aspx",
                    entry_point="btnTest",
                    first_attack_at=datetime.fromisoformat(
                        "2021-01-02T05:00:00+00:00"
                    ),
                    group_name="unittesting",
                    seen_at=datetime.fromisoformat(
                        "2020-03-14T05:00:00+00:00"
                    ),
                    seen_first_time_by="test@test.com",
                    unreliable_root_id="",
                ),
                cursor="eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJJTlBVVFMjQ09NUE9ORU5UI3Rlc3QuY29tL3Rlc3QvdGVzdC5hc3B4I0VOVFJZUE9JTlQjYnRuVGVzdCJ9",
            ),
            ToeInputEdge(
                node=ToeInput(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    attacked_by="test2@test.com",
                    be_present=True,
                    be_present_until=None,
                    component="test.com/test2/test.aspx",
                    entry_point="-",
                    first_attack_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    group_name="unittesting",
                    seen_at=datetime.fromisoformat(
                        "2020-01-11T05:00:00+00:00"
                    ),
                    seen_first_time_by="test2@test.com",
                    unreliable_root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                ),
                cursor="eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJJTlBVVFMjQ09NUE9ORU5UI3Rlc3QuY29tL3Rlc3QyL3Rlc3QuYXNweCNFTlRSWVBPSU5UIy0ifQ==",
            ),
        ),
        page_info=PageInfo(has_next_page=False, end_cursor="bnVsbA=="),
    )
