# pylint:disable=too-many-branches
from typing import Dict, List, Union, cast
from magic import Magic

from backend import util
from backend.dal import finding as finding_dal
from backend.exceptions import (
    EvidenceNotFound,
    InvalidFileType,
    InvalidFileSize
)
from backend.utils import (
    findings as finding_utils,
    validations
)
from .finding import get_finding


async def update_evidence(finding_id: str, evidence_type: str, file) -> bool:
    finding = await get_finding(finding_id)
    files = cast(List[Dict[str, str]], finding.get('files', []))
    project_name = str(finding.get('projectName', ''))
    success = False

    if evidence_type == 'fileRecords':
        old_file_name: str = next(
            (
                item['file_url']
                for item in files
                if item['name'] == 'fileRecords'
            ), ''
        )
        if old_file_name != '':
            old_records = await finding_utils.get_records_from_file(
                project_name, finding_id, old_file_name)
            if old_records:
                file = finding_utils.append_records_to_file(cast(
                    List[Dict[str, str]],
                    old_records
                ), file)
                file.open()

    try:
        mime = Magic(mime=True).from_buffer(file.file.getvalue())
        extension = {
            'image/gif': '.gif',
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'application/x-empty': '.exp',
            'text/x-python': '.exp',
            'text/csv': '.csv',
            'text/plain': '.txt'
        }[mime]
    except AttributeError:
        extension = ''
    evidence_id = f'{project_name}-{finding_id}-{evidence_type}{extension}'
    full_name = f'{project_name}/{finding_id}/{evidence_id}'

    if await finding_dal.save_evidence(file, full_name):
        evidence: Union[Dict[str, str], list] = next(
            (
                item
                for item in files
                if item['name'] == evidence_type
            ), []
        )
        if evidence:
            index = files.index(cast(Dict[str, str], evidence))
            if files[index].get('file_url', evidence_id) != evidence_id:
                # old evidence that does not comply the
                # namestyle will not be replaced and be orphan
                await finding_dal.remove_evidence(
                    '{group_name}/{finding_id}/{file_url}'.format(
                        group_name=project_name,
                        finding_id=finding_id,
                        file_url=files[index].get('file_url', '')
                    )
                )
            success = await finding_dal.update(
                finding_id,
                {f'files[{index}].file_url': evidence_id}
            )
        else:
            success = await finding_dal.list_append(
                finding_id,
                'files',
                [{'name': evidence_type, 'file_url': evidence_id}]
            )

    return success


async def update_evidence_description(
        finding_id: str,
        evidence_type: str,
        description: str) -> bool:
    validations.validate_fields(cast(List[str], [description]))
    finding = await get_finding(finding_id)
    files = cast(
        List[Dict[str, str]],
        finding.get('files', [])
    )
    success = False

    evidence: Union[Dict[str, str], list] = next(
        (
            item
            for item in files
            if item['name'] == evidence_type
        ), []
    )
    if evidence:
        index = files.index(cast(Dict[str, str], evidence))
        success = await finding_dal.update(
            finding_id,
            {f'files[{index}].description': description}
        )
    else:
        raise EvidenceNotFound()

    return success


async def remove_evidence(evidence_name: str, finding_id: str) -> bool:
    finding = await get_finding(finding_id)
    project_name = finding['projectName']
    files = cast(
        List[Dict[str, str]],
        finding.get('files', [])
    )
    success = False

    evidence: Dict[str, str] = next(
        (
            item
            for item in files
            if item['name'] == evidence_name
        ), dict()
    )
    if not evidence:
        raise EvidenceNotFound()

    evidence_id = str(evidence.get('file_url', ''))
    full_name = f'{project_name}/{finding_id}/{evidence_id}'

    if await finding_dal.remove_evidence(full_name):
        index = files.index(evidence)
        del files[index]
        success = await finding_dal.update(
            finding_id, {'files': files})

    return success


def validate_evidence(evidence_id: str, file) -> bool:
    mib = 1048576
    success = False
    max_size = {
        'animation': 15,
        'exploitation': 10,
        'exploit': 1,
        'fileRecords': 1
    }

    if (evidence_id in ['animation', 'exploitation'] or
            evidence_id.startswith('evidence')):
        allowed_mimes = ['image/gif', 'image/jpeg', 'image/png']
        if not util.assert_uploaded_file_mime(file, allowed_mimes):
            raise InvalidFileType()
    elif evidence_id == 'exploit':
        allowed_mimes = ['text/x-python', 'text/plain']
        if not util.assert_uploaded_file_mime(file, allowed_mimes):
            raise InvalidFileType()
    elif evidence_id == 'fileRecords':
        allowed_mimes = ['text/csv', 'text/plain']
        if not util.assert_uploaded_file_mime(file, allowed_mimes):
            raise InvalidFileType()

    if file.size > max_size.get(evidence_id, 10) * mib:
        raise InvalidFileSize()
    success = True

    return success
