# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    RootEnvironmentUrl,
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
@pytest.mark.resolver_test_group("update_toe_input")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date="2020-11-19T13:37:10+00:00",
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    group_name="group1",
                    id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        environment_urls=["https://test.com"],
                        git_environment_urls=[
                            RootEnvironmentUrl(
                                url="https://test.com",
                                id="78dd64d3198473115a7f5263d27bed15f9f2fc07",
                            )
                        ],
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date="2020-11-19T13:37:10+00:00",
                        nickname="test_nickname_1",
                        other=None,
                        reason=None,
                        status=RootStatus.INACTIVE,
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date="2020-11-19T13:37:10+00:00",
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    group_name="group1",
                    id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        environment_urls=["https://test.com"],
                        git_environment_urls=[
                            RootEnvironmentUrl(
                                url="https://test.com",
                                id="78dd64d3198473115a7f5263d27bed15f9f2fc07",
                            )
                        ],
                        gitignore=["node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date="2020-11-19T13:37:10+00:00",
                        nickname="test_nickname_2",
                        other=None,
                        reason=None,
                        status=RootStatus.INACTIVE,
                        url="https://gitlab.com/fluidattacks/asm_1",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
        "toe_inputs": (
            ToeInput(
                attacked_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                attacked_by="",
                be_present=True,
                be_present_until=None,
                component="https://test.com/test",
                entry_point="idTest",
                first_attack_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                seen_at=None,
                seen_first_time_by="",
                unreliable_root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
            ),
            ToeInput(
                attacked_at=datetime.fromisoformat(
                    "2021-02-02T05:00:00+00:00"
                ),
                attacked_by="",
                be_present=True,
                be_present_until=None,
                component="192.168.1.1:8080",
                entry_point="btnTest",
                first_attack_at=datetime.fromisoformat(
                    "2021-02-02T05:00:00+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                seen_at=datetime.fromisoformat("2020-03-14T05:00:00+00:00"),
                seen_first_time_by="test@test.com",
                unreliable_root_id="",
            ),
            ToeInput(
                attacked_at=datetime.fromisoformat(
                    "2021-02-11T05:00:00+00:00"
                ),
                attacked_by="",
                be_present=False,
                be_present_until=datetime.fromisoformat(
                    "2021-03-11T05:00:00+00:00"
                ),
                component="https://app.fluidattacks.com:8080/test",
                entry_point="-",
                first_attack_at=datetime.fromisoformat(
                    "2021-02-11T05:00:00+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                seen_at=datetime.fromisoformat("2020-01-11T05:00:00+00:00"),
                seen_first_time_by="test2@test.com",
                unreliable_root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
