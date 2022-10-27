# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from db_model.enrollment.types import (
    Enrollment,
)
from enrollment import (
    domain as enrollment_domain,
)
from freezegun import (
    freeze_time,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_enrollment")
@freeze_time("2022-10-21T15:58:31.280182")
async def test_should_add_enrollment(
    populate: bool, mocker: MockerFixture
) -> None:
    assert populate
    mail_spy = mocker.spy(enrollment_domain, "mail_free_trial_start")
    query = """
        mutation AddEnrollment {
            addEnrollment {
                success
            }
        }
    """
    email = "johndoe@fluidattacks.com"
    loaders = get_new_context()
    result = await get_graphql_result(
        data={"query": query},
        stakeholder=email,
        context=loaders,
    )

    assert "errors" not in result
    assert result["data"]["addEnrollment"]["success"]

    loaders.enrollment.clear_all()
    enrollment: Enrollment = await loaders.enrollment.load(email)
    assert enrollment.enrolled
    assert enrollment.trial.start_date == "2022-10-21T15:58:31.280182+00:00"

    assert mail_spy.await_count == 1
    mail_spy.assert_any_call(mock.ANY, email, "unit test", "testgroup")


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_enrollment")
@freeze_time("2022-10-21T15:58:31.280182")
async def test_should_validate_uniqueness(populate: bool) -> None:
    assert populate
    query = """
        mutation AddEnrollment {
            addEnrollment {
                success
            }
        }
    """
    email = "janedoe@fluidattacks.com"
    loaders = get_new_context()
    result = await get_graphql_result(
        data={"query": query},
        stakeholder=email,
        context=loaders,
    )

    assert "errors" in result
    assert result["errors"][0]["message"] == "Enrollment user already exists"
