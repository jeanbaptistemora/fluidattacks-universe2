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
from typing import (
    Any,
    Optional,
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
    verifications: list[str],
    age: int,
) -> dict[str, Any]:
    query: str = """
        query RequestGroupReport(
            $reportType: ReportType!
            $groupName: String!
            $lang: ReportLang
            $treatments: [VulnerabilityTreatment!]
            $states: [VulnerabilityState!]
            $verifications: [VulnerabilityVerification!]
            $age: Int
        ) {
            report(
                reportType: $reportType
                groupName: $groupName
                lang: $lang
                treatments: $treatments
                verificationCode: "123"
                states: $states
                verifications: $verifications
                age: $age
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
            "verifications": verifications,
            "age": age,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def get_result_closing_date(
    *,
    user: str,
    group_name: str,
    report_type: str,
    treatments: list[str],
    states: list[str],
    verifications: list[str],
    closing_date: Optional[str],
    finding_title: str,
    min_severity: Optional[float],
    max_severity: Optional[float],
) -> dict[str, Any]:
    query: str = """
        query RequestGroupReport(
            $reportType: ReportType!
            $groupName: String!
            $lang: ReportLang
            $treatments: [VulnerabilityTreatment!]
            $states: [VulnerabilityState!]
            $verifications: [VulnerabilityVerification!]
            $closingDate: DateTime
            $findingTitle: String
            $minSeverity: Float
            $maxSeverity: Float
        ) {
            report(
                reportType: $reportType
                groupName: $groupName
                lang: $lang
                treatments: $treatments
                verificationCode: "123"
                states: $states
                closingDate: $closingDate
                verifications: $verifications
                findingTitle: $findingTitle
                minSeverity: $minSeverity
                maxSeverity: $maxSeverity
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
            "verifications": verifications,
            "closingDate": closing_date,
            "findingTitle": finding_title,
            "minSeverity": min_severity,
            "maxSeverity": max_severity,
        },
    }

    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
