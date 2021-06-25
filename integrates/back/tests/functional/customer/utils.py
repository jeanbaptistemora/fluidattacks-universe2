from back.tests.functional.utils import (
    complete_register,
    get_graphql_result,
)
from dataloaders import (
    Dataloaders,
)
from typing import (
    Any,
    Dict,
    Optional,
)

MANAGER = "integratesmanager@gmail.com"
CUSTOMER = "integratescustomer@gmail.com"


async def get_result(
    data: Dict[str, Any],
    stakeholder: str = CUSTOMER,
    session_jwt: Optional[str] = None,
    context: Optional[Dataloaders] = None,
) -> Dict[str, Any]:
    """Get result for customer role."""
    result = await get_graphql_result(data, stakeholder, session_jwt, context)

    return result


async def create_group() -> str:
    query = """{
        internalNames(entity: GROUP){
            name
            __typename
        }
    }"""
    data = {"query": query}
    result = await get_result(data, stakeholder=MANAGER)
    assert "errors" not in result
    assert "internalNames" in result["data"]
    group_name = result["data"]["internalNames"]["name"]

    org_name = "okada"
    query = f"""
        mutation {{
            createGroup(
                organization: "{org_name}",
                description: "This is a new group from pytest",
                projectName: "{group_name}",
                subscription: CONTINUOUS,
                hasMachine: true,
                hasSquad: true,
                hasForces: true
            ) {{
            success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, stakeholder=MANAGER)
    assert "success" in result["data"]["createGroup"]
    assert result["data"]["createGroup"]["success"]

    role = "CUSTOMER"
    customer_email = CUSTOMER
    query = f"""
        mutation {{
            grantStakeholderAccess (
                email: "{customer_email}",
                phoneNumber: "-",
                groupName: "{group_name}",
                responsibility: "Customer",
                role: {role}
            ) {{
            success
                grantedStakeholder {{
                    email
                }}
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, stakeholder=MANAGER)
    assert "errors" not in result
    assert result["data"]["grantStakeholderAccess"]["success"]
    assert await complete_register(customer_email, group_name)

    return group_name
