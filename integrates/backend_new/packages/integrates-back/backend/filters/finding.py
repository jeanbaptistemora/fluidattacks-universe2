from typing import Dict, List, cast

from backend.typing import (
    Finding as FindingType,
    Historic as HistoricType
)


def filter_non_approved_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    no_approved_findings = [
        finding
        for finding in findings
        if cast(
            HistoricType,
            finding.get('historic_state', [{}])
        )[-1].get('state', '') != 'APPROVED'
    ]

    return no_approved_findings


def filter_non_created_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    non_submited_findings = [
        finding
        for finding in findings
        if cast(
            HistoricType,
            finding.get('historic_state', [{}])
        )[-1].get('state', '') != 'CREATED'
    ]

    return non_submited_findings


def filter_non_deleted_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    no_deleted_findings = [
        finding
        for finding in findings
        if cast(
            HistoricType,
            finding.get('historic_state', [{}])
        )[-1].get('state', '') != 'DELETED'
    ]

    return no_deleted_findings


def filter_non_rejected_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    non_rejected_findings = [
        finding
        for finding in findings
        if cast(
            HistoricType,
            finding.get('historic_state', [{}])
        )[-1].get('state', '') != 'REJECTED'
    ]

    return non_rejected_findings


def filter_non_submitted_findings(
    findings: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    non_submitted_findings = [
        finding
        for finding in findings
        if cast(
            HistoricType,
            finding.get('historic_state', [{}])
        )[-1].get('state', '') != 'SUBMITTED'
    ]

    return non_submitted_findings


def get_release_date(finding: Dict[str, FindingType]) -> str:
    """Get release date from the historic state"""
    release_date = ''
    current_state_info = {}
    if 'historic_state' in finding:
        current_state_info = cast(
            HistoricType,
            finding['historic_state']
        )[-1]
    elif 'historicState' in finding:
        current_state_info = cast(
            HistoricType,
            finding['historicState']
        )[-1]
    if current_state_info.get('state', '') == 'APPROVED':
        release_date = current_state_info['date']

    return release_date


def is_released(finding: Dict[str, FindingType]) -> bool:
    """Determine if a finding is released from the historic state"""
    is_finding_released = False
    if get_release_date(finding):
        is_finding_released = True

    return is_finding_released
