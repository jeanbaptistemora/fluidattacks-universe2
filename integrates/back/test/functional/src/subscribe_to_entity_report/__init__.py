# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def put_mutation(
    *,
    entity: str,
    email: str,
    frequency: str,
    subject: str,
) -> dict[str, Any]:
    query: str = """
        mutation SubscribeToEntityReport(
            $frequency: Frequency!
            $reportEntity: SubscriptionReportEntity!
            $reportSubject: String!
        ) {
            subscribeToEntityReport(
                frequency: $frequency
                reportEntity: $reportEntity
                reportSubject: $reportSubject
            ) {
                success
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "frequency": frequency,
            "reportEntity": entity,
            "reportSubject": subject,
        },
    }
    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )


async def get_query(
    *,
    email: str,
) -> dict[str, Any]:
    query: str = """
        query SubscriptionsToEntityReport {
            me {
                subscriptionsToEntityReport {
                    entity
                    frequency
                    subject
                }
                userEmail
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=email,
        context=get_new_context(),
    )
