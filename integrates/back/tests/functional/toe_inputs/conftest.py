from back.tests import (
    db,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_inputs")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "toe_inputs": (
            ToeInput(
                commit="hh66uu5",
                component="test.com/api/Test",
                created_date="2000-01-01T00:00:00-05:00",
                entry_point="idTest",
                group_name="group1",
                seen_first_time_by="",
                tested_date="2020-01-02T00:00:00-05:00",
                verified="Yes",
                unreliable_root_id="",
                vulns="FIN.S.0001.Test",
            ),
            ToeInput(
                commit="e91320h",
                component="test.com/test/test.aspx",
                created_date="2020-03-14T00:00:00-05:00",
                entry_point="btnTest",
                group_name="group1",
                seen_first_time_by="test@test.com",
                tested_date="2021-02-02T00:00:00-05:00",
                unreliable_root_id="",
                verified="No",
                vulns="",
            ),
            ToeInput(
                commit="d83027t",
                component="test.com/test2/test.aspx",
                created_date="2020-01-11T00:00:00-05:00",
                entry_point="-",
                group_name="group1",
                seen_first_time_by="test2@test.com",
                tested_date="2021-02-11T00:00:00-05:00",
                unreliable_root_id="",
                verified="No",
                vulns="FIN.S.0003.Test",
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
