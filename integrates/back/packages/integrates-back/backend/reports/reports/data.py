# Standard library
import contextlib
import os
import subprocess
import tempfile
from typing import (
    Any,
    Dict,
    Iterator,
    List,
)
from uuid import uuid4

# Local libraries
from backend.dal.helpers.s3 import (
    download_file,
    list_files,
)
from backend.domain import (
    notifications as notifications_domain
)
from backend.reports.reports import technical as technical_report
from backend.typing import Finding as FindingType
from backend.utils import (
    reports as reports_utils,
)
from newutils.passphrase import get_passphrase
from __init__ import (
    FI_AWS_S3_BUCKET as EVIDENCES_BUCKET,
)


async def generate(
    *,
    context: Any,
    findings_ord: List[Dict[str, FindingType]],
    group: str,
    group_description: str,
    requester_email: str,
) -> None:
    passphrase = get_passphrase(4)

    with tempfile.TemporaryDirectory() as directory:
        await _append_pdf_report(
            directory=directory,
            findings_ord=findings_ord,
            group=group,
            group_description=group_description,
            passphrase=passphrase,
            requester_email=requester_email,
        )
        await _append_xls_report(
            context,
            directory=directory,
            findings_ord=findings_ord,
            passphrase=passphrase,
        )
        await _append_evidences(
            directory=directory,
            group=group,
        )

        with _encrypted_zip_file(
            passphrase=passphrase,
            source_contents=_get_directory_contents(directory),
        ) as file:
            signed_url = await reports_utils.sign_url(
                await reports_utils.upload_report(file)
            )

            await notifications_domain.new_password_protected_report(
                file_link=signed_url,
                file_type='Group Data',
                passphrase=passphrase,
                project_name=group,
                user_email=requester_email,
            )


async def _append_pdf_report(
    *,
    directory: str,
    findings_ord: List[Dict[str, FindingType]],
    group: str,
    group_description: str,
    passphrase: str,
    requester_email: str,
) -> None:
    # Generate the PDF report
    report_filename = await technical_report.generate_pdf_file(
        description=group_description,
        findings_ord=findings_ord,
        group_name=group,
        lang='en',
        passphrase=passphrase,
        user_email=requester_email,
    )
    with open(os.path.join(directory, 'report.pdf'), mode='wb') as file:
        with open(report_filename, 'rb') as report:
            file.write(report.read())


async def _append_xls_report(
    context: Any,
    directory: str,
    findings_ord: List[Dict[str, FindingType]],
    passphrase: str,
) -> None:
    report_filename = await technical_report.generate_xls_file(
        context,
        findings_ord=findings_ord,
        passphrase=passphrase,
    )
    with open(os.path.join(directory, 'report.xls'), mode='wb') as file:
        with open(report_filename, 'rb') as report:
            file.write(report.read())


async def _append_evidences(
    *,
    directory: str,
    group: str,
) -> None:
    target_folders: Dict[str, str] = {
        '': 'evidences',
        '.exp': 'exploits',
        '.gif': 'evidences',
        '.jpg': 'evidences',
        '.png': 'evidences',
        '.py': 'exploits',
        '.txt': 'compromised-records',
    }

    # Walk everything under the S3 evidences bucket and save relevant info
    for key in await list_files(EVIDENCES_BUCKET, group):
        _, extension = os.path.splitext(key)

        if extension in target_folders:
            target_name = os.path.join(directory, target_folders[extension])
            os.makedirs(target_name, exist_ok=True)
            target_name = os.path.join(target_name, os.path.basename(key))
            await download_file(EVIDENCES_BUCKET, key, target_name)


@contextlib.contextmanager
def _encrypted_zip_file(
    *,
    passphrase: str,
    source_contents: List[str],
) -> Iterator[str]:
    # This value must be sanitized because it needs to be passed as OS command
    if not all(word.isalpha() for word in passphrase.split(' ')):
        raise ValueError(
            f'Expected words separated by spaces as passphrase: {passphrase}'
        )

    # If there are no source contents the current working directory is assumed
    #   by default.
    # We don't want to leave the sandbox at any point
    if not source_contents:
        raise RuntimeError('Nothing to pack into the final file')

    # Impossible to predict with this uuid4
    with tempfile.NamedTemporaryFile() as temp_file:
        target = temp_file.name + f'_{uuid4()}.7z'

    subprocess.run(
        [
            '7z', 'a', f'-p{passphrase}', '-mhe', '-t7z',
            '--', target, *source_contents
        ],
        check=True,
    )

    try:
        yield target
    finally:
        os.unlink(target)


def _get_directory_contents(directory: str) -> List[str]:
    return [
        absolute
        for relative in os.listdir(directory)
        for absolute in [os.path.join(directory, relative)]
        if (os.path.isfile(absolute) or
            os.path.isdir(absolute) and
            os.listdir(absolute))
    ]
