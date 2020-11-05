# Standard libraries
import subprocess
import tempfile
from typing import IO, List, NamedTuple
# Third party libraries
# Local libraries
from streamer_dynamodb.extractor import PageData


class SingerPageData(NamedTuple):
    file: IO[str]


def transform_page(dpage: PageData) -> SingerPageData:
    file = tempfile.NamedTemporaryFile(mode='w+')
    cmd = (
        "echo '[INFO] Running tap' && "
        f'tap-json > {file.name} < "{dpage.file.name}"'
    )
    subprocess.check_output(cmd, shell=True)
    return SingerPageData(
        file=file
    )


def transform_pages(pages: List[PageData]) -> List[SingerPageData]:
    spages = []
    for page in pages:
        spages.append(transform_page(page))
    return spages
