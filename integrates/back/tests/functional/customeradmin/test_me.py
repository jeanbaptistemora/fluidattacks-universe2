from back.tests.functional.customeradmin.utils import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("old")
async def test_me() -> None:  # pylint: disable=too-many-statements
    context = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    group_name = "unittesting"
    query = """
        mutation {
            signIn(
                authToken: "badtoken",
                provider: GOOGLE
            ) {
                sessionJwt
                success
            }
        }
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert "success" in result["data"]["signIn"]
    assert not result["data"]["signIn"]["success"]

    expiration_time = datetime.utcnow() + timedelta(weeks=8)
    int_expiration_time = int(expiration_time.timestamp())
    query = f"""
        mutation {{
            updateAccessToken(expirationTime: {int_expiration_time}) {{
                sessionJwt
                success
            }}
        }}
    """

    context = get_new_context()
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert result["data"]["updateAccessToken"]["success"]
    session_jwt = result["data"]["updateAccessToken"]["sessionJwt"]

    context = get_new_context()
    query = """
        mutation {
            addPushToken(token: "ExponentPushToken[something123]") {
                success
            }
        }
    """
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt, context=context)
    assert "error" not in result
    assert result["data"]["addPushToken"]["success"]

    context = get_new_context()
    frecuency = "WEEKLY"
    entity = "GROUP"
    query = f"""
        mutation {{
            subscribeToEntityReport(
                frequency: {frecuency},
                reportEntity: {entity},
                reportSubject: "{org_id}"


            ) {{
                success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt, context=context)
    assert "errors" not in result
    assert result["data"]["subscribeToEntityReport"]["success"]

    context = get_new_context()
    query = """
        mutation {
            acceptLegal(remember: false) {
                success
            }
        }
    """
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt, context=context)
    assert "errors" not in result
    assert result["data"]["acceptLegal"]["success"]

    context = get_new_context()
    query = f"""{{
        me(callerOrigin: "API") {{
            accessToken
            callerOrigin
            organizations {{
                name
            }}
            permissions(entity: USER)
            remember
            role(entity: USER)
            sessionExpiration
            subscriptionsToEntityReport{{
                entity
                frequency
                subject

            }}
            tags(organizationId: "{org_id}") {{
                name
                projects {{
                    name
                }}
            }}
            __typename
        }}
    }}"""
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt, context=context)
    assert "errors" not in result
    assert '{"hasAccessToken": true' in result["data"]["me"]["accessToken"]
    assert result["data"]["me"]["callerOrigin"] == "API"
    assert result["data"]["me"]["organizations"] == [
        {"name": "okada"},
        {"name": "kamiya"},
        {"name": "bulat"},
        {"name": "makimachi"},
    ]
    assert len(result["data"]["me"]["permissions"]) == 0
    assert result["data"]["me"]["remember"] == False
    assert result["data"]["me"]["role"] == "customeradmin"
    assert result["data"]["me"]["sessionExpiration"] == str(
        datetime.fromtimestamp(int_expiration_time)
    )
    assert result["data"]["me"]["subscriptionsToEntityReport"] == [
        {"entity": "DIGEST", "frequency": "HOURLY", "subject": "ALL_GROUPS"},
        {"entity": entity, "frequency": frecuency, "subject": org_id},
    ]
    assert result["data"]["me"]["tags"] == [
        {
            "name": "another-tag",
            "projects": [
                {"name": "continuoustesting"},
                {"name": "oneshottest"},
            ],
        },
        {
            "name": "test-projects",
            "projects": [
                {"name": "oneshottest"},
                {"name": "unittesting"},
            ],
        },
        {
            "name": "test-updates",
            "projects": [
                {"name": "oneshottest"},
                {"name": "unittesting"},
            ],
        },
    ]
    assert result["data"]["me"]["__typename"] == "Me"

    context = get_new_context()
    query = f"""{{
        me(callerOrigin: "API") {{
            permissions(entity: PROJECT, identifier: "{group_name}")
            role(entity: PROJECT, identifier: "{group_name}")
        }}
    }}"""
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt, context=context)
    assert "errors" not in result
    assert len(result["data"]["me"]["permissions"]) == 59
    assert result["data"]["me"]["role"] == "customeradmin"

    context = get_new_context()
    query = f"""{{
        me(callerOrigin: "API") {{
            permissions(entity: ORGANIZATION, identifier: "{group_name}")
            role(entity: ORGANIZATION, identifier: "{group_name}")
        }}
    }}"""
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt, context=context)
    assert "errors" not in result
    assert len(result["data"]["me"]["permissions"]) == 0
    assert result["data"]["me"]["role"] == "customeradmin"

    context = get_new_context()
    query = """
        mutation {
            invalidateAccessToken {
                success
            }
        }
    """
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt, context=context)
    assert "errors" not in result
    assert result["data"]["invalidateAccessToken"]["success"]

    context = get_new_context()
    query = f"""{{
        me(callerOrigin: "API") {{
            accessToken
            callerOrigin
            organizations {{
                name
            }}
            permissions(entity: USER)
            remember
            role(entity: USER)
            sessionExpiration
            subscriptionsToEntityReport{{
                entity
                frequency
                subject

            }}
            tags(organizationId: "{org_id}") {{
                name
                projects {{
                    name
                }}
            }}
            __typename
        }}
    }}"""
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt, context=context)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Login required"
