from back.tests.functional.executive.utils import (
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
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert "success" in result["data"]["signIn"]
    assert not result["data"]["signIn"]["success"]

    context = get_new_context()
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
            role
            sessionExpiration
            subscriptionsToEntityReport{{
                entity
                frequency
                subject
            }}
            tags(organizationId: "{org_id}") {{
                name
                groups {{
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
    assert result["data"]["me"]["organizations"] == [{"name": org_name}]
    assert len(result["data"]["me"]["permissions"]) == 0
    assert not result["data"]["me"]["remember"]
    assert result["data"]["me"]["role"] == "executive"
    assert result["data"]["me"]["sessionExpiration"] == str(
        datetime.fromtimestamp(int_expiration_time)
    )
    assert result["data"]["me"]["subscriptionsToEntityReport"] == [
        {"entity": entity, "frequency": frecuency, "subject": org_id}
    ]
    assert result["data"]["me"]["tags"] == [
        {
            "name": "test-projects",
            "groups": [
                {"name": "oneshottest"},
                {"name": "unittesting"},
            ],
        },
        {
            "name": "test-updates",
            "groups": [
                {"name": "oneshottest"},
                {"name": "unittesting"},
            ],
        },
    ]
    assert result["data"]["me"]["__typename"] == "Me"

    context = get_new_context()
    query = f"""{{
        group(groupName:"{group_name}"){{
            userRole
            permissions
        }}
    }}"""
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt, context=context)
    assert "errors" not in result
    assert len(result["data"]["group"]["permissions"]) == 51
    assert result["data"]["group"]["userRole"] == "executive"

    context = get_new_context()
    query = f"""{{
        organization(
            organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
        )
        {{
            permissions(identifier: "{group_name}")
            userRole(identifier: "{group_name}")
        }}
    }}"""
    data = {"query": query}
    result = await get_result(data, session_jwt=session_jwt, context=context)
    assert "errors" not in result
    assert len(result["data"]["organization"]["permissions"]) == 0
    assert result["data"]["organization"]["userRole"] == "executive"

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
            role
            sessionExpiration
            subscriptionsToEntityReport{{
                entity
                frequency
                subject
            }}
            tags(organizationId: "{org_id}") {{
                name
                groups {{
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
