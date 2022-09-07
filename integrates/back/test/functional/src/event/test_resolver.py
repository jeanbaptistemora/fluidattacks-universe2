# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("event")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_get_event(populate: bool, email: str) -> None:
    assert populate
    event_id: str = "418900971"
    result: dict[str, Any] = await get_result(user=email, event=event_id)
    assert "errors" not in result
    assert "event" in result["data"]
    assert result["data"]["event"]["client"] == "Fluid"
    assert result["data"]["event"]["closingDate"] == "-"
    assert result["data"]["event"]["consulting"] == [
        {
            "content": "This is a test comment",
            "id": "43455343453",
            "fullName": "test one",
            "created": "2019/05/28 15:09:37",
        }
    ]
    assert result["data"]["event"]["detail"] == "ASM unit test"
    assert result["data"]["event"]["eventDate"] == "2018-06-27 07:00:00"
    assert result["data"]["event"]["eventStatus"] == "CREATED"
    assert result["data"]["event"]["eventType"] == "OTHER"
    assert result["data"]["event"]["groupName"] == "group1"
    assert result["data"]["event"]["hacker"] == "unittest@fluidattacks.com"
    assert result["data"]["event"]["historicState"] == [
        {
            "analyst": "unittest@fluidattacks.com",
            "date": "2018-06-27 07:00:00",
            "state": "OPEN",
        },
        {
            "analyst": "unittest@fluidattacks.com",
            "date": "2018-06-27 14:40:05",
            "state": "CREATED",
        },
    ]
    assert result["data"]["event"]["id"] == event_id
    assert result["data"]["event"]["subscription"] == "CONTINUOUS"
    assert result["data"]["event"]["evidences"] == {
        "file1": {
            "date": "2019-03-11 10:57:45",
            "fileName": "unittesting_418900971_evidence_file_1.csv",
        },
        "image1": {
            "date": "2019-03-11 10:57:45",
            "fileName": "unittesting_418900971_evidence_image_1.png",
        },
        "image2": None,
        "image3": None,
        "image4": None,
        "image5": None,
        "image6": None,
    }
