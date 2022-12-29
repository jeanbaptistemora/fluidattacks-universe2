# pylint: disable=import-error
import asyncio
from back.test.functional.src.utils import (
    get_graphql_result,
)
from batch.dal import (
    get_actions,
)
from batch.types import (
    BatchProcessing,
)
from dataloaders import (
    get_new_context,
)
import os
import subprocess
from typing import (
    Any,
    List,
    Optional,
)


async def _get_batch_job(
    *, entity: str, additional_info: str, subject: str
) -> BatchProcessing:
    all_actions = await get_actions()
    return next(
        (
            action
            for action in all_actions
            if action.entity == entity
            and additional_info in action.additional_info
            and subject in action.subject
        )
    )


async def run(*, entity: str, additional_info: str, subject: str) -> int:
    batch_action = await _get_batch_job(
        entity=entity, additional_info=additional_info, subject=subject
    )
    cmd_args: List[str] = [
        "test",
        batch_action.key,
    ]
    process: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(
        os.environ["BATCH_BIN"],
        *cmd_args,
        stdin=subprocess.DEVNULL,
    )

    return await process.wait()


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
