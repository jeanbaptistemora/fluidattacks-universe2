from back.tests.functional.closer.utils import (
    get_result,
)
from datetime import (
    datetime,
    timedelta,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("old")
async def test_me() -> None:  # pylint: disable=too-many-statements
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    org_name = "okada"
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
    result = await get_result(data)
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

    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert result["data"]["updateAccessToken"]["success"]
    session_jwt = result["data"]["updateAccessToken"]["sessionJwt"]

    query = """
        mutation {
            addPushToken(token: "ExponentPushToken[something123]") {
                success
            }
        }
    """
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt)
    assert "error" not in result
    assert result["data"]["addPushToken"]["success"]

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
    result = await get_result(data, session_jwt=session_jwt)
    assert "errors" not in result
    assert result["data"]["subscribeToEntityReport"]["success"]

    query = """
        mutation {
            acceptLegal(remember: false) {
                success
            }
        }
    """
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt)
    assert "errors" not in result
    assert result["data"]["acceptLegal"]["success"]

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
    result = await get_result(data, session_jwt=session_jwt)
    assert "errors" not in result
    assert '{"hasAccessToken": true' in result["data"]["me"]["accessToken"]
    assert result["data"]["me"]["callerOrigin"] == "API"
    assert result["data"]["me"]["organizations"] == [{"name": org_name}]
    assert len(result["data"]["me"]["permissions"]) == 0
    assert not result["data"]["me"]["remember"]
    assert result["data"]["me"]["role"] == "closer"
    assert result["data"]["me"]["sessionExpiration"] == str(
        datetime.fromtimestamp(int_expiration_time)
    )
    assert result["data"]["me"]["subscriptionsToEntityReport"] == [
        {"entity": entity, "frequency": frecuency, "subject": org_id}
    ]
    assert result["data"]["me"]["tags"] == [
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

    query = f"""{{
        me(callerOrigin: "API") {{
            permissions(entity: PROJECT, identifier: "{group_name}")
            role(entity: PROJECT, identifier: "{group_name}")
        }}
    }}"""
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt)
    assert "errors" not in result
    assert len(result["data"]["me"]["permissions"]) == 49
    assert result["data"]["me"]["role"] == "closer"

    query = f"""{{
        me(callerOrigin: "API") {{
            permissions(entity: ORGANIZATION, identifier: "{group_name}")
            role(entity: ORGANIZATION, identifier: "{group_name}")
        }}
    }}"""
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt)
    assert "errors" not in result
    assert len(result["data"]["me"]["permissions"]) == 0
    assert result["data"]["me"]["role"] == "closer"

    query = """
        mutation {
            invalidateAccessToken {
                success
            }
        }
    """
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt)
    assert "errors" not in result
    assert result["data"]["invalidateAccessToken"]["success"]

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
    result = await get_result(data, session_jwt=session_jwt)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Login required"
