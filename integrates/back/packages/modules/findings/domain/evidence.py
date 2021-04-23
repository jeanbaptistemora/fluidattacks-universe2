# Standard libraries
import io
import itertools
import logging
import logging.config
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Union,
)

# Third-party libraries
from backports import csv
from magic import Magic
from starlette.datastructures import UploadFile

# Local libraries
from back.settings import LOGGING
from backend import util
from custom_exceptions import (
    EvidenceNotFound,
    InvalidFileSize,
    InvalidFileType,
)
from findings import dal as findings_dal
from newutils import (
    datetime as datetime_utils,
    findings as finding_utils,
    validations,
)
from .core import get_finding


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def download_evidence_file(
    group_name: str,
    finding_id: str,
    file_name: str
) -> str:
    file_id = '/'.join([group_name.lower(), finding_id, file_name])
    file_exists = await findings_dal.search_evidence(file_id)
    if file_exists:
        start = file_id.find(finding_id) + len(finding_id)
        localfile = f'/tmp{file_id[start:]}'
        ext = {'.py': '.tmp'}
        tmp_filepath = util.replace_all(localfile, ext)
        await findings_dal.download_evidence(file_id, tmp_filepath)
        return cast(str, tmp_filepath)
    raise Exception('Evidence not found')


async def get_records_from_file(
    group_name: str,
    finding_id: str,
    file_name: str
) -> List[Dict[object, object]]:
    file_path = await download_evidence_file(group_name, finding_id, file_name)
    file_content = []
    encoding = Magic(mime_encoding=True).from_file(file_path)
    try:
        with io.open(file_path, mode='r', encoding=encoding) as records_file:
            csv_reader = csv.reader(records_file)
            max_rows = 1000
            headers = next(csv_reader)
            file_content = [
                util.list_to_dict(headers, row)
                for row in itertools.islice(csv_reader, max_rows)
            ]
    except (csv.Error, LookupError, UnicodeDecodeError) as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return file_content


async def remove_evidence(evidence_name: str, finding_id: str) -> bool:
    finding = await get_finding(finding_id)
    group_name = finding['projectName']
    files = cast(List[Dict[str, str]], finding.get('files', []))
    success = False

    evidence: Dict[str, str] = next(
        (item for item in files if item['name'] == evidence_name),
        dict()
    )
    if not evidence:
        raise EvidenceNotFound()

    evidence_id = str(evidence.get('file_url', ''))
    full_name = f'{group_name}/{finding_id}/{evidence_id}'
    if await findings_dal.remove_evidence(full_name):
        index = files.index(evidence)
        del files[index]
        success = await findings_dal.update(finding_id, {'files': files})
    return success


async def update_evidence(
    finding_id: str,
    evidence_type: str,
    file: UploadFile
) -> bool:
    finding = await get_finding(finding_id)
    files = cast(List[Dict[str, str]], finding.get('files', []))
    group_name = str(finding.get('projectName', ''))
    today = datetime_utils.get_now_as_str()
    success = False

    if evidence_type == 'fileRecords':
        old_file_name: str = next(
            (
                item['file_url']
                for item in files
                if item['name'] == 'fileRecords'
            ),
            ''
        )
        if old_file_name != '':
            old_records = await get_records_from_file(
                group_name,
                finding_id,
                old_file_name
            )
            if old_records:
                file = await finding_utils.append_records_to_file(
                    cast(List[Dict[str, str]], old_records),
                    file
                )

    evidence_id = f'{group_name}-{finding_id}-{evidence_type}'
    full_name = f'{group_name}/{finding_id}/{evidence_id}'
    if await findings_dal.save_evidence(file, full_name):
        evidence: Union[Dict[str, str], List[Optional[Any]]] = next(
            (item for item in files if item['name'] == evidence_type),
            []
        )
        if evidence:
            index = files.index(cast(Dict[str, str], evidence))
            success = await findings_dal.update(
                finding_id,
                {
                    f'files[{index}].file_url': evidence_id,
                    f'files[{index}].upload_date': today
                }
            )
        else:
            success = await findings_dal.list_append(
                finding_id,
                'files',
                [{
                    'name': evidence_type,
                    'file_url': evidence_id,
                    'upload_date': today,
                }]
            )
    return success


async def update_evidence_description(
    finding_id: str,
    evidence_type: str,
    description: str
) -> bool:
    validations.validate_fields(cast(List[str], [description]))
    finding = await get_finding(finding_id)
    files = cast(List[Dict[str, str]], finding.get('files', []))
    success = False

    evidence: Union[Dict[str, str], List[Optional[Any]]] = next(
        (item for item in files if item['name'] == evidence_type),
        []
    )
    if evidence:
        index = files.index(cast(Dict[str, str], evidence))
        success = await findings_dal.update(
            finding_id,
            {f'files[{index}].description': description}
        )
    else:
        raise EvidenceNotFound()
    return success


async def validate_and_upload_evidence(
    finding_id: str,
    evidence_id: str,
    file: UploadFile
) -> bool:
    success = False
    if await validate_evidence(evidence_id, file):
        success = await update_evidence(finding_id, evidence_id, file)
    return success


async def validate_evidence(evidence_id: str, file: UploadFile) -> bool:
    mib = 1048576
    success = False
    allowed_mimes = []
    max_size = 10

    if evidence_id in ['animation', 'exploitation']:
        allowed_mimes = ['image/gif', 'image/png']
    elif evidence_id.startswith('evidence'):
        allowed_mimes = ['image/png']
    elif evidence_id == 'fileRecords':
        allowed_mimes = ['text/csv', 'text/plain', 'application/csv']

    if not await util.assert_uploaded_file_mime(file, allowed_mimes):
        raise InvalidFileType()

    if await util.get_file_size(file) < max_size * mib:
        success = True
    else:
        raise InvalidFileSize()
    return success
