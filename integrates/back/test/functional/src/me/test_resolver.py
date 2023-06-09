# pylint: disable=import-error, too-many-arguments
from . import (
    get_has_drafts_rejected,
    get_result,
    get_vulnerabilities,
)
from back.test.functional.src.reject_draft import (
    get_result as reject_draft,
)
from back.test.functional.src.submit_draft import (
    get_result as submit_draft,
)
from back.test.functional.src.unsubscribe_from_group import (
    get_result as unsubscribe_from_group,
)
from db_model.enums import (
    CredentialType,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.mark.parametrize(
    (
        "email",
        "role",
        "permissions",
        "phone",
        "groups_length",
        "assigned",
        "enrolled",
        "credentials",
    ),
    (
        (
            "admin@gmail.com",
            "admin",
            14,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "1111111111",
            },
            3,
            [],
            True,
            [],
        ),
        (
            "user@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "2029182132",
            },
            1,
            [{"id": "6401bc87-8633-4a4a-8d8e-7dae0ca57e6b"}],
            True,
            [],
        ),
        (
            "user_manager@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "77777777777777",
            },
            1,
            [{"id": "de70c2f7-7ec7-49aa-9a84-aff4fbe5d1ad"}],
            False,
            [],
        ),
        (
            "vulnerability_manager@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "51",
                "countryCode": "PE",
                "nationalNumber": "1111111111111",
            },
            1,
            [{"id": "be09edb7-cd5c-47ed-bee4-97c645acdce8"}],
            False,
            [],
        ),
        (
            "hacker@gmail.com",
            "hacker",
            2,
            {
                "callingCountryCode": "1",
                "countryCode": "US",
                "nationalNumber": "2029182131",
            },
            2,
            [],
            False,
            [],
        ),
        (
            "reattacker@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "4444444444444",
            },
            1,
            [],
            False,
            [],
        ),
        (
            "resourcer@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "33333333333",
            },
            1,
            [],
            False,
            [],
        ),
        (
            "reviewer@gmail.com",
            "user",
            3,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "7777777777",
            },
            2,
            [],
            False,
            [],
        ),
        (
            "service_forces@gmail.com",
            "user",
            3,
            None,
            1,
            [],
            False,
            [],
        ),
        (
            "customer_manager@fluidattacks.com",
            "user",
            12,
            {
                "callingCountryCode": "57",
                "countryCode": "CO",
                "nationalNumber": "9999999999999",
            },
            1,
            [],
            True,
            [
                {
                    "azureOrganization": None,
                    "isPat": False,
                    "isToken": True,
                    "key": None,
                    "name": "cred_https_token",
                    "oauthType": "",
                    "organization": {
                        "id": "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
                    },
                    "owner": "customer_manager@fluidattacks.com",
                    "password": None,
                    "token": "token test",
                    "type": CredentialType.HTTPS,
                    "user": None,
                },
            ],
        ),
    ),
)
async def test_get_me(
    populate: bool,
    email: str,
    role: str,
    permissions: int,
    phone: dict[str, str],
    groups_length: int,
    assigned: list[dict[str, str]],
    enrolled: bool,
    credentials: list[dict[str, str]],
) -> None:
    assert populate
    org_name: str = "orgtest"
    organization: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: dict[str, Any] = await get_result(
        user=email,
        org_id=organization,
    )
    assert "errors" not in result
    assert '{"hasAccessToken": false' in result["data"]["me"]["accessToken"]
    assert result["data"]["me"]["callerOrigin"] == "API"
    assert result["data"]["me"]["enrolled"] == enrolled
    assert result["data"]["me"]["vulnerabilitiesAssigned"] == assigned
    assert result["data"]["me"]["credentials"] == credentials
    assert not result["data"]["me"]["isConcurrentSession"]
    assert len(result["data"]["me"]["notificationsPreferences"]["email"]) == 18
    assert result["data"]["me"]["organizations"][0]["name"] == org_name
    assert (
        len(result["data"]["me"]["organizations"][0]["groups"])
        == groups_length
    )
    assert len(result["data"]["me"]["permissions"]) == permissions
    assert result["data"]["me"]["phone"] == phone
    assert not result["data"]["me"]["remember"]
    assert result["data"]["me"]["role"] == role
    assert result["data"]["me"]["subscriptionsToEntityReport"] == []
    assert result["data"]["me"]["tags"] == []
    assert result["data"]["me"]["tours"] == {
        "newGroup": False,
        "newRoot": False,
    }
    assert result["data"]["me"]["pendingEvents"][0]["id"] == "418900971"
    assert result["data"]["me"]["userEmail"] == email
    assert result["data"]["me"]["userName"] == "unit test"
    assert result["data"]["me"]["__typename"] == "Me"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.mark.parametrize(
    ["email", "length"],
    [
        ["user@gmail.com", 1],
        ["user_manager@gmail.com", 1],
        ["vulnerability_manager@gmail.com", 1],
    ],
)
async def test_get_me_assigned(
    populate: bool, email: str, length: int
) -> None:
    assert populate
    result: dict[str, Any] = await get_vulnerabilities(
        user=email,
    )
    assert "errors" not in result
    assert len(result["data"]["me"]["vulnerabilitiesAssigned"]) == length
    assert len(result["data"]["me"]["reattacks"]["edges"]) == 1
    assert result["data"]["me"]["reattacks"]["edges"][0]["node"] == {
        "lastRequestedReattackDate": "2019-12-31 19:45:12"
    }
    assert (
        len(result["data"]["me"]["findingReattacksConnection"]["edges"]) == 2
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][0]["node"][
            "id"
        ]
        == "475041521"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][0]["node"][
            "state"
        ]
        == "open"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][0]["node"][
            "status"
        ]
        == "VULNERABLE"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][1]["node"][
            "id"
        ]
        == "3c475384-834c-47b0-ac71-a41a022e401c"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][1]["node"][
            "state"
        ]
        == "open"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][1]["node"][
            "status"
        ]
        == "VULNERABLE"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][0]["node"][
            "groupName"
        ]
        == "group1"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][1]["node"][
            "groupName"
        ]
        == "group1"
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][0]["node"][
            "verificationSummary"
        ]["requested"]
        == 3
    )
    assert (
        result["data"]["me"]["findingReattacksConnection"]["edges"][1]["node"][
            "verificationSummary"
        ]["requested"]
        == 1
    )
    assert (
        len(
            result["data"]["me"]["findingReattacksConnection"]["edges"][0][
                "node"
            ]["vulnerabilitiesToReattackConnection"]["edges"]
        )
        == 1
    )
    assert (
        len(
            result["data"]["me"]["findingReattacksConnection"]["edges"][1][
                "node"
            ]["vulnerabilitiesToReattackConnection"]["edges"]
        )
        == 0
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_get_me_has_drafts_rejected(populate: bool, email: str) -> None:
    assert populate
    not_rejected: dict[str, Any] = await get_has_drafts_rejected(
        user=email,
    )
    assert "errors" not in not_rejected
    assert not not_rejected["data"]["me"]["hasDraftsRejected"]

    reject_draft_result: dict[str, Any] = await reject_draft(
        user=email,
        finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
        reasons="WRITING, CONSISTENCY",
    )
    assert "errors" not in reject_draft_result
    assert reject_draft_result["data"]["rejectDraft"]["success"]

    rejected: dict[str, Any] = await get_has_drafts_rejected(
        user=email,
    )
    assert "errors" not in rejected
    assert rejected["data"]["me"]["hasDraftsRejected"]

    submit_draft_result: dict[str, Any] = await submit_draft(
        user=email, finding_id="3c475384-834c-47b0-ac71-a41a022e401c"
    )
    assert "errors" not in submit_draft_result
    assert submit_draft_result["data"]["submitDraft"]["success"]

    not_rejected_1: dict[str, Any] = await get_has_drafts_rejected(
        user=email,
    )
    assert "errors" not in not_rejected_1
    assert not not_rejected_1["data"]["me"]["hasDraftsRejected"]

    reject_draft_result_1: dict[str, Any] = await reject_draft(
        user=email,
        finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
        reasons="CONSISTENCY",
    )
    assert "errors" not in reject_draft_result_1
    assert reject_draft_result_1["data"]["rejectDraft"]["success"]

    rejected_2: dict[str, Any] = await get_has_drafts_rejected(
        user=email,
    )
    assert "errors" not in rejected_2
    assert rejected_2["data"]["me"]["hasDraftsRejected"]

    unsubscribe: dict[str, Any] = await unsubscribe_from_group(
        email=email, group_name="group1"
    )
    assert "errors" not in unsubscribe
    assert unsubscribe["data"]["unsubscribeFromGroup"]["success"]

    not_rejected_2: dict[str, Any] = await get_has_drafts_rejected(
        user=email,
    )
    assert "errors" not in not_rejected_2
    assert not not_rejected_2["data"]["me"]["hasDraftsRejected"]
