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


def get_historic_state(finding: Dict[str, FindingType]) -> HistoricType:
    historic_state = []
    if 'historic_state' in finding:
        historic_state = cast(
            HistoricType,
            finding['historic_state']
        )
    elif 'historicState' in finding:
        historic_state = cast(
            HistoricType,
            finding['historicState']
        )

    return historic_state


def get_creation_date(finding: Dict[str, FindingType]) -> str:
    """Get creation date from the historic state"""
    creation_date = ''
    historic_state = get_historic_state(finding)
    if historic_state:
        creation_info = list(filter(
            lambda state_info: state_info['state'] == 'CREATED',
            historic_state
        ))
    if creation_info:
        creation_date = creation_info[-1]['date']

    return creation_date


def is_created(finding: Dict[str, FindingType]) -> bool:
    """Determine if a finding is created from the historic state"""

    return bool(get_creation_date(finding))


def get_submission_date(finding: Dict[str, FindingType]) -> str:
    """Get submission date from the historic state"""
    submission_date = ''
    historic_state = get_historic_state(finding)
    if historic_state:
        submission_info = list(filter(
            lambda state_info: state_info['state'] == 'SUBMITTED',
            historic_state
        ))
    if submission_info:
        submission_date = submission_info[-1]['date']

    return submission_date


def is_submitted(finding: Dict[str, FindingType]) -> bool:
    """Determine if a finding is submitted from the historic state"""

    return bool(get_submission_date(finding))


def get_approval_date(finding: Dict[str, FindingType]) -> str:
    """Get approval date from the historic state"""
    approval_date = ''
    historic_state = get_historic_state(finding)
    if historic_state:
        approval_info = list(filter(
            lambda state_info: state_info['state'] == 'APPROVED',
            historic_state
        ))
    if approval_info:
        approval_date = approval_info[-1]['date']

    return approval_date


def is_approved(finding: Dict[str, FindingType]) -> bool:
    """Determine if a finding is approved from the historic state"""

    return bool(get_approval_date(finding))
