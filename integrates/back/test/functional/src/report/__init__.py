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


async def get_result(
    *,
    user: str,
    group_name: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            report(
                groupName: "{group_name}",
                reportType: PDF,
                lang: EN,
                verificationCode: "123"
            ) {{
                success
            }}
        }}
    """
    data: dict[str, str] = {
        "query": query,
    }
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_result_treatments(
    *,
    user: str,
    group_name: str,
    report_type: str,
    treatments: list[str],
) -> dict[str, Any]:
    query: str = """
        query RequestGroupReport(
            $reportType: ReportType!
            $groupName: String!
            $lang: ReportLang
            $treatments: [VulnerabilityTreatment!]
        ) {
            report(
                reportType: $reportType
                groupName: $groupName
                lang: $lang
                treatments: $treatments
                verificationCode: "123"
            ) {
                success
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "reportType": report_type,
            "groupName": group_name,
            "treatments": treatments,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_result_states(
    *,
    user: str,
    group_name: str,
    report_type: str,
    treatments: list[str],
    states: list[str],
) -> dict[str, Any]:
    query: str = """
        query RequestGroupReport(
            $reportType: ReportType!
            $groupName: String!
            $lang: ReportLang
            $treatments: [VulnerabilityTreatment!]
            $states: [VulnerabilityState!]
        ) {
            report(
                reportType: $reportType
                groupName: $groupName
                lang: $lang
                treatments: $treatments
                verificationCode: "123"
                states: $states
            ) {
                success
            }
        }
    """
    data: dict[str, Any] = {
        "query": query,
        "variables": {
            "reportType": report_type,
            "groupName": group_name,
            "treatments": treatments,
            "states": states,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
